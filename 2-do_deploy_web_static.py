#!/usr/bin/python3
# Fabric Script that distributes an archive to my web-servers
# Using the do_deploy function

import os
import tarfile
from fabric.api import *
from sys import argv


# Executing remote commands on both of my web servers
env.hosts = ["34.229.189.80", "18.204.11.87"]

# Setting the username to my servers
env.user = argv[-1]

# Setting the password to my servers
env.password = "~/.ssh/school"


def do_deploy(archive_path):
    """ function that distributes the archive to my web-servers """
    # Checking if the file at the path archive_path doesn’t exist
    if not os.path.exists(archive_path):
        return False
    else:
        # Uploading the archive to the /tmp/ directory of the web server
        with lcd("/tmp"):
            put(archive_path)
        """ Uncompressing the archive to the folder on the web server """
        # Getting only the file from the path
        filename = os.path.basename(archive_path)

        # Opening the file and extracting it to the desired folder
        file = tarfile.open(filename)
        file.extractall("/data/web_static/releases/the_archive")

        # Joining path and deleting the archive from the web server
        complete_path = os.path.join("/tmp", archive_path)
        local("rm -rf complete_path")

        # Deleting the symbolic link from the server
        local("unlink /data/web_static/current")

        # Creating the new symbolic Link
        local("ln -s /data/web_static/current \
        data/web_static/releases/the_archive")

        return True
