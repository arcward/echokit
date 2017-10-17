"""Utility to bundle echokit into a lambda function for deployment as ZIP

Deploying an AWS Lambda function using a ZIP archive requires dependencies
to be included as well. Specifically, this utility copies the specified
directory tree into a temporary one, adds an *echokit* directory at the
top level of that structure, copies the current echokit install into that
directory, and zips it all up.

So rather than explicitly creating this directory in a project and possibly
running into conflicts between that and the version installed via *pip*,
the installed version will always be copied into the final ZIP.
"""
import argparse
import zipfile
import echokit
from os import getcwd, chdir, path, walk
from shutil import copytree, rmtree
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        prog="echozip",
        description="Bundles a specified directory and echokit into a ZIP "
                    "archive for upload to AWS Lambda.",
        epilog="Specify the base directory for your project. A ZIP file "
               "containing the contents of that directory, as well as "
               "an echokit/ directory at the top level of the archive, will "
               "be created in the current working directory."
    )
    parser.add_argument("directory", help='Directory containing your project')
    args = parser.parse_args()
    echozip(args.directory)


def echozip(directory):
    """Create ZIP file packaged with echokit

    :param directory: Project/skill directory
    :return:
    """
    if not path.isdir(directory):
        raise NotADirectoryError(f"Invalid path: {directory}")
    cwd = getcwd()
    proj_dir = path.basename(path.abspath(directory))
    timestamp = datetime.now().strftime("%d-%m-%y-%H%M%S")
    proj_base = f"{proj_dir}_{timestamp}"
    zip_dir = path.join(cwd, proj_base)
    zip_file_path = path.join(cwd, f"{proj_base}.zip")

    if path.exists(zip_dir):
        raise IsADirectoryError(f"Directory already exists! {zip_dir}")
    if path.exists(zip_file_path):
        raise FileExistsError(f"File exists!: {zip_file_path}")

    # Copy the full project directory tree into the temporary directory
    print(f"Copying project to temporary directory: {zip_dir}")
    copytree(directory, zip_dir)
    copytree(path.dirname(echokit.__file__), path.join(zip_dir, 'echokit'))

    # Create the ZIP archive, cd into the temporary directory, then
    # recursively add the entire tree to the ZIP
    print(f"Creating: {zip_file_path}")
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
    chdir(zip_dir)
    for root, dirs, files in walk(zip_dir):
        for file in files:
            out_path = path.join(path.relpath(path.join(root), getcwd()), file)
            print(f"Writing: {out_path}")
            zip_file.write(out_path)
    zip_file.close()
    print(f"Cleaning up, removing temporary directory: {zip_dir}")
    chdir(cwd)
    rmtree(zip_dir)
    print("Done! Created ZIP archive: {zip_file_path}")


if __name__ == '__main__':
    main()