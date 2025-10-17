from typing import Literal, List, Tuple
import logging
import os
import weakref
from threading import Lock

log = logging.getLogger("socketdev")

IntegrationType = Literal["api", "github", "gitlab", "bitbucket", "azure"]
INTEGRATION_TYPES = ("api", "github", "gitlab", "bitbucket", "azure")


class FileDescriptorManager:
    """
    Global manager to track and limit the number of open file descriptors.
    Automatically closes least recently used files when limit is reached.
    """
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.max_open_files = 100  # Default limit, can be overridden
            self.open_files = []  # List of weakrefs to LazyFileLoader instances
            self._initialized = True
            log.debug(f"FileDescriptorManager initialized with default max_open_files={self.max_open_files}")
    
    def set_max_open_files(self, max_files: int):
        """Set the maximum number of open files."""
        with self._lock:
            self.max_open_files = max_files
            log.debug(f"FileDescriptorManager max_open_files set to {self.max_open_files}")
            
            # If we're now over the limit, close some files
            while len(self.open_files) >= self.max_open_files:
                self.open_files = [ref for ref in self.open_files if ref() is not None]
                if len(self.open_files) >= self.max_open_files and self.open_files:
                    oldest_ref = self.open_files.pop(0)
                    oldest_file = oldest_ref()
                    if oldest_file is not None and oldest_file._file is not None:
                        oldest_file.close()
                        log.debug(f"Auto-closed file due to new descriptor limit: {oldest_file.file_path}")
                else:
                    break
    
    def register_file_open(self, lazy_file_loader):
        """Register a file as opened and manage the descriptor limit."""
        with self._lock:
            # Remove any dead weak references
            self.open_files = [ref for ref in self.open_files if ref() is not None]
            
            # If we're at the limit, close the oldest file
            if len(self.open_files) >= self.max_open_files:
                oldest_ref = self.open_files.pop(0)
                oldest_file = oldest_ref()
                if oldest_file is not None and oldest_file._file is not None:
                    oldest_file.close()
                    log.debug(f"Auto-closed file due to descriptor limit: {oldest_file.file_path}")
            
            # Add the new file to the end of the list
            self.open_files.append(weakref.ref(lazy_file_loader))
    
    def unregister_file(self, lazy_file_loader):
        """Remove a file from the tracking list when it's closed."""
        with self._lock:
            self.open_files = [ref for ref in self.open_files 
                             if ref() is not None and ref() is not lazy_file_loader]


# Global instance
_fd_manager = FileDescriptorManager()


class LazyFileLoader:
    """
    A file-like object that only opens the actual file when needed for reading.
    This prevents keeping too many file descriptors open simultaneously.
    
    This class implements the standard file-like interface that requests library
    expects for multipart uploads, making it a drop-in replacement for regular
    file objects.
    """
    
    def __init__(self, file_path: str, name: str):
        self.file_path = file_path
        self.name = name
        self._file = None
        self._closed = False
        self._position = 0
        self._size = None
    
    def _ensure_open(self):
        """Ensure the file is open and seek to the correct position."""
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        
        if self._file is None:
            try:
                self._file = open(self.file_path, 'rb')
                _fd_manager.register_file_open(self)
                log.debug(f"Opened file for reading: {self.file_path}")
                # Seek to the current position if we've been reading before
                if self._position > 0:
                    self._file.seek(self._position)
            except OSError as e:
                if e.errno == 24:  # Too many open files
                    # Try to force garbage collection to close unused files
                    import gc
                    gc.collect()
                    # Retry once
                    self._file = open(self.file_path, 'rb')
                    _fd_manager.register_file_open(self)
                    log.debug(f"Opened file for reading (after gc): {self.file_path}")
                    if self._position > 0:
                        self._file.seek(self._position)
                else:
                    raise
    
    def _get_size(self):
        """Get file size without keeping file open."""
        if self._size is None:
            self._size = os.path.getsize(self.file_path)
        return self._size
    
    def read(self, size: int = -1):
        """Read from the file, opening it if needed."""
        self._ensure_open()
        data = self._file.read(size)
        self._position = self._file.tell()
        
        # If we've read the entire file, close it to free the file descriptor
        if size == -1 or len(data) < size:
            self.close()
            
        return data
    
    def readline(self, size: int = -1):
        """Read a line from the file."""
        self._ensure_open()
        data = self._file.readline(size)
        self._position = self._file.tell()
        return data
    
    def seek(self, offset: int, whence: int = 0):
        """Seek to a position in the file."""
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        
        # Calculate new position for tracking
        if whence == 0:  # SEEK_SET
            self._position = offset
        elif whence == 1:  # SEEK_CUR
            self._position += offset
        elif whence == 2:  # SEEK_END
            # We need to open the file to get its size
            self._ensure_open()
            result = self._file.seek(offset, whence)
            self._position = self._file.tell()
            return result
        
        # If file is already open, seek it too
        if self._file is not None:
            result = self._file.seek(self._position)
            return result
        
        return self._position
    
    def tell(self):
        """Return current file position."""
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        
        if self._file is not None:
            self._position = self._file.tell()
        
        return self._position
    
    def close(self):
        """Close the file if it was opened."""
        if self._file is not None:
            self._file.close()
            log.debug(f"Closed file: {self.file_path}")
            self._file = None
            _fd_manager.unregister_file(self)
        self._closed = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def __len__(self):
        """Return file size. Requests library uses this for Content-Length."""
        return self._get_size()
    
    @property
    def closed(self):
        """Check if the file is closed."""
        return self._closed
    
    @property 
    def mode(self):
        """Return the file mode."""
        return 'rb'
    
    def readable(self):
        """Return whether the file is readable."""
        return not self._closed
    
    def writable(self):
        """Return whether the file is writable."""
        return False
    
    def seekable(self):
        """Return whether the file supports seeking."""
        return True


