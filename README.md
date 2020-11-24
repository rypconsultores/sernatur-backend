django-skeretonu
=================


A skeleton for django framework.


Create a project with `django-skeretonu`
---------------------------------------

Please rename `project-name` with your project folder name

```
curl -sL https://github.com/fbuccioni/django-skeretonu/tarball/master | tar -zxvf -; mv -v fbuccioni-django-skeretonu-[0-9]*[0-9] project-name
```


Why all those dirs at the root?
-------------------------------

The reason I chose to use the `settings` and `wsgi` directories outside
the app, is because I need to standarize projects with multiple apps
to make containers or different orchrestration and automation scripts 
without the dependency of _"a main application"_ to start the applications.

Because those dirs are in the root folder, I decided to use an `/apps` 
folder in the root to put all apps there and make the skeleton tidy.

Additionally I use the folder `/automation` for `requierements.txt` and 
some other automation stuff like ssh keys, `fabfile.py` scripts, other
scripts, etc.

How can configure this
-----------------------

There are 4 ways to configure:

1. By default uses `settings.env.default` module, the example of 
   `settings/env/default.py` is a simpy symlink to `local.py` (in the same
   directory)
2. The common use of `DJANGO_SETTINGS_MODULE` environment variable pointing 
   to your environment, an example can be `settings.env.prod 
3. Dotenv, the `manage.py` and the `wsgi/__init__.py` (the wsgi application
   in `wsgi` module) also read the `.env` file in the root
4. Environment Variables using `os.getenv`

In my personal experience, I use a module for the static configuration for
different environments and `os.getenv` for environment variables and depending
on the envoironment use raw environment variables, for example in a docker
container or `.env` if it's a deploy with `Fabric/fake`


`fabfile.py` Template for development and server tasks
------------------------------------------------------

The skeleton uses a Fabric template, but you need fake to use it, try to install globally
and not inside your virtualenv.

```
pip install fake
```


Fake provides a deploy capistrano-like tasks, check out the [Fabric GitHub](https://github.com/bmuller/fake) and additionally have the following commands

| Task                | Description
|---------------------|-------------------------------------------------------------
| `cleanup_rollback`    |  Remove and archive rolled-back release.
| `copy_envfile`        |  Copy dotenv file arg to the main app directory as dotenv
| `create_run_dir`      |  Create a `run` directory inside the project root for the socket and pid files
| `deploy_dir_perms`    |  Add permissions to the service user and the app user using `setfacl` Linux 
| `deploy_staticfiles`  |  Deploy django static files in the server
| `deploy_virtualenv`   |  Create the virtualenv inside the root project directory
| `finished`            |  Extended Fake task, executes `restart` job
| `install_dotenv`      |  Copy the dotenv file int the root application directory to current app files 
| `install_git_ssh`     |  Installs ssh kit for git (automation/ssh.key)
| `install_ssh_key`     |  Installs ssh public key from `key_filename` env into authorized_keys file 
| `install_ssh_kit`     |  Install the whole ssh kit (key + git config)
| `log_dir_permissions` |  Create a `log` directory in the current app files
| `migrate_database`    |  Apply django database migrations in the server
| `published`           |  Extended Fake task, executes `log_dir_permissions`, `deploy_virtualenv`, `install_dotenv`, `deploy_staticfiles`, `migrate_database`, `create_run_dir`
| `restart`             |  Restart service (This case `uwsgi` using `sudo`)
| `starting`            |  Start a deployment, make sure server(s) ready.
| `symlink_files`       |  Symlink linked files.
| `symlink_folders`     |  Symlink linked folders.


### Deploy

1. Add a development key to your git project
2. Save the key as `automation/ssh.key`
3. Install your public key in authorized_keys, maybe `fab -R env install_ssh_key` task can help.
4. Install the git key using `fab -R env install_git_ssh`
5. Create the application directory in the server
6. Create server app configurations, the example uses uwsgi in the task `restart` maybe you use another
7. Test it with `fab -R env deploy`
8. Check if errors
9. `goto 7 until works`


What is the `httpserver.py` file?
-----------------------------

The `httpserver.py` is a python script to run a 
[Tornado](http://www.tornadoweb.org) web server serving our Django project.

_**Note**_: If your project use static files, this script use static from 
`/static` folder, so you must run the  `collectstatic` django command 
before run this command.

_**Note**_: You must install the tornado python package before use this
script, this can be done via `pip` using the following command:

```
pip install tornado
```


### Usage:

```
python httpserver.py 9000
```

And the web server will be running in the port `9000`, the default host is
`0.0.0.0` binding the service to all ips. you can specify a host with `127.0.0.1:9000` argument.


Suggestions?
------------

All suggestions are always welcome, pleas feel free to ask in the issues
section of this repo.