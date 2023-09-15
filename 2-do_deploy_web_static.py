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

    # Get the base name of the archive
    archive_name = os.path.basename(archive_path)

    # Upload the archive to the remote server's /tmp/ directory
    put(archive_path, "/tmp/{}".format(archive_name))

    # Extract the archive to the desired folder
    run("mkdir -p /data/web_static/releases/the_archive/")
    run("tar -xzf /tmp/{} -C /data/web_static/releases/the_archive/"
        .format(archive_name))

    # Delete the archive from the server
    run("rm /tmp/{}".format(archive_name))

    # Remove the old symbolic link
    run("rm -rf /data/web_static/current")

    # Create a new symbolic link
    run("ln -s /data/web_static/releases/the_archive/ \
        /data/web_static/current")

    return True
