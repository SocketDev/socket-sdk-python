import glob
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
        file = file.replace("\\", '/')
        fixed_files.append(file)
    return fixed_files


def load_files(files: list, loaded_files: list) -> list:
    for file in files:
        if "/" in file:
            _, file_name = file.rsplit("/", 1)
        elif "\\" in file:
            _, file_name = file.rsplit("/", 1)
        else:
            file_name = file
        try:
            file_tuple = (file_name, (file_name, open(file, 'rb'), 'text/plain'))
            loaded_files.append(file_tuple)
        except Exception as error:
            print(f"Unable to open {file}")
            print(error)
            exit(1)
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
                    package.repository
                ]
                output.append(output_object)
    return output
