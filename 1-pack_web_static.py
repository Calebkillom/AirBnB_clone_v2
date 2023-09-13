#!/usr/bin/python
# Fabric script that generates a .tgz archive
# from the contents of the web_static folder of my AirBnB Clone repo 

from fabric.api import local, lcd
import tarfile
import os
from datetime import datetime


def do_pack():
    # Local path to the folder you want to compress (web_static folder)
    folder_to_compress = "web_static"

    # Create the "versions" folder if it doesn't exist
    versions = "versions"
    if not os.path.exists(versions):
        os.makedirs(versions)

    # Get the current date and time
    current_datetime = datetime.now()

    # Create the archive filename based on the current date and time
    archive_filename = current_datetime.strftime("web_static_%Y%m%d%H%M%S.tgz")

    # Create a .tar archive within the "versions" folder
    archive_path = os.path.join(versions, archive_filename)

    # Create a .tar archive
    with lcd(folder_to_compress):
        local("tar -czvf ../" + archive_path + " .")

    # Check if the archive file exists
    if os.path.exists(archive_path):
        return archive_path
    else:
        return None