class Utils:
    @staticmethod
    def validate_integration_type(integration_type: str) -> IntegrationType:
        if integration_type not in INTEGRATION_TYPES:
            raise ValueError(f"Invalid integration type: {integration_type}")
        return integration_type  # type: ignore
    
    @staticmethod
    def load_files_for_sending_lazy(files: List[str], workspace: str = None, max_open_files: int = 100, base_path: str = None, base_paths: List[str] = None) -> List[Tuple[str, Tuple[str, LazyFileLoader]]]:
        """
        Prepares files for sending to the Socket API using lazy loading.
        
        This version doesn't open all files immediately, instead it creates
        LazyFileLoader objects that only open files when they're actually read.
        This prevents "Too many open files" errors when dealing with large numbers
        of manifest files.

        Args:
            files: List of file paths from find_files()
            workspace: Base directory path to make paths relative to
            max_open_files: Maximum number of files to keep open simultaneously (default: 100)
            base_path: Optional base path to strip from key names for cleaner file organization
            base_paths: Optional list of base paths to strip from key names (takes precedence over base_path)

        Returns:
            List of tuples formatted for requests multipart upload:
            [(field_name, (filename, lazy_file_object)), ...]
        """
        # Configure the file descriptor manager with the specified limit
        _fd_manager.set_max_open_files(max_open_files)
        
        send_files = []
        if workspace and "\\" in workspace:
            workspace = workspace.replace("\\", "/")
        if base_path and "\\" in base_path:
            base_path = base_path.replace("\\", "/")
        if base_paths:
            base_paths = [bp.replace("\\", "/") if "\\" in bp else bp for bp in base_paths]
        
        for file_path in files:
            # Normalize file path
            if "\\" in file_path:
                file_path = file_path.replace("\\", "/")
            
            for file_path in files:
                # Normalize file path
                if "\\" in file_path:
                    file_path = file_path.replace("\\", "/")

                # Skip directories
                if os.path.isdir(file_path):
                    continue

                # Handle file path splitting safely
                if "/" in file_path:
                    _, name = file_path.rsplit("/", 1)
                else:
                    name = file_path

                # Calculate the key name for the form data
                key = file_path
                path_stripped = False

                # If base_paths is provided, try to strip one of the paths from the file path
                if base_paths:
                    for bp in base_paths:
                        normalized_base_path = bp.rstrip("/") + "/" if not bp.endswith("/") else bp
                        if key.startswith(normalized_base_path):
                            key = key[len(normalized_base_path):]
                            path_stripped = True
                            break
                        elif key.startswith(bp.rstrip("/")):
                            stripped_base = bp.rstrip("/")
                            if key.startswith(stripped_base + "/") or key == stripped_base:
                                key = key[len(stripped_base):]
                                key = key.lstrip("/")
                                path_stripped = True
                                break
                elif base_path:
                    normalized_base_path = base_path.rstrip("/") + "/" if not base_path.endswith("/") else base_path
                    if key.startswith(normalized_base_path):
                        key = key[len(normalized_base_path):]
                        path_stripped = True
                    elif key.startswith(base_path.rstrip("/")):
                        stripped_base = base_path.rstrip("/")
                        if key.startswith(stripped_base + "/") or key == stripped_base:
                            key = key[len(stripped_base):]
                            key = key.lstrip("/")
                            path_stripped = True

                # If workspace is provided and no base paths matched, fall back to workspace logic
                if not path_stripped and workspace and file_path.startswith(workspace):
                    key = file_path[len(workspace):]
                    # Remove all leading slashes (for absolute paths)
                    while key.startswith("/"):
                        key = key[1:]
                    path_stripped = True

                # Clean up relative path prefixes, but preserve filename dots
                while key.startswith("./"):
                    key = key[2:]
                while key.startswith("../"):
                    key = key[3:]
                # Remove any remaining leading slashes (for absolute paths)
                while key.startswith("/"):
                    key = key[1:]

                # Remove Windows drive letter if present (C:/...)
                if len(key) > 2 and key[1] == ':' and (key[2] == '/' or key[2] == '\\'):
                    key = key[2:]
                    while key.startswith("/"):
                        key = key[1:]

                # Create lazy file loader instead of opening file immediately
                lazy_file = LazyFileLoader(file_path, key)
                payload = (key, (key, lazy_file))
                send_files.append(payload)
            return send_files
