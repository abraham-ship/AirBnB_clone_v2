#!/usr/bin/python3

'''distribute an archive on web servers'''
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
import os


def do_deploy(archive_path):
    """Deploy the web_static archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on both servers
        put(archive_path, '/tmp/')

        # Uncompress archive to /data/web_static/current/ directory
        filename = os.path.basename(archive_path).split('.')[0]
        release_path = '/data/web_static/releases/{}'.format(filename)
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{}.tgz -C {}'.format(filename, release_path))

        # Remove the archive from the server
        run('rm -rf /tmp/{}.tgz'.format(filename))

        run("mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/".format(name, name))

        run("rm -rf /data/web_static/releases/{}/web_static/".format(name))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
