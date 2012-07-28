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

from _crack import FascistCheck, default_dictpath

digits = '0123456789'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'

diff_ok = 5
min_length = 9
dig_credit = 1
up_credit = 1
low_credit = 1
oth_credit = 1


def palindrome(s):
    '''
    Check if the string s is a palindrome
    '''
    for i in xrange(len(s)):
        if s[i] != s[-i - 1]:
            return 0
    return 1


def distdifferent(old, new, i, j):
    if i == 0 or len(old) <= i:
        c = 0
    else:
        c = old[i - 1]

    if j == 0 or len(new) <= i:
        d = 0
    else:
        d = new[j - 1]

    return c != d


def distcalculate(distances, old, new, i, j):
    tmp = 0

    if distances[i][j] != -1:
        return distances[i][j]

    tmp = distcalculate(distances, old, new, i - 1, j - 1)
    tmp = min(tmp, distcalculate(distances, old, new, i, j - 1))
    tmp = min(tmp, distcalculate(distances, old, new, i - 1, j))
    tmp = tmp + distdifferent(old, new, i, j)

    distances[i][j] = tmp

    return tmp


def distance(old, new):
    '''
    Calculate how different two strings are in terms of the number of
    character removals, additions, and changes needed to go from one to
    the other
    '''
    m = len(old)
    n = len(new)

    distances = [[] for i in xrange(m + 1)]
    for i in xrange(m + 1):
        distances[i] = [-1 for j in xrange(n + 1)]

    for i in xrange(m + 1):
        distances[i][0] = i
    for j in xrange(n + 1):
        distances[0][j] = j
    distances[0][0] = 0

    r = distcalculate(distances, old, new, m, n)

    for i in xrange(len(distances)):
        for j in xrange(len(distances[i])):
            distances[i][j] = 0

    return r


def similar(old, new):
    '''
    Determines if two passwords are similar by calculate if 1/2 of the
    characters in the new password are different from the old one or if the
    distance between them is acceptable

    Accepted distance difference is defined by :diff_ok, the number of
    characters in the new password that must not be present in the old
    password.
    '''
    if len(new) >= (len(old) * 2):
        return 0

    if distance(old, new) >= diff_ok:
        return 0

    # passwords are too similar
    return 1


def simple(new):
    '''
    Check that the password is not too simple and follow some criteria.

    A minimum acceptable size is required (:min_length) for the new password
    (plus one if credits are not disabled which is the default). In addition
    to the number of characters in the new password, credit (of +1 in length)
    is given for each different kind of character (digit, upper, lower and
    other).

    To set the minimum number of a character type that must be met for a new
    password, credit of this type must be negative.

    The default minimum length is 9 which is good for a old style Unix
    password all of the same type of character but may be too low to exploit
    the added security of a md5 system.

    Note that there is a pair of length limits in cracklib itself, a "way too
    short" limit of 4 which is hard coded in and a defined limit of 6 that
    will be checked without reference to min_length. If you want to allow
    passwords as short as 5 characters you should either not use this module
    or recompile the crack library and then recompile this module.
    '''
    digits = 0
    uppers = 0
    lowers = 0
    others = 0

    for c in new:
        if c in digits:
            digits = digits + 1
        elif c in ascii_uppercase:
            uppers = uppers + 1
        elif c in ascii_lowercase:
            lowers = lowers + 1
        else:
            others = others + 1

    if digits > dig_credit:
        digits = dig_credit

    if uppers > up_credit:
        uppers = up_credit

    if lowers > low_credit:
        lowers = low_credit

    if others > oth_credit:
        others = oth_credit

    size = min_length

    if dig_credit >= 0:
        size -= digits
    elif digits < -dig_credit:
        return 1

    if up_credit >= 0:
        size -= uppers
    elif uppers < -up_credit:
        return 1

    if low_credit >= 0:
        size -= lowers
    elif lowers < -low_credit:
        return 1

    if oth_credit >= 0:
        size -= others
    elif others < -oth_credit:
        return 1

    if len(new) < size:
        return 1

    return 0


def VeryFascistCheck(new, old=None, dictpath=None):
    '''
    Behaves like FascistCheck but performs also checks for palindrome and
    simple passwords.

    If the optional old_password is provided additional checks for minimum
    distance between the two passwords, for similarity, for change of case
    only and for rotation are performed.

    Exception ValueError is raised in case of weak password.

    dictpath parameter is used only for the inner call to FascistCheck, hence
    it has the same signification it has for FascistCheck.
    '''
    if dictpath == None:
        dictpath = default_dictpath

    if old != None:
        if new == old:
            raise ValueError('is the same as the old one')

        oldmono = old.lower()
        newmono = new.lower()
        wrapped = old + old

        if newmono == oldmono:
            raise ValueError('case changes only')
        if wrapped.find(new) != -1:
            raise ValueError('is rotated')
        if similar(oldmono, newmono):
            raise ValueError('is too similar to the old one')

    FascistCheck(new, dictpath)

    if palindrome(new):
        raise ValueError('is a palindrome')
    if simple(new):
        raise ValueError('is too simple')

    return new
