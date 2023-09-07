#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['35.174.211.53', '54.209.215.209']
env.user = 'ubuntu'

def do_deploy(archive_path):
    '''Distributes an archive to a web server.'''
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_extension = archive_filename.split('.')[0]
        remote_tmp_archive = "/tmp/{}".format(archive_filename)
        remote_release_dir = "/data/web_static/releases/{}/".format(archive_no_extension)

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, remote_tmp_archive)

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
