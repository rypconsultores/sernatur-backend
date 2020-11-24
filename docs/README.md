Documentation
=============


Sphinx
-------

The docs are developed with [Sphinx](http://sphinx-doc.org) and the python
requirementa are included in the file 
[requirements-docs.txt]`../automation/requirements-docs.txt`

To install this dependencies use pip, in the root of the project run:

    pip install -r automation/requirements-docs.txt


Sphinx Configuration
--------------------

The main configuration file is `/docs/conf.py`, in the top of this files it 
includes and starts the django application to read properly the docstrings and
default values  

**A good point to start the docs is replacing `django-skeretonu` for the name
of the project and `Felipe Buccioni` for the name of the author and delete
this paragraph**
 

Directory structure
-------------------

- `/docs/rst` - Main docs
- `/docs/.doctrees` - Doctrees
- `/docs/static` - Static files
- `/docs/{format}` - Build dirs, format can be (html, dirhtml, lates, etc.) 


Generate
--------

To generate docs, is necessary to initialize the django app, this means create 
the symlink `settings/env/default.py` or use `DJANGO_SETTINGS_MODULE` environment
variable.

There are several formats to create docs provided by Sphinx, you can see it
with the following command:

    docs/make help

The format `dirhtml` will be used to online docs, and `html` for personal
docs, we can compile just one format:

    docs/make html

Or more formats in one command:

    docs/make html dirhtml latexpdf

The docs will be in `docs/{format}` subfolder. 
