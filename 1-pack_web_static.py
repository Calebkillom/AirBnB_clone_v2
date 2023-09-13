#!/usr/bin/python3
# Fabric script that generates a .tgz archive
# from the contents of the web_static folder of my AirBnB Clone repo

from fabric.api import local, lcd
import tarfile
import os
from datetime import datetime


def do_pack():
    """
    returns the archive path
    if the archive has been correctly generated
    """
    folder_to_compress = "web_static"
    versions = "versions"

    if not os.path.exists(versions):
        os.makedirs(versions)

    current_datetime = datetime.now()
    archive_filename = current_datetime.strftime("web_static_%Y%m%d%H%M%S.tgz")
    archive_path = os.path.join(versions, archive_filename)

    with lcd(folder_to_compress):
        local(f"tar -czvf ../{archive_path} .")

    return archive_path if os.path.exists(archive_path) else None
