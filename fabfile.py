import os.path
import fabric.utils as utils
from fake.api import (
    settings, task, execute, run as rrun, local as lrun,
    env, paths, cd, put, after
)
from fake.tasks.deploy import *


#import paramiko
#paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)


class FabricException(Exception):
    pass


current_path = os.path.dirname(__file__)
name = 'c19trace'

if 'local'  in env.roles:
    run = lrun
else:
    run = rrun

env.roledefs = {
    'prod': {
        'hosts': ['c19trace.org'],
        'user': 'admin',
        'service_user': 'www-data',
        'branch': 'master',
        'repo_url': 'git+ssh://git@github.com/fbuccioni/{0}'.format(name),
        'key_filename': current_path + '/automation/ssh.key',
        'deploy_path': '/hosting/app/{0}'.format(name),
        'use_ssh_config': True,
        'settings_module': 'aws'
    },
    'dev': {
        'hosts': ['c19trace.org'],
        'user': 'admin',
        'service_user': 'www-data',
        'branch': 'v2',
        'repo_url': 'git+ssh://git@github.com/fbuccioni/{0}'.format(name),
        'key_filename': current_path + '/automation/ssh.key',
        'deploy_path': '/hosting/app/{0}-dev'.format(name),
        'use_ssh_config': True,
        'settings_module': 'dev'
    },
    'local': {
        'hosts': ['localhost'],
        'dir': '/'
    }
}


@task
def install_ssh_key():
    """
        Installs ssh public key from `key_filename` env into authorized_keys file 
    """

    with open(env.key_filename + '.pub', 'r') as ssh_key_fp:
        ssh_public_key = ssh_key_fp.readline().strip("\n\r ")
        ssh_key_fp.close()

    abort_msg = None

    utils.puts("Checking previous installation...")
    with settings(abort_exception=FabricException):
        try:
            run(
                '! grep \"{0}\" ~/.ssh/authorized_keys > /dev/null'.format(
                    ssh_public_key.replace('"', '\\\\"')                    
                )
            )
        except(FabricException):
            abort_msg = "Public key is already installed on authorized_keys file"

    if abort_msg:
        utils.abort(abort_msg)

    run("[ ! -d ~/.ssh ] && mkdir ~/.ssh || true")
    run("echo \"{0}\" >> ~/.ssh/authorized_keys ".format(
        ssh_public_key.replace('"', '\\\\"')
    ))


@task
def install_git_ssh():
    """
        Installs ssh kit for git (automation/ssh.key)
    """
    abort_msg = None

    utils.puts("Checking previous installation...")
    with settings(abort_exception=FabricException):
        try:
            run('[ ! -f ~/.ssh/git.dev.key ]')
        except(FabricException):
            abort_msg = "git.dev.key already exists"

    if abort_msg:
        utils.abort(abort_msg)
    
    utils.puts("Copying key...")
    put(current_path + '/automation/ssh.key', '~/.ssh/git.dev.key')
    
    with open(current_path + '/automation/ssh.git.conf', 'r') as ssh_conf_fp:
        ssh_git_conf = ssh_conf_fp.read()
        ssh_conf_fp.close()

    utils.puts("Adding conf to user ssh config file...")
    run("echo \"{0}\" >> ~/.ssh/config ".format(
        ssh_git_conf.replace('"', '\\\\"')
    ))

    utils.puts("Enforce permissions for user ssh config file and key...")
    run("chmod 600 ~/.ssh/config")
    run("chmod 600 ~/.ssh/git.dev.key")

    utils.puts("Adding github.com to known_hosts")
    run(
        "(host=github.com; ssh-keyscan -H $host; " +
        "for ip in $(dig github.com +short); do " +
        "ssh-keyscan -H $host,$ip; " +
        "ssh-keyscan -H $ip; " +
        "done) 2> /dev/null >> ~/.ssh/known_hosts"
    )


@task 
def install_ssh_kit():
    """
        Install the whole ssh kit (key + git config)
    """

    tasks = (
        'install_git_ssh', 'install_ssh_key'
    )

    for task in tasks:
        execute(task, host=env.host)


@task
def starting():
    """
    Start a deployment, make sure server(s) ready.
    """

    if "local" in env.roles:
        utils.abort("Cannot run deploy in local role")

    abort_msg = None

    utils.puts("Check server packages...")
    with settings(abort_exception=FabricException):
        try:
            run('which python3 > /dev/null 2>&1')
        except(FabricException):
            abort_msg = "Python 3 must be installed"

        try:
            run('which virtualenv > /dev/null 2>&1')
        except(FabricException):
            abort_msg = "virtualenv for python must be installed"

    if abort_msg:
        utils.abort(abort_msg)

    execute('check', host=env.host)
    execute('set_previous_revision', host=env.host)


