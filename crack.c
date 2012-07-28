/* python-crack - CPython libcrack wrapper
 *
 * Copyright (C) 2003 Domenico Andreoli
 * Copyright (C) 2012 Alexandre Joseph
 *
 * This file is part of python-crack.
 *
 * python-crack is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * python-crack is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */

#include <Python.h>
#include <crack.h>
#include <fcntl.h>

#define FILENAME_MAXLEN 512

static char const DEFAULT_DICTPATH[] = DICTPATH;

static char _crack_FascistCheck_doc [] =
  "Maps the homonym cracklib function with few differences.\n"
  "\n"
  "First, it always returns the given passwd. If it is found to be weak \
  ValueError exception is raised with parameter set to the reason returned by \
  cracklib's FascistCheck.\n"
  "\n"
  "Second, dictpath parameter is optional. If it is not specified the default \
  one, determined at build time, is used. See default_dictpath variable.\n"
;

static PyObject* _crack_FascistCheck(PyObject* self, PyObject* args)
{
  char* passwd;
  char const* dictpath;
  char const* reason;

  int i, fd;
  char filename[FILENAME_MAXLEN];
  char const* ext[] = { "hwm", "pwd", "pwi" };

  dictpath = DEFAULT_DICTPATH;

  if(!PyArg_ParseTuple(args, "s|s:FascistCheck", &passwd, &dictpath))
    return NULL;

  /* we need to check if files are readable, FascistCheck doesn't */
  for(i = 0; i < 3; i++) {
    snprintf(filename, FILENAME_MAXLEN - 1, "%s.%s", dictpath, ext[i]);
    fd = open(filename, O_RDONLY);
    if(fd == -1) {
      PyErr_SetFromErrnoWithFilename(PyExc_IOError, filename);
      return NULL;
    } else {
      close(fd);
    }
  }

  if((reason = FascistCheck(passwd, dictpath)) != NULL) {
    PyErr_SetString(PyExc_ValueError, reason);
    return NULL;
  }

  return Py_BuildValue("s", passwd);
}

static PyMethodDef _crack_methods[] = {
  { "FascistCheck", _crack_FascistCheck, METH_VARARGS, _crack_FascistCheck_doc },
  { NULL } /* Sentinel */
};

static char _crack_doc[] =
  "CPython libcrack wrapper.\n"
  "\n"
  "This module anables the use of cracklib features from within a Python\n"
  "program or interpreter.\n"
;

DL_EXPORT(void) init_crack(void)
{
  PyObject *m, *d, *dictpath;
  m = Py_InitModule3("_crack", _crack_methods, _crack_doc);
  d = PyModule_GetDict(m);
  dictpath = PyString_FromString(DEFAULT_DICTPATH);
  if (!d || !dictpath || PyDict_SetItemString(d, "default_dictpath", dictpath) < 0)
    return;

  Py_DECREF(dictpath);
}
