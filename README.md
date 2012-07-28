Overview
========

*TL;DR:* This CPython extension provides a Python binding for _cracklib_ (C
language) library.

It provides a _crack_ Python module that exposes a simple interface to check the
strength of passwords. This can be used from within Python programs as easily as
calling a function and catching an exception.

_crack_ can be very severe in performing checks. It uses the standard
_cracklib2_ library to discover whether passwords are based on dictionary words
or are too simple. Moreover additional checks such as minimum difference
characters and rotation of old password have been written on the model of those
found in PAM _cracklib_ module.


Installation
============

Installing _crack_ is simple with pip:

~~~
$ pip install git@github.com:jexhson/python-crack.git --install-option='--dictpath=/path/to/dict'
~~~

or, directly from the source by running the installation script:

~~~
$ python setup.py install --dictpath=/path/to/dict
~~~

`--dictpath` specify the default dictionary crack will be using to perform it
check. If none specified, make sure to specify one each time you call crack.

Dictionary have to be packed as follow:

~~~
cracklib-packer my-cracklib-dict < my-plain-dict.txt
~~~

Three files where generated: `my-cracklib-dict.hwm` `my-cracklib-dict.pwd` `my-cracklib-dict.pwi`
`--dictpath` should be here _my-cracklib-dict_


Examples
========

```python
>>> import crack
>>> crack.FascistCheck("abcdefghilmn")
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
  File "/usr/lib/python2.2/site-packages/crack.py", line 194, in VeryFascistCheck
    return FascistCheck(new, dictpath)
ValueError: it is too simplistic/systematic
>>> crack.FascistCheck("secret")
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
ValueError: it is based on a dictionary word
>>> crack.VeryFascistCheck("secret", "scrt")
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
  File "/usr/lib/python2.2/site-packages/crack.py", line 187, in VeryFascistCheck
    raise ValueError, "is too similar to the old one"
ValueError: is too similar to the old one
>>> crack.VeryFascistCheck("secret", "cretse")
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
  File "/usr/lib/python2.2/site-packages/crack.py", line 185, in VeryFascistCheck
    raise ValueError, "is rotated"
ValueError: is rotated
>>> crack.FascistCheck("this is a really secure secret but do not use it!!")
'this is a really secure secret but do not use it!!'
```

Documentation
=============

The two main functions are `FascistCheck` and `VeryFascistCheck`. The example
above show the usage. If you want more information or more configuration
parameters please refer to the documented source code `crack.py`.


Why Use crack?
==============

Passwords are the most common way a computer uses to authenticate the user. The
key point is in the little possibility for any user to guess other users'
passwords and then use their identities. Sadly nowadays this often shows to be
also the weakest ring of the whole security chain.

Reducing the possibility of password guessing and then improving passwords'
strength can greatly improve the overall system security.

_crack_ and _cracklib_ have been written for this purpose: mandate the use of
stronger passwords. Whether these passwords are strong enough for his purpose is
solely a matter of the user.


Security consideration
======================

Beware of a little, tiny particular. Python does not allow direct memory
management.

Python objects, and then strings and passwords, are garbage collected
automatically. There is no way (known to the author) to clean passwords safely.
So might happen that other programs are able to see the left passwords in they
dirty (not initialized) memory.

If the user cannot live with this limitation, he is better to change module or
language.


Authors
=======

Originally written by Domenico Andreoli <cavok@filibusta.crema.unimi.it>

Small improvements, updates and packaging by Alexandre Joseph
<http://www.alexandrejoseph.com>

License
=======

_python-crack_ is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

_python-crack_ is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
