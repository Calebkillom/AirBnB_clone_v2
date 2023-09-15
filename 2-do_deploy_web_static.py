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
    # Check if the archive file exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Getting the base name of the archive
        archive_name = os.path.basename(archive_path)

        # Uploading the archive to the remote server's /tmp/ directory
        put(archive_path, "/tmp/{}.tgz".format(archive_name))

        # Extracting the archive to the desired folder without .tgz extension
        release_folder = "/data/web_static/releases/{}/".format(archive_name)
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{}.tgz -C {}".format(archive_name, release_folder))

        # Delete the archive with .tgz extension from the server
        run("rm /tmp/{}.tgz".format(archive_name))

        # Move files from extracted subdirectory to release folder
        extracted_folder = "{}web_static".format(release_folder)
        run("mv {}/* {}".format(extracted_folder, release_folder))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_folder))

        # Print the "New version deployed!" message
        print("New version deployed!")

        # Return True on successful deployment
        return True
    except Exception as e:
        # Handle any exceptions and return False
        print("Error: {}".format(e))
        return False
