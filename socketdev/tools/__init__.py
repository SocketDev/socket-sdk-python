import glob
import platform
import sys


def find_package_files(folder: str, file_types: list) -> list:
    files = []
    for file_type in file_types:
        search_pattern = f"{folder}/**/{file_type}"
        result = glob.glob(search_pattern, recursive=True)
        if sys.platform.lower() == "win32":
            result = fix_file_path(result)
        files.extend(result)
    return files


def fix_file_path(files) -> list:
    fixed_files = []
    for file in files:
        fixed_files.append(file.replace("\\", "/"))
    return fixed_files


def load_files(files: list, loaded_files: list, workspace: str | None = None) -> list:
    for original_file in files:
        file = original_file.replace("\\", "/") if platform.system() == "Windows" else original_file
        if "/" in file:
            path, name = file.rsplit("/", 1)
        else:
            path = "."
            name = file
        full_path = f"{path}/{name}"

        # Calculate key based on workspace if provided
        if workspace and full_path.startswith(workspace):
            key = full_path[len(workspace) :]
            key = key.lstrip("/")
            key = key.lstrip("./")
        else:
            key = full_path

        payload = (key, (name, open(full_path, "rb")))  # noqa: SIM115  # caller owns returned upload handles
        loaded_files.append(payload)
    return loaded_files


def prepare_for_csv(dependencies: list, packages: dict) -> list:
    output = []
    for dependency in dependencies:
        if dependency.name in packages:
            for package in packages[dependency.name]:
                output_object = [
                    dependency.repository,
                    dependency.branch,
                    package.name,
                    package.version,
                    package.license,
                    package.repository,
                ]
                output.append(output_object)
    return output
