"""Command-line utility to create Lambda deployment ZIP files"""
import argparse
import os
import echokit
import shutil
import zipfile


def zipdir(path, ziph):
    # Modified from example at:
    # http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    # Modified to use relative paths instead of recreating the entire
    #  directory structure in the ZIP file. Ex: Zipping /home/me/project
    #  would create paths like /home/me/project/test.txt
    # Now this will cause /home/me/project/test.txt to be at the top of
    # the ZIP directory structure
    os.chdir(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root), os.getcwd())
            output_path = os.path.join(rel_path, file)
            ziph.write(output_path)


def copy_dir(project_path):
    """Copies given path to tmp-{project_path}"""
    tmp_path = f"tmp-{os.path.basename(os.path.normpath(project_path))}"
    print(f"Copying project directory to temporary path: {tmp_path}")
    shutil.copytree(project_path, tmp_path)
    shutil.copytree(os.path.dirname(echokit.__file__),
                    os.path.join(tmp_path, 'echokit'))
    return os.path.join(os.path.abspath(os.getcwd()), tmp_path)


def filename_prompt(file_name):
    rename = input(f"File {file_name} already exists. Rename? [Y/n] ")
    rename = rename.strip()
    rename = rename.upper()
    if rename == 'Y':
        new_filename = input("Enter new filename: ")
    else:
        exit()
    path = os.path.join(os.path.abspath(os.getcwd()), new_filename)
    if os.path.exists(path):
        filename_prompt(new_filename)
    else:
        return path


def echodist():
    description = "Creates a deployment package for AWS Lambda"
    epilog = ("Specify the top level of your project with --dir.\nFor "
              "example, if __init__.py is located at  "
              "/home/me/project/project/__init__.py, you would specify "
              "/home/me/proj_root/project\nThis will create "
              "a 'project.zip' file in your current directory.")
    parser = argparse.ArgumentParser(prog='echodist', description=description,
                                     epilog=epilog)
    parser.add_argument('--dir', required=True,
                        help='Directory containing your project')
    args = parser.parse_args()

    out_dir = os.path.abspath(args.dir)
    if not os.path.exists(out_dir):
        raise NotADirectoryError(f"Invalid project path: {out_dir}")
    print(f"Creating Lambda deployment package from:\n\t{out_dir}")

    # If /home/me/project/, then create project.zip in the current working dir
    file_name = f"{os.path.basename(os.path.normpath(out_dir))}.zip"
    file_path = os.path.join(os.path.abspath(os.getcwd()), file_name)
    print(f"Creating deployment package in:\n\t{file_path}")
    if os.path.exists(file_path):
        file_path = filename_prompt(file_name)

    # Copy to tmp directory, cd in and create the archive
    tmp_project_dir = copy_dir(out_dir)
    output_file_path = os.path.join(os.path.abspath(os.getcwd()), file_path)

    dist_zip = zipfile.ZipFile(output_file_path, 'w', zipfile.ZIP_DEFLATED)
    zipdir(tmp_project_dir, dist_zip)
    dist_zip.close()

    print("Deployment package created")
    print(f"Removing temporary directory:\n\t{tmp_project_dir}")
    shutil.rmtree(tmp_project_dir)
    print("Done")
