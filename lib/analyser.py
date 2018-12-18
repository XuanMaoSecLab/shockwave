import re
import os
import yaml
import time
import sys

from module.csvop import CsvOp

from setting import output_file,verbose,debug

csvop = CsvOp(output_file,",")
csvop.get_header()

def matchcheck(_content, _notarray):
    for value in _notarray:
        if value in _content:
            return True,0
    return False,0


def method_match(_screen, _rule, i):
    rules = _rule[i]['rule']
    match = _rule[i]['match'][True]
    notmatch = _rule[i]['match'][False]
    result, lineno = matchcheck(_screen, rules)
    if result:
        return match, _screen, lineno
    else:
        return notmatch, _screen, lineno


def method_regex(_screen, _rule, i):
    regex = _rule[i]['rule']
    flag = None
    if _rule[i]["factor"][0]: flag = re.M
    if _rule[i]["factor"][1]:
        if flag:
            flag = flag | re.I
        else:
            flag = re.I
    if _rule[i]["factor"][2]:
        if flag:
            flag = flag | re.S
        else:
            flag = re.S
    if flag:
        searchObj = re.search(regex, _screen, flag)
    else:
        searchObj = re.search(regex, _screen)

    match = _rule[i]['match'][True]
    notmatch = _rule[i]['match'][False]
    if searchObj:
        searchObj.start()
        start = searchObj.start()
        lineno = _screen.count('\n', 0, start) + 1
        if _rule[i]['fetch']:
            return match, searchObj.group(), lineno
        return match, _screen, lineno
    else:
        return notmatch, _screen, 0


def poccheck(_content, _rule):
    screen = _content
    for i in range(len(_rule)):
        if _rule[i]["method"] == "regex":
            result, screen, lineno= method_regex(screen, _rule, i)
            if result == 'next':
                continue
            if result == 'fail':
                return False, "", 0
            if result == 'success':
                return True, screen, lineno
        if _rule[i]["method"] == "match":
            result, screen, lineno = method_match(screen, _rule, i)
            if result == 'next':
                continue
            if result == 'fail':
                return False, "", 0
            if result == 'success':
                return True, screen, lineno


import threading

lock = threading.RLock()


class mythread(threading.Thread):
    def __init__(self, tname, process, tokenpath, rulepath):
        threading.Thread.__init__(self)
        self.name = tname
        self.process = process
        self.tokenpath = tokenpath
        self.rulepath = rulepath

    def run(self):
        if verbose :
            print('[*] [Scan][t-{0}][p-{1:.2f}%]: {2} ----> {3}'.format(self.name, self.process*100, os.path.basename(self.tokenpath),
                                                      os.path.basename(self.rulepath)))
        else:
            print("[*] [Scan][t-{0}][p-{1:.2f}%]".format(self.name, self.process*100),end='\r')
            sys.stdout.flush()
        f_token = open(self.tokenpath, "r", encoding='utf-8')
        content = f_token.read()
        f_rule = open(self.rulepath)
        rule = yaml.load(f_rule)
        f_token.close()
        f_rule.close()
        result, catch, lineno = poccheck(content, rule)
        if result:
            lock.acquire()
            filename = os.path.basename(self.tokenpath)
            vulname = os.path.basename(self.rulepath)
            address = ""
            if "0x" in filename: address = re.search(r'0x\w{40}', filename).group()
            info = {
                    "Filename": filename,
                    "Address": address,
                    "Vulname": vulname,
                    "Lineno": lineno,
                    "Date": time.strftime("%Y-%m-%d-%H-%M-%S")
                    }
            print("[+] [found] {0}".format(info))
            csvop.write_line(info)
            lock.release()


def staticcheck(_all_tokens, _all_rules):
    '''
    start static check
    :param _all_tokens : [ ]
    :param _all_rules  : [ ]
    '''
    thread_list = []
    t_num = 0
    all_t = len(_all_tokens) * len(_all_rules)
    print("[*] loaded tokens : {0} , rules : {1} , thread count : {2}".format(len(_all_tokens), len(_all_rules), str(all_t)))
    for tokenpath in _all_tokens:
        for rulepath in _all_rules:
            ## multithread
            t_num += 1
            thread_list.append(mythread(t_num, t_num/all_t, tokenpath, rulepath))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
