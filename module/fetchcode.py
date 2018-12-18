#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author = Tri0nes

import requests
import json
import os


from time import sleep

from module.txtop import TxtOp
from module.csvop import CsvOp

from setting import apikey, verbose, debug, info_file, path


def check_exists(_address):
    # get all file address
    allfile = os.listdir(path + "/codes/")
    for fl in allfile:
        if _address.upper() in fl.upper():
            return True, path + "/codes/" + fl
    return False, ""


def write2file(_address, _name, _code):
    output = "./codes/{0}_{1}.sol".format(_name, _address)
    txtop = TxtOp(output)
    txtop.empty_file()
    txtop.write_line_add(_code)
    return output


def req(_url):
    if verbose: print(f"[*] requesting : {_url}")
    for i in range(3):
        try:
            g = requests.get(_url, timeout=5)
            if debug : print(f"[+] [DEBUG] {g.text}")
            return g.text
        except Exception as e:
            print(f"[x] [ERROR] {e}")
        sleep(0.8)
    return False


def record(_info):
    csvop = CsvOp(info_file, ",")
    csvop.get_header()
    csvop.write_line(_info)
    return True


class FetchCode:

    def fetch(self, _address):
        # check file
        is_file, code_file = check_exists(_address)
        if is_file:
            with open(code_file, "r",encoding = "utf-8") as f:
                lines = f.readlines()
                return True, os.path.basename(code_file).split(".")[0], lines

        # download
        url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address={0}&apikey={1}".format(
            _address, apikey)
        r = req(url)
        if not r: return False, None, None
        response = json.loads(r)
        result = response["result"][0]
        if not result["SourceCode"]: return False, None, None

        # write to file
        output = write2file(_address, result["ContractName"], result["SourceCode"])

        result["Address"] = _address
        info = {}
        for k, v in result.items():
            if k == "Address" or k == "ContractName" or k == "CompilerVersion" or k == "OptimizationUsed" or k == "Runs":
                info[k] = v
        record(info)

        return True, output, result["SourceCode"]
