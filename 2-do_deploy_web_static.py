#!/usr/bin/python3
# Fabric Script that distributes an archive to my web-servers
# Using the do_deploy function

import os
from fabric.api import *
from sys import argv


# Executing remote commands on both of my web servers
env.hosts = ["34.229.189.80", "18.204.11.87"]

# Setting the username to my servers
env.user = argv[-1]

# Setting the password to my servers
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """Function that distributes the archive to web servers"""

    if not os.path.exists(archive_path):
        return False

    # Getting the base name of the archive without the file extension
    archive_name = os.path.splitext(os.path.basename(archive_path))[0]

    # Uploading the archive to the remote server's /tmp/ directory
    put(archive_path, "/tmp/{}.tgz".format(archive_name))

    # Extracting the archive to the desired folder
    release_path = "/data/web_static/releases/{}/".format(archive_name)
    run("mkdir -p {}".format(release_path))
    run("tar -xzf /tmp/{}.tgz -C {}".format(archive_name, release_path))

    # Deleting the archive from the server
    run("rm /tmp/{}.tgz".format(archive_name))

    # Move files from 'web_static' subdirectory to release folder
    run("mv {}/web_static/* {}/"
        .format(release_path.rstrip('/'), release_path.rstrip('/')))

    # Removing the 'web_static' subdirectory
    run("rm -rf {}/web_static".format(release_path))

    # Removing the old symbolic link
    run("rm -rf /data/web_static/current")

    # Creating a new symbolic link
    run("ln -s {} /data/web_static/current".format(release_path))

    # Printing the "New version deployed!" message
    print("New version deployed!")
