#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author = Tri0nes

from multiprocessing.pool import Pool
from time import sleep

from module.utils import get_files
from module.txtop import TxtOp
from module.fetchcode import FetchCode

from lib.analyser import staticcheck

from setting import targetfile, loadrules


# =====================================
# module selector
# =====================================
def module_selector(_args):
    if _args.default:
        analyse_dir(_args.target_directory, _args.rule)

    elif _args.target:
        analyse_address(_args.target, _args.rule)
    elif _args.target_file:
        txtop = TxtOp(_args.target_file)
        analyse_address_list([line for line in txtop.read_file_lines()],_args.rule)

    elif _args.local_file:
        analyse_local(_args.local_file, _args.rule)
    elif _args.local_directory:
        analyse_dir(_args.local_directory, _args.rule)

# =====================================
# online analyse module
# =====================================
def analyse_address(_address, _rule):
    """
    download and analyse the address contract source code
    """

    f = FetchCode()
    ret, filename, code = f.fetch(_address)
    if ret:
        analyse_local(filename, _rule)
    else:
        print("[x] {0} not code found".format(_address))


def analyse_address_list(_list, _rule):
    """
    analyse the local file
    Current daily limit of 100 submissions per day per user due to the api limit
    """
    for addr in _list:
        analyse_address(addr, _rule)


# =====================================
# analyse local module
# =====================================
def analyse_local(_file, _rule):
    """
    analyse the local file
    """
    # print(f"file : {_file} , rule : {_rule}")
    all_tokens = get_files(targetfile, _file, [".sol"])
    all_rules = get_files(loadrules, _rule, [".yaml"])
    staticcheck(all_tokens, all_rules)


def analyse_dir(_dir, _rule):
    """
    analyse the local directory
    """
    all_tokens = get_files(_dir, [], [".sol"])
    all_rules = get_files(loadrules, _rule, [".yaml"])
    staticcheck(all_tokens, all_rules)


