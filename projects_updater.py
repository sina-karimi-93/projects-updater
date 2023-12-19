"""
This module is about to run a os command
in multiple directories such as git pull
to update the projects all in once.

Author: Sina Karimi Aliabad
year: 2023
"""

import os
from os.path import exists
from threading import Thread

def get_projects_paths(projects_folder: str) -> iter:
    """
    Gets projects directory and create all projects paths
    and yield them
    -----------------------------------------------------
    -> Params
        projects_folder: str
    <- Return
        Generator
    """
    if not exists(projects_folder):
        raise FileNotFoundError("Desired folder is not exists.")
    try:
        projects_names = os.listdir(path=projects_folder)
        for project_name in projects_names:
            project_path = os.path.join(projects_folder, project_name)
            yield project_path
    except FileNotFoundError:
        print(f"Error:\nSystem can not find the target path:"
              f" {projects_folder}\n")


def run_command_on_directory(project_path: str,
                             command: str) -> None:
    """
    Change current terminal directory to the 
    project path and run git pull command on
    this path to get the latest update.
    -------------------------------------------
    -> Params
        project_path: str
        command: str
    """
    try:
        os.chdir(project_path)
        os.system(command)
    except FileNotFoundError as error:
        print(error, f"Error on Path: {project_path}")


def update_projects(projects_paths: list) -> None:
    """
    For each project, create new thread and assign
    run_command_on_directory as its target to run
    git pull on that directory to get the latests
    updates.
    ----------------------------------------------
    -> Params   
        projects_paths: list
    """
    threads = list()
    for path in projects_paths:
        thread = Thread(target=run_command_on_directory,
                        args=(path, "git pull"))
        thread.start()
        threads.append(thread)
    for th in threads:
        th.join()


if __name__ == "__main__":
    projects_folder_path = ""
    projects_paths = list(get_projects_paths(projects_folder_path))
    while True:
        print("Start Updating...\n")
        update_projects(projects_paths)