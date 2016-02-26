from __future__ import print_function
import os
import unittest
import tempfile
from contextlib import closing

import jshint_scanner

class Tests(unittest.TestCase):
    
    def test_scan(self):
        
        files = []

        fd, fn1 = tempfile.mkstemp()
        with closing(os.fdopen(fd, 'w')) as fout:
            fout.write(jshint_scanner.sample_html_bad)
        files.append(fn1)
        
        fd, fn2 = tempfile.mkstemp()
        with closing(os.fdopen(fd, 'w')) as fout:
            fout.write(jshint_scanner.sample_html_good)
        files.append(fn2)
            
        files_checked, error_files = jshint_scanner.check_js(
            verbose=True,
            files=files,
            template_patterns=['*'])
        print('ret:', files_checked, error_files)
        self.assertEqual(files_checked, 2)
        self.assertEqual(len(error_files), 1)
        
        for _fn in files:
            os.remove(_fn)
        
if __name__ == '__main__':
    unittest.main()
