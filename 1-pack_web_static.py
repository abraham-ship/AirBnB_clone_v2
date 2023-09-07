#!/usr/bin/python3

'''generate .tgz archive from web_static folder'''
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Compress the contents of the web_static folder into a .tgz archive.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        if not os.path.exists("versions"):
            os.makedirs("versions")

        print(f"Packing web_static to {archive_path}")
        tar_command = "tar -cvzf {} web_static".format(archive_path)
        result = local(tar_command, capture=True)

        print(result)

        if os.path.exists(archive_path):
            print(f"web_static packed: {archive_path} ->\
                  {os.path.getsize(archive_path)}Bytes")
            return archive_path
        else:
            return None
    except Exception as e:
        return None
