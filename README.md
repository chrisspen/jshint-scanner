Jshint-Scanner 
=============================================================================

Overview
--------

Extract Javascript from documents and scan with [JSHint](http://jshint.com/).

Installation
------------

    pip install jshint-scanner

Usage
-----

To recursively scan all files in the current working directory, simply run:

    jshint_scanner.py

To scan a specific file, run:

    jshint_scanner.py /path/to/file

Development
-----------

To run all unittests:

    rm -Rf .tox; tox

To run all unittests in a specific Python version:

    tox -e py27
    
To run a specific unittest:

    tox -- Tests.test_scan
