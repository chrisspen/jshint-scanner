from distutils.core import setup

VERSION = (1, 0, 0)
__version__ = '.'.join(map(str, VERSION))

setup(name='jshint-scanner',
    version=__version__,
    description='Extracts Javascript from files and scans with Jshint.',
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='https://github.com/chrisspen/jshint-scanner',
    license='MIT License',
    py_modules=['jshint_scanner'],
    scripts=['jshint_scanner.py'],
    install_requires=open('pip-requirements.txt').readlines(),
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
    ],
    platforms=['OS Independent'],)
