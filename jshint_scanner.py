#!/usr/bin/env python
"""
2016.2.26 CKS
Wrapper around jshint to scan JS files for syntax errors.

To run, first install the necessary system packages via:

    sudo apt-get install nodejs nodejs-legacy npm

then install jshint:

    sudo npm install -g jshint
    
then the script can be run to scan all HTML and JS files via:

    ./jshint_scanner.py
    
"""
from __future__ import print_function
import os
import sys
import fnmatch
import re
import tempfile

try:
    # Python 2 only
    import commands
except ImportError:
    
    # Python 2 and 3
    from future import standard_library
    standard_library.install_aliases()
    import subprocess as commands
    
from contextlib import closing

HTML_PAT = '*.html'
JS_PAT = '*.js'
SCRIPT_REGEX = re.compile(r'<script[^>]+>(.*?)</script>', flags=re.DOTALL|re.I)#

sample_html_good = '''
<html> 
  <head> 
    <title>Regular Expression HOWTO &mdash; Python v2.7.1 documentation</title> 
    <script type="text/javascript"> 
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    '../',
        VERSION:     '2.7.1',
        COLLAPSE_MODINDEX: false,
        FILE_SUFFIX: '.html',
        HAS_SOURCE:  true
      };
    </script> 
    <script type="text/javascript" src="../_static/jquery.js"></script>
  </head>
</html>
'''

sample_html_bad = '''
<html> 
  <head> 
    <title>Regular Expression HOWTO &mdash; Python v2.7.1 documentation</title> 
    <script type="text/javascript"> 
      var DOCUMENTATION_OPTIONS ={
        URL_ROOT:    '../'
        VERSION:     '2.7.1',
        COLLAPSE_MODINDEX: false,
        FILE_SUFFIX '.html',
        HAS_SOURCE:  true
      }
    </script> 
    <script type="text/javascript" src="../_static/jquery.js"></script>
  </head>
</html>
'''

def check_js(verbose=False, template_patterns=None, files=None, config=None):
    
    files = files or []
    
    template_patterns = template_patterns or [HTML_PAT]#, JS_PAT]
    
    error_files = set()
    files_checked = 0
    
    if config:
        assert os.path.isfile(config), 'Configuration file %s does not exist.' % config
        cmd = 'jshint --config=jshint.rc %s'
    else:
        cmd = 'jshint %s'
    
    def iter_files():
        if files:
            for filename in files:
                yield filename
        else:       
            for root, dirnames, filenames in os.walk(os.getcwd()):
                for template_pattern in template_patterns:
                    for filename in fnmatch.filter(filenames, template_pattern):
                        yield os.path.join(root, filename)
    
    for fqfn in iter_files():
        filename = os.path.split(fqfn)[-1]
        full_content = open(fqfn).read()
        js_chunks = [
            _.strip()
            for _ in SCRIPT_REGEX.findall(full_content)
            if _.strip()
        ]
        if js_chunks:
            print('Checking %s...' % fqfn)
            for chunk in js_chunks:
                
                chunk_line_start = full_content.find(chunk)
                prior_lines = full_content[:chunk_line_start].count('\n')
                
                # Remove Django template notation.
                chunk = re.sub(r'{%.*?%}', '', chunk)
                chunk = re.sub(r'{{.*?}}', '', chunk)
                chunk = re.sub(r'{#.*?#}', '', chunk)
                
                fd, fn = tempfile.mkstemp()
                with closing(os.fdopen(fd, 'w')) as fout:
                    fout.write(chunk)
                
                ret_code, output = commands.getstatusoutput(cmd % fn)
                files_checked += 1
                os.remove(fn)
                if ret_code:
                    line_matches = re.findall(r' line ([0-9]+),', output)
                    output = output.replace(fn, filename)
                    for line_number in line_matches:
                        line_number = int(line_number)
                        new_line_number = prior_lines + line_number
                        output = output.replace(' line %i,' % line_number, ' line %i,' % new_line_number)
                        
                    error_files.add(fqfn)
                    print('Found errors in %s!\n\n%s' % (fqfn, output), file=sys.stderr)
                    
    print('-'*80)
    print('%i files checked' % files_checked)
    print('%i files with errors found' % len(error_files))
    
    return files_checked, error_files
                        
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Scan Javascript with Jshint.')
    parser.add_argument('files', nargs='+',
        help='a list of explicit files to check')
    parser.add_argument('--verbose', action='store_true',
        default=False,
        help='if given, outputs debugging info')
    parser.add_argument('--config',
        default=None,
        help='path to jshint config file')
                       
    check_js(**parser.parse_args().__dict__)
    