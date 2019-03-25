#!/usr/bin/env python
import argparse
import json
import logging
import sys
from datetime import datetime
from health_check.utils.logging import current_logger as logger
from health_check.utils.zipfile import save_all

#    _______  __        ______   .______        ___       __        #
#   /  _____||  |      /  __  \  |   _  \      /   \     |  |       #
#  |  |  __  |  |     |  |  |  | |  |_)  |    /  ^  \    |  |       #
#  |  | |_ | |  |     |  |  |  | |   _  <    /  /_\  \   |  |       #
#  |  |__| | |  `----.|  `--'  | |  |_)  |  /  _____  \  |  `----.  #
#   \______| |_______| \______/  |______/  /__/     \__\ |_______|  #
#                                                                   #


__version__ = "1.0.0"


#  .___  ___.      ___       __  .__   __.  #
#  |   \/   |     /   \     |  | |  \ |  |  #
#  |  \  /  |    /  ^  \    |  | |   \|  |  #
#  |  |\/|  |   /  /_\  \   |  | |  . `  |  #
#  |  |  |  |  /  _____  \  |  | |  |\   |  #
#  |__|  |__| /__/     \__\ |__| |__| \__|  #
#                                           #


def load_checks_module(platform):
    module_name = "health_check.os.%s.checks" % platform
    checks = __import__(module_name, globals(), locals(), ["checks"])
    return checks


def get_zipfile_name(platform, host):
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y%m%d_%H%M%S")
    return "{}_{}_{}.zip".format(platform, host, current_time_str)


def run_all_checks(host, port, username, password, checks):
    for each_check in checks:
        check_name = each_check.__name__.split(".")[-1]
        check_func = each_check.check_retrieve

        try:
            check_result = check_func(host, port, username, password)
            json_check_reuslt = json.dumps(check_result)
            yield check_name, json_check_reuslt
            logger.debug("check [%s]: ok", check_name)
        except Exception as e:
            logger.warn("check [%s]: %s", check_name, e)


def main():
    parser = argparse.ArgumentParser(description="health check")
    parser.add_argument("host", help="host name")
    parser.add_argument("username", help="host username")
    parser.add_argument("password", help="host password")
    parser.add_argument("platform", help="host platform", choices=["windows", "linux"])
    parser.add_argument("--port", help="host port", type=int)
    parser.add_argument("--verbose", help="debug mode", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    checks_module = load_checks_module(args.platform)
    all_checks = checks_module.__all__

    if args.port is None:
        args.port = checks_module.DEFAULT_PORT

    save_all(
        get_zipfile_name(args.platform, args.host),
        run_all_checks(args.host, args.port, args.username, args.password, all_checks),
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
