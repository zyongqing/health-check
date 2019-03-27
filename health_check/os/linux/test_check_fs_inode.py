#!/usr/bin/env python
import logging
import sys
import unittest
from unittest import mock
import check_fs_inode
from health_check.result import Result

FS_INFO = """
Filesystem          Inodes IUsed IFree IUse% Mounted on
/dev/mapper/VG-LV00   100K   10K   90K   10% /test
""".split(
    "\n"
)

FS_WARN = """
Filesystem          Inodes IUsed IFree IUse% Mounted on
/dev/mapper/VG-LV00   100K   80K   20K   80% /test
""".split(
    "\n"
)

FS_ERROR = """
Filesystem          Inodes IUsed IFree IUse% Mounted on
/dev/mapper/VG-LV00   100K   90K   10K   90% /test
""".split(
    "\n"
)


@mock.patch("check_fs_inode.execute")
class MainTestCase(unittest.TestCase):
    def test_fs_info(self, execute):
        execute.return_value = (0, FS_INFO, "")
        sys.argv = "progname 127.0.0.1 test test".split()
        expect = [
            Result(
                logging.INFO,
                {
                    "fs": "/dev/mapper/VG-LV00",
                    "inodes": "100K",
                    "iused": "10K",
                    "ifree": "90K",
                    "iused%": 10,
                    "mount": "/test",
                },
            )
        ]
        result = check_fs_inode.main()
        self.assertEqual(expect, result)

    def test_fs_warn(self, execute):
        execute.return_value = (0, FS_WARN, "")
        sys.argv = "progname 127.0.0.1 test test".split()
        expect = [
            Result(
                logging.WARN,
                {
                    "fs": "/dev/mapper/VG-LV00",
                    "inodes": "100K",
                    "iused": "80K",
                    "ifree": "20K",
                    "iused%": 80,
                    "mount": "/test",
                },
                rec="请及时清理文件系统",
            )
        ]
        result = check_fs_inode.main()
        self.assertEqual(expect, result)

    def test_fs_error(self, execute):
        execute.return_value = (0, FS_ERROR, "")
        sys.argv = "progname 127.0.0.1 test test".split()
        expect = [
            Result(
                logging.ERROR,
                {
                    "fs": "/dev/mapper/VG-LV00",
                    "inodes": "100K",
                    "iused": "90K",
                    "ifree": "10K",
                    "iused%": 90,
                    "mount": "/test",
                },
                rec="请尽快清理文件系统",
            )
        ]
        result = check_fs_inode.main()
        self.assertEqual(expect, result)


if __name__ == "__main__":
    unittest.main()
