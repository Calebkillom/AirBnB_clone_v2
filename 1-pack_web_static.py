#!/usr/bin/python3
# Fabric script that generates a .tgz archive
# from the contents of the web_static folder of my AirBnB Clone repo

from fabric.api import local, lcd
from datetime import datetime


def do_pack():
    #  returning the archive path if the archive has been correctly generated
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Generate the timestamp
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the archive filename
    archive_name = "web_static_{}.tgz".format(current_time)

    """
    Changing the local working directory to
    web_static before creating the archive
    """
    with lcd("web_static"):
        # Create the command to generate the archive
        command = "tar -czvf ../versions/{} .".format(archive_name)

        # Run the command and capture the output
        result = local(command)

    # Check if the command was successful
    if result.failed:
        return None

    # Return the path to the archive file
    return "versions/{}".format(archive_name)
