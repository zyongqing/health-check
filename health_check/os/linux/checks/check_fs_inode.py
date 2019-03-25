#!/usr/bin/env python
import argparse
import logging
import sys

if __name__ == "__main__":
    from helper import logger, execute
else:
    from .helper import logger, execute


#    _______  __        ______   .______        ___       __        #
#   /  _____||  |      /  __  \  |   _  \      /   \     |  |       #
#  |  |  __  |  |     |  |  |  | |  |_)  |    /  ^  \    |  |       #
#  |  | |_ | |  |     |  |  |  | |   _  <    /  /_\  \   |  |       #
#  |  |__| | |  `----.|  `--'  | |  |_)  |  /  _____  \  |  `----.  #
#   \______| |_______| \______/  |______/  /__/     \__\ |_______|  #
#                                                                   #


__version__ = "1.0.0"


#  .______       _______ .___________..______       __   ___________    ____  _______ #
#  |   _  \     |   ____||           ||   _  \     |  | |   ____\   \  /   / |   ____|#
#  |  |_)  |    |  |__   `---|  |----`|  |_)  |    |  | |  |__   \   \/   /  |  |__   #
#  |      /     |   __|      |  |     |      /     |  | |   __|   \      /   |   __|  #
#  |  |\  \----.|  |____     |  |     |  |\  \----.|  | |  |____   \    /    |  |____ #
#  | _| `._____||_______|    |__|     | _| `._____||__| |_______|   \__/     |_______|#
#                                                                                     #


REMOTE_COMMAND = """
df -i
"""


def check_retrieve(host, port, username, password):
    _, result, _ = execute(host, port, username, password, REMOTE_COMMAND)
    logger.debug("check retrieve => %s", result)
    return result


#   __________   ___ .___________..______          ___       ______ .___________. #
#  |   ____\  \ /  / |           ||   _  \        /   \     /      ||           | #
#  |  |__   \  V  /  `---|  |----`|  |_)  |      /  ^  \   |  ,----'`---|  |----` #
#  |   __|   >   <       |  |     |      /      /  /_\  \  |  |         |  |      #
#  |  |____ /  .  \      |  |     |  |\  \----./  _____  \ |  `----.    |  |      #
#  |_______/__/ \__\     |__|     | _| `._____/__/     \__\ \______|    |__|      #
#                                                                                 #


def check_extract(source):
    logger.debug("check extract => %s", source)
    return source


#   ___________    ____  ___       __       __    __       ___   .___________. _______ #
#  |   ____\   \  /   / /   \     |  |     |  |  |  |     /   \  |           ||   ____|#
#  |  |__   \   \/   / /  ^  \    |  |     |  |  |  |    /  ^  \ `---|  |----`|  |__   #
#  |   __|   \      / /  /_\  \   |  |     |  |  |  |   /  /_\  \    |  |     |   __|  #
#  |  |____   \    / /  _____  \  |  `----.|  `--'  |  /  _____  \   |  |     |  |____ #
#  |_______|   \__/ /__/     \__\ |_______| \______/  /__/     \__\  |__|     |_______|#
#                                                                                      #


def check_evaluate(source):
    logger.debug("check evaluate => %s", source)
    return source


#  .___  ___.      ___       __  .__   __.  #
#  |   \/   |     /   \     |  | |  \ |  |  #
#  |  \  /  |    /  ^  \    |  | |   \|  |  #
#  |  |\/|  |   /  /_\  \   |  | |  . `  |  #
#  |  |  |  |  /  _____  \  |  | |  |\   |  #
#  |__|  |__| /__/     \__\ |__| |__| \__|  #
#                                           #


def main():
    parser = argparse.ArgumentParser(description="check host connection")
    parser.add_argument("host", help="host name")
    parser.add_argument("username", help="host username")
    parser.add_argument("password", help="host password")
    parser.add_argument("--port", help="host port", type=int, default=22)
    parser.add_argument("--verbose", help="debug mode", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    retrieve_result = check_retrieve(args.host, args.port, args.username, args.password)
    extract_result = check_extract(retrieve_result)
    evaluate_result = check_evaluate(extract_result)
    print(evaluate_result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
