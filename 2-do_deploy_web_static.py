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

        # Upload the archive to the remote server's /tmp/ directory
        put(archive_path, "/tmp/{}".format(archive_name))

        # Extracting the archive to the /data/web_static/releases/ directory
        release_folder = "/data/web_static/releases/"
        run("mkdir -p {}/{}"
            .format(release_folder.rstrip('/'), archive_name[:-4]))
        run("tar -xzf /tmp/{} -C {}{}"
            .format(archive_name, release_folder, archive_name[:-4]))

        # Delete the archive from the server
        run("rm /tmp/{}".format(archive_name))

        # Create a new folder for the release without the extra slash
        new_release_folder = "{}/{}".format(release_folder.rstrip('/'), archive_name[:-4])

        # Use the shell argument to allow wildcard expansion
        run("mv {}/web_static/* {}/"
            .format(release_folder.rstrip('/'), \
                    new_release_folder), shell=True)


        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(new_release_folder))

        # Print the "New version deployed!" message
        print("New version deployed!")

        # Return True on successful deployment
        return True
    except Exception as e:
        # Handle any exceptions and return False
        print("Error: {}".format(e))
        return False
