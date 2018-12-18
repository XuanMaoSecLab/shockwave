import sys
import os
import argparse

from module.utils import filenamewith

from setting import path

LOGO = r"""

         __               __                           
   _____/ /_  ____  _____/ /___      ______ __   _____ 
  / ___/ __ // __ // ___/ //_/ | /| / / __ `/ | / / _ /
 (__  ) / / / /_/ / /__/ ,<  | |/ |/ / /_/ /| |/ /  __/
/____/_/ /_//____//___/_/|_| |__/|__//__,_/ |___//___/ 

                                            VERSION 2.0

Shock Wave is a static analysis tool of smart contracts.
"""


def check_exists(_file):
    if not os.path.exists(_file):
        print("[x] not exists : {0}".format(_file))
        sys.exit()


def parse_args():
    print(LOGO)
    parser = argparse.ArgumentParser(prog='shockwave.py', usage='%(prog)s [options]', add_help=True)
    parser.add_argument('-d', help='default : analyse all local files with all rules', action='count', default=0, dest='default')

    parser.add_argument('-t', help='target address', dest='target')
    parser.add_argument('--target-file', metavar='', help='target address list file', dest='target_file')

    parser.add_argument('-l', help='analyse local code files', dest='local_file')
    parser.add_argument('--local-dir', metavar='', help='analyse local code directory', dest='local_directory',
                        default="{0}/codes/".format(path))

    parser.add_argument('-r', help="designate vulnerability rule ID likes A.1,A.2,C.1,D.1", dest='rule', default=[])

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()

    if args.default:
        args.target_directory = "{0}/codes/".format(path)
        args.rule = []

    if args.target_file: check_exists(args.target_file)

    if args.local_file: check_exists(args.local_file)
    if args.local_directory: check_exists(args.local_directory)

    if args.rule:
        vulns = args.rule.split(",")
        args.rule = []
        for vuln in vulns:
            args.rule.append("[{}]".format(vuln))

    return args
