#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author = Tri0nes

class TxtOp():
    def __init__(self,_file):
        self.file = _file

    def write_line_add(self,_line):
        with open(self.file,"a", encoding="utf-8", newline='') as f:
            f.write(_line + "\n")


    def write_list(self,_list):
        self.empty_file()
        with open(self.file,"w", encoding="utf-8", newline='') as f:
            for line in _list:
                f.write(line + "\n")


    def write_list_add(self,_list):
        with open(self.file,"a", encoding="utf-8", newline='') as f:
            for line in _list:
                f.write(line + "\n")


    def empty_file(self):
        with open(self.file,"w", encoding="utf-8", newline='') as f:
            f.write("")


    def read_file_lines(self):
        with open(self.file,"r", encoding="utf-8", newline='') as f:
            for line in f.readlines():
                ret = line.strip()
                yield ret

