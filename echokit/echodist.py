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
import os
import echokit
import shutil
import zipfile
from datetime import datetime


def echodist():
    prog = "echodist"
    desc = ("Bundles the specified directory into a ZIP archive with echokit "
            "for upload to AWS Lambda")
    epilog = ("Specify the base directory of your project. A ZIP file will "
              "be generated in the current working directory containing "
              "the contents of that directory, as well as echokit at the "
              "top level to enable import statements.")
    parser = argparse.ArgumentParser(prog=prog, description=desc,
                                     epilog=epilog)
    parser.add_argument('project_dir', help="Project base directory")
    args = parser.parse_args()

    # Initial timestamp used to help identify output paths
    timestamp = datetime.now().strftime("%d-%m-%y-%H%M%S")

    if not os.path.isdir(args.project_dir):
        raise NotADirectoryError(f"Invalid project path: {args.project_dir}")

    # Last directory in path is assumed to be the project for naming purposes
    project_base = os.path.basename(os.path.abspath(args.project_dir))
    # temporary directory to hold copy of target project
    temp_path = f"{timestamp}_{project_base}"
    temp_dir = os.path.join(os.getcwd(), temp_path)
    # zip file to be exported
    zip_filename = f"{project_base}_{timestamp}.zip"
    zip_path = os.path.join(os.getcwd(), zip_filename)
    # installation path for the current interpreter
    echokit_path = os.path.dirname(echokit.__file__)
    echokit_target = os.path.join(temp_dir, "echokit")

    if os.path.exists(temp_dir):
        raise IsADirectoryError(f"Directory exists! {temp_dir}")
    if os.path.exists(zip_path):
        raise FileExistsError(f"File exists!: {zip_path}")

    # Copies the target project directory tree into a temporary
    # one, then copies echokit from wherever it's installed, into
    # a new 'echokit/' directory at the top of the target project copy
    print(f"Copying project to temporary directory {temp_dir}")
    shutil.copytree(args.project_dir, temp_dir)
    print(f"Copying echokit lib from {echokit_path} to {echokit_target}")
    shutil.copytree(echokit_path, echokit_target)
    print(f"Creating zip file: {zip_path}")
    zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

    current_dir = os.getcwd()
    os.chdir(temp_dir)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root), os.getcwd())
            out_path = os.path.join(rel_path, file)
            print(f"Writing: {out_path}")
            zip_file.write(out_path)
    zip_file.close()

    print(f"Created: {zip_path}")
    print(f"Cleaning up, deleting temporary directory: {temp_dir}")
    os.chdir(current_dir)
    shutil.rmtree(temp_dir)
    print("Done!")