@task
def deploy_dir_perms():
    """
    Add permissions to the service user and the app user using `setfacl` Linux command
    """
    utils.puts("Setting owner as {0}".format(env.user))
    run("chown -R {1} {0}".format(env.deploy_path, env.user))

    utils.puts("Setting default ACLs on dirs")
    run("find \"{0}\" -type d -exec setfacl -d -m 'u:{1}:rwx' -m 'u:{2}:rwx' '{}' ';'".format(
        env.deploy_path, env.service_user, env.user
    ))

    utils.puts("Setting ACLs on dirs")
    run("find \"{0}\" -type d -exec setfacl -m 'u:{1}:rwx' -m 'u:{2}:rwx' '{}' ';'".format(
        env.deploy_path, env.service_user, env.user
    ))

    utils.puts("Setting ACLs on files")
    run("find \"{0}\" -type f -exec setfacl -m 'u:{1}:rw' -m 'u:{2}:rw' '{}' ';'".format(
        env.deploy_path, env.service_user, env.user
    ))


@task
def install_dotenv():
    """
    Copy the dotenv file int the root application directory to current app files directory
    """
    run("[ -f \"{0}/dotenv\" ] && cp -v \"{0}/dotenv\" \"{0}/current/.env\"".format(
        env.deploy_path
    ))

@task
def published():
    """
        Published
    """

    execute('log_dir_permissions', host=env.host)
    execute('deploy_virtualenv', host=env.host)
    execute('install_dotenv', host=env.host)
    execute('deploy_staticfiles', host=env.host)
    execute('migrate_database', host=env.host)
    execute('create_run_dir', host=env.host)


@task
def deploy_virtualenv():
    """
    Create the virtualenv inside the root project directory
    """

    utils.puts("Checking virtualenv...")

    abort_msg = None

    with settings(abort_exception=FabricException):
        try:
            run('which virtualenv > /dev/null 2>&1')
        except(FabricException):
            abort_msg = "python-virtualenv must be installed"

    if abort_msg:
        utils.abort(abort_msg)

    # TODO: remove diffs on requirements.txt
    run(
        (
            "[ -f \"{0}/virtualenv/bin/activate\" ]  || " +
            "virtualenv -p $(which python3) --prompt='({1}) ' \"{0}/virtualenv\""
        ).format(env.deploy_path, name)
    )

    utils.puts("Installing from requirements.txt...")
    run(
        (
            "source {0}/virtualenv/bin/activate && " +
            "pip install -r {0}/current/automation/requirements.txt"
        ).format(env.deploy_path)
    )


@task
def create_run_dir():
    """
    Create a `run` directory inside the project root for the socket and pid files
    """
    utils.puts("Creating run dir...")

    abort_msg = None

    with settings(abort_exception=FabricException):
        try:
            run('which setfacl > /dev/null 2>&1')
        except(FabricException):
            abort_msg = "This conf uses POSIX acl setfacl command"

    if abort_msg:
        utils.abort(abort_msg)

    # TODO: remove diffs on requirements.txt
    run_dir = env.deploy_path + '/run'

    run("[ -d \"{0}\" ] || mkdir \"{0}\" ".format(run_dir))
    run("setfacl -m 'u:{1}:rwx' \"{0}\"".format(run_dir, env.service_user))
    run("setfacl -n -m 'm::rwx' \"{0}\"".format(run_dir))
    run("setfacl -d -m 'u:{1}:rwx' \"{0}\"".format(run_dir, env.service_user))
    run("setfacl -d -n -m 'm::rwx' \"{0}\"".format(run_dir))


@task
def log_dir_permissions():
    """
    Makes a log path in the current app files
    """
    log_dir = env.deploy_path + '/current/log'

    run("setfacl -m 'u:{1}:rwx' \"{0}\"".format(log_dir, env.service_user))
    run("setfacl -d -m 'u:{1}:rwx' \"{0}\"".format(log_dir, env.service_user))


@task
def finished():
    """
        Published
    """

    execute('restart', host=env.host)


@task
def restart():
    """
    Restart service (This case `uwsgi` using `sudo`)
    """
    utils.puts("Restarting...")
    run("sudo service uwsgi restart")


@task
def deploy_staticfiles():
    """
    Deploy django static files in the server
    """
    utils.puts("Collecting static files...")
    run(
        (
            "source {0}/virtualenv/bin/activate && "
            "DJANGO_SETTINGS_MODULE=settings.env.{1} "
            "python {0}/current/manage.py collectstatic --noinput -l"
        ).format(env.deploy_path, env.settings_module)
    )


@task
def migrate_database():
    """
    Apply django database migrations in the server
    """
    utils.puts("Migrating database...")
    run(
        (
            "source {0}/virtualenv/bin/activate && "
            "DJANGO_SETTINGS_MODULE=settings.env.{1} "
            "python {0}/current/manage.py migrate"
        ).format(env.deploy_path, env.settings_module)
    )


@task
def copy_envfile(*args):
    """
    Copy dotenv file arg to the main app directory as dotenv
    """

    if len(args):
        utils.puts("Copying envfile...")
        put(args[0], "{0}/dotenv".format(env.deploy_path) )
    else:
        utils.abort("Usage: fab copy_envfile:path.env.file")