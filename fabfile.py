#
# Used to easily deploy code to the production server
#
# INSTALL fabric ON YOUR LOCAL MACHINE
# i.e. sudo easy_install fabric
#
from fabric.api import *

env.hosts=['cinepy.com']

def deploy():
    project_dir = '/www/cinepy'
    with cd(project_dir):
        run("sudo git pull origin master")
        run("sudo supervisorctl restart cinepy-8000")
        run("sudo supervisorctl restart cinepy-8001")
        run("sudo chown -R www-data:www-data %s" % project_dir)
        run("sudo chmod 770 %s" % project_dir)

