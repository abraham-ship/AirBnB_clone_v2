#!/usr/bin/python3
"""Python fabric that manages archives for web servers"""

from fabric.api import env, local, run
from os.path import exists
from datetime import datetime

env.hosts = ['35.174.211.53', '54.209.215.209']
env.user = 'ubuntu'


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


def do_deploy(archive_path):
    '''Distributes an archive to a web server.'''
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_extension = archive_filename.split('.')[0]
        remote_tmp_archive = "/tmp/{}".format(archive_filename)
        remote_release_dir = "/data/web_static/releases/{}/".\
            format(archive_no_extension)

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp")

        # Uncompress the archive to the /data/web_static/releases/ directory
        run("mkdir -p {}".format(remote_release_dir))
        run("tar -xzf {} -C {}".format(remote_tmp_archive, remote_release_dir))

        # Delete the archive from the web server
        run("rm {}".format(remote_tmp_archive))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s {} /data/web_static/current".format(remote_release_dir))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False


def deploy():
    """Deploy the web_static content to the web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
