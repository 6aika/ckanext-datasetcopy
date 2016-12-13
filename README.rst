=============
ckanext-datasetcopy
=============

Adds an option to copy an existing dataset as a template for a new dataset. Enabling the plugin adds a "copy"-button
into the dataset edit view.


------------
Requirements
------------

Tested with CKAN v2.6, but should work fine with older 2.x versions.


------------
Installation
------------

To install ckanext-datasetcopy:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-datasetcopy Python package into your virtual environment::

     pip install ckanext-datasetcopy

3. Add ``datasetcopy`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


------------------------
Development Installation
------------------------

To install ckanext-datasetcopy for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/6aika/ckanext-datasetcopy.git
    cd ckanext-datasetcopy
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

No tests implemented yet. Feel free to submit a pull request.
