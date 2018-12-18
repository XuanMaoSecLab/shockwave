
import os
import itertools

from itertools import product

# get_files(loadrules,["[F.3]","[A.1]"],[".yaml"])
def get_files(_path, _startwith=None, _endwith=None):
    '''
    get all files
    :param _startwith : ["str1","str2"]
    :param _endwith : [".sol",".py"]
    '''
    if not _startwith: _startwith = [""]
    if type(_startwith) is str : 
        if os.path.isfile(_startwith):
            return [_startwith]
        else:
            _startwith = [_startwith]
    if not _endwith: _endwith = [""]
    if type(_endwith) is str : _endwith = [_endwith]

    all_files = []

    def checkwith(_fp,_fn):
        for x,y in list(product(_startwith, _endwith)):
            if _fn.startswith(x) and _fn.endswith(y):
                path_name = os.path.join(_fp,_fn)
                all_files.append(path_name)

    for fpath, dirname, fnames in os.walk(_path):
        for filename in fnames:
            checkwith(fpath,filename)
    return all_files


def filestartwith(_file):
    _startwith = []
    if '.' in _file:
        for t in _file.split(","):
            _startwith.append("[{0}]".format(t))
    else:
        _startwith = [""]
    return _startwith


def filenamewith(_file):
    _startwith = []
    if _file:
        for t in _file.split(","):
            _startwith.append(t)
    else:
        _startwith = [""]
    return _startwith
