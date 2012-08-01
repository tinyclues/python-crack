# python-crack - CPython libcrack wrapper
#
# Copyright (C) 2003 Domenico Andreoli
# Copyright (C) 2012 Alexandre Joseph
#
# This file is part of python-crack.
#
# python-crack is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# python-crack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
from os.path import isfile
from distutils.core import setup, Extension


# Know a more elegant way to add parameters to distutils?
def get_dict_path():
    dictpath = ''
    if '--dictpath' in sys.argv:
        dictpath_arg_pos = sys.argv.index('--dictpath')
        if len(sys.argv) - 1 == dictpath_arg_pos:
            sys.exit('Invalid value for --dictpath')
        sys.argv.pop(dictpath_arg_pos)
        dictpath = sys.argv.pop(dictpath_arg_pos)
    else:
        dictpath_arg = [d for d in sys.argv if d.startswith('--dictpath=')]
        if dictpath_arg:
            sys.argv.remove(dictpath_arg[0])
            dictpath = dictpath_arg[0].split('=', 1)[1]
    if not dictpath:
        print('WARNING: No default dictionary specified.' +
              'Use --dictpath to specify one')
    elif not any([isfile('%s.%s' % (dictpath, ext))
                for ext in ('hwm', 'pwd', 'pwi')]):
        print('WARNING: Dictionary is not packed correctly, ' +
              'not able to find one of %s.(hwm|pwd|pwi)' % dictpath)
    return dictpath


modules = [
    Extension(
        '_crack',
        sources=['crack.c'],
        libraries=['crack'],
        define_macros=[('DICTPATH', '"%s"' % get_dict_path())],
    )
]

setup(name='python-crack',
      version='0.6.1',
      description='CPython libcrack wrapper',
      author='Alexandre Joseph',
      url='https://github.com/jexhson/python-crack',
      license='GPLv2+',
      py_modules=['crack'],
      ext_modules=modules,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Unix',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      long_description='''\
python-crack is a CPython extension providing a Python binding for cracklib
library. It provides a crack python module that exposes a simple interface to
check the strength of passwords. This can be used from within Python programs
as easily as calling a function and catching an exception.

crack can be very severe in performing checks. It uses the standard cracklib2
library to discover whether passwords are based on dictionary words or are too
simple. Moreover additional checks such as minimum difference characters and
rotation of old password have been written on the model of those found in PAM
cracklib module.
''')
