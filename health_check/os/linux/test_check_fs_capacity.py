#!/usr/bin/env python
import logging
import sys
import unittest
from unittest import mock
import check_fs_capacity
from health_check.result import Result

FS_INFO = """
Filesystem           Size  Used Avail Use% Mounted on
/dev/mapper/VG-LV00  100G   10G   90G  10% /test
""".split(
    "\n"
)

FS_WARN = """
Filesystem           Size  Used Avail Use% Mounted on
/dev/mapper/VG-LV00  100G   80G   20G  80% /test
""".split(
    "\n"
)

FS_ERROR = """
Filesystem           Size  Used Avail Use% Mounted on
/dev/mapper/VG-LV00  100G   90G   10G  90% /test
""".split(
    "\n"
)


@mock.patch("check_fs_capacity.execute")
class MainTestCase(unittest.TestCase):
    def test_fs_info(self, execute):
        execute.return_value = (0, FS_INFO, "")
        sys.argv = "progname 127.0.0.1 test test".split()
        expect = [
            Result(
                logging.INFO,
                {
                    "fs": "/dev/mapper/VG-LV00",
                    "size": "100G",
                    "used": "10G",
                    "free": "90G",
                    "used%": 10,
                    "mount": "/test",
                },
            )
        ]
        result = check_fs_capacity.main()
        self.assertEqual(expect, result)

    def test_fs_warn(self, execute):
        execute.return_value = (0, FS_WARN, "")
        sys.argv = "progname 127.0.0.1 test test".split()
        expect = [
            Result(
                logging.WARN,
                {
                    "fs": "/dev/mapper/VG-LV00",
                    "size": "100G",
                    "used": "80G",
                    "free": "20G",
                    "used%": 80,
                    "mount": "/test",
                },
                rec="请及时清理文件系统",
            )
        ]
        result = check_fs_capacity.main()
        self.assertEqual(expect, result)

    def test_fs_error(self, execute):
        execute.return_value = (0, FS_ERROR, "")
        sys.argv = "progname 127.0.0.1 test test".split()
        expect = [
            Result(
                logging.ERROR,
                {
                    "fs": "/dev/mapper/VG-LV00",
                    "size": "100G",
                    "used": "90G",
                    "free": "10G",
                    "used%": 90,
                    "mount": "/test",
                },
                rec="请尽快清理文件系统",
            )
        ]
        result = check_fs_capacity.main()
        self.assertEqual(expect, result)


if __name__ == "__main__":
    unittest.main()
