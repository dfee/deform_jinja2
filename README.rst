deform_jinja2
===========

Jinja2 templates for deform using the uni-form model

The following is an example demonstrating deform_jinja2's three supported 
settings::

    deform_jinja2.i18n.domain=deform
    deform_jinja2.template_search_path=
        myapp:templates/forms
        deform_jinja2:bootstrap_templates
    deform_jinja2.filters =
        debug = myapp.filters.debug_filter
        route_url = pyramid_jinja2.filters:route_url_filter
        static_url = pyramid_jinja2.filters:static_url_filter
    
  These settings belong in your ``app.ini`` file

To run the `deformdemo <http://deformdemo.repoze.org>`_ application using the
``deform_jinja2`` renderer:

- Create a virtualenv::

    $ virtualenv2.6 --no-site-packages env

  Heretofore, the ``env`` directory created above will be referred to as
  $VENV

- Clone the deformdemo GitHub repository::

    $ git clone git://github.com/Pylons/deformdemo.git

- cd to the deformdemo checkout and ``setup.py develop`` it into your
  virtualenv

    $ cd deformdemo
    $ $VENV/bin/python setup.py develop

- Use the deform_jinja2 ``demo.ini`` file to run a demo app server via ``paster
  serve``:

    $ $VENV/bin/paster demo.ini

- The demo app will be running on port 8521.  See the ``README.rst`` in the
  deformdemo checkout for instructions about how to run the selenium tests.

