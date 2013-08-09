#! /usr/bin/env python

import unittest
import os

from pymsbayes.utils import (functions, get_tool_path, TOOL_PATH_MAP,
        MSBAYES_SORT_INDEX)
from pymsbayes.test.support import package_paths
from pymsbayes.test.support.pymsbayes_test_case import PyMsBayesTestCase

class MsBayesSortIndexTestCase(unittest.TestCase):
    def test_valid_values(self):
        self.assertEqual(MSBAYES_SORT_INDEX.valid_values, list(range(8)))

    def test_default(self):
        self.assertEqual(MSBAYES_SORT_INDEX.current_value(), 7)

    def test_set(self):
        for i in range(8):
            MSBAYES_SORT_INDEX.set_index(i)
            self.assertEqual(MSBAYES_SORT_INDEX.current_value(), i)

    def test_invalid_value(self):
        self.assertRaises(Exception, MSBAYES_SORT_INDEX.set_index, -1)
        self.assertRaises(Exception, MSBAYES_SORT_INDEX.set_index, 8)

class GetToolPathTestCase(unittest.TestCase):
    def test_error(self):
        self.assertRaises(Exception, get_tool_path, 'blah')

    def test_get_tool_path(self):
        for name, path in TOOL_PATH_MAP.iteritems():
            p = get_tool_path(name)
            self.assertEqual(p, path)
            self.assertTrue(os.path.exists(p))

class MkdrTestCase(PyMsBayesTestCase):
    def setUp(self):
        self.set_up()
        p = ['mkdr', 'test', 'dir']
        self.path = os.path.join(self.temp_fs.base_dir, *p)
        for i in range(len(p)):
            self.register_dir(os.path.join(
                    self.temp_fs.base_dir,
                    *p[:i+1]))

    def tearDown(self):
        self.tear_down()
    
    def test_mkdr(self):
        self.assertFalse(os.path.exists(self.path))
        functions.mkdr(self.path)
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.isdir(self.path))
        functions.mkdr(self.path)
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.isdir(self.path))

class MkNewDirTestCase(PyMsBayesTestCase):
    def setUp(self):
        self.set_up()
        p = ['mkdr', 'test', 'dir']
        self.path = os.path.join(self.temp_fs.base_dir, *p)
        for i in range(len(p)):
            self.register_dir(os.path.join(
                    self.temp_fs.base_dir,
                    *p[:i+1]))

    def tearDown(self):
        self.tear_down()
    
    def test_mk_new_dir(self):
        self.assertFalse(os.path.exists(self.path))
        functions.mk_new_dir(self.path)
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.isdir(self.path))
        for i in range(10):
            functions.mk_new_dir(self.path)
            p = self.path + '-' + str(i)
            self.assertTrue(os.path.exists(p))
            self.assertTrue(os.path.isdir(p))
            self.register_dir(p)

class WhereisTestCase(unittest.TestCase):
    def test_whereis(self):
        path = functions.whereis('more')
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))
        path = functions.whereis('x_bogus_exe_name_x')
        self.assertIsNone(path)

class IsFileTestCase(unittest.TestCase):
    def setUp(self):
        self.file = package_paths.data_path("4pairs_1locus.cfg")
        self.bogus_file = package_paths.data_path("bogusdatafilename")
    
    def test_is_file(self):
        self.assertFalse(functions.is_file(None))
        self.assertFalse(functions.is_file(self.bogus_file))
        self.assertTrue(functions.is_file(self.file))
        
class IsdirTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = package_paths.data_path()
        self.file = package_paths.data_path("4pairs_1locus.cfg")
    
    def test_is_dir(self):
        self.assertFalse(functions.is_dir(None))
        self.assertFalse(functions.is_dir(self.file))
        self.assertTrue(functions.is_dir(self.dir))

class IsExecutableTestCase(unittest.TestCase):
    def setUp(self):
        self.file = package_paths.data_path("4pairs_1locus.cfg")
        self.bogus_file = package_paths.data_path("bogusdatafilename")
        self.exe = get_tool_path('eureject')
    
    def test_is_executable(self):
        self.assertFalse(functions.is_executable(None))
        self.assertFalse(functions.is_executable(self.bogus_file))
        self.assertFalse(functions.is_executable(self.file))
        self.assertTrue(functions.is_executable(self.exe))

class LongDivisionTestCase(unittest.TestCase):
    def test_long_division(self):
        self.assertEqual(functions.long_division(5, 2), (2, 1))
        self.assertEqual(functions.long_division(6, 2), (3, 0))
        self.assertEqual(functions.long_division(-11, 3), (-4, 1))

if __name__ == '__main__':
    unittest.main()
