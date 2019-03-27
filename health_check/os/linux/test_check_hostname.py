#!/usr/bin/env python
import logging
import sys
import unittest
from unittest import mock
import check_hostname
from health_check.result import Result

HOSTNAME_INFO = """
rac1
""".split(
    "\n"
)


@mock.patch("check_hostname.execute")
class MainTestCase(unittest.TestCase):
    def test_fs_info(self, execute):
        execute.return_value = (0, HOSTNAME_INFO, "")
        sys.argv = "progname 127.0.0.1 test test".split()
        expect = Result(logging.INFO, "rac1")
        result = check_hostname.main()
        self.assertEqual(expect, result)


if __name__ == "__main__":
    unittest.main()
