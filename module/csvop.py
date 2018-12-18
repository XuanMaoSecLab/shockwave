#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author = Tri0nes

import csv


class CsvOp(object):
    def __init__(self, _csvfile,_delimiter='\t'):
        self.csv_file = _csvfile
        self.deli = _delimiter
        self.header = {}


    def add_header(self,_fields):
        """
        add the header fields
        :param _fields: [cloumn1,cloumn2]
        """
        i = len(self.header)
        for key in _fields:
            if key not in self.header.keys():
                self.header[key] = i
                i += 1


    def get_header(self,_header=None):
        """
        parse the header
        :param _header: [cloumn1,cloumn2]
        :return json: {"cloumn1":1,"cloumn2":2}
        """
        if _header:
            theheader = _header
        else:
            with open(self.csv_file,"r",encoding = "utf-8") as f:
                reader = csv.DictReader(f, delimiter=self.deli, quotechar='"')
                theheader = reader.fieldnames
        header = {}
        i = 0
        for key in theheader:
            header[key] = i
            i += 1
        self.header = header
        return header


    def empty_file(self):
        with open(self.csv_file,"w", encoding="utf-8", newline='') as f:
            header = self.header.keys()
            writer = csv.writer(f,delimiter=self.deli)
            writer.writerow(header)


    def write_line(self,_info):
        """
        write data of an bug id
        :param _info: info
        :return bool: Success or not
        """
        with open(self.csv_file,"a+", encoding="utf-8", newline='') as f:
            headers = self.header.keys()
            writer = csv.DictWriter(f,headers,delimiter=self.deli)
            writer.writerow(_info)
        return True

    def add_line(self,_info):
        """
        add a new line
        :param _info: info
        :return bool: Success or not
        """
        with open(self.csv_file,"a+", encoding="utf-8", newline='') as f:
            f.write(_info + "\n")


    def columns(self,_column):
        """
        read columns
        :param _column: column name
        :return: colunms
        """
        with open(self.csv_file,"r",encoding = "utf-8") as f:
            reader = csv.DictReader(f, delimiter=self.deli, quotechar='"')
            columns = [row[_column] for row in reader]
            return columns

            
    def csv_generater(self):
        """
        csv file read line
        :param _file: csv file
        :return: every single line of the file
        """
        with open(self.csv_file,"r",encoding = "utf-8") as f:
            reader = csv.reader(f, delimiter=self.deli, quotechar='"')
            next(reader, None) # discard the header
            for row in reader:
                yield row


    def csv_dict_generater(self):
        '''
        csv file read line by DictReader
        :param _file: csv file
        :return: every single line of the file
        '''
        with open(self.csv_file,"r",encoding = "utf-8") as f:
            reader = csv.DictReader(f, delimiter=self.deli, quotechar='"')
            for row in reader:
                yield row