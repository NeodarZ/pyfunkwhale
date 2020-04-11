#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def read_file(filename: str) -> str:
    """
    Simple wrapper for read a file content

    Parameters
    ----------
    filename : str
        The filename where read the datas
    """
    with open(filename, 'r') as file:
        data = file.read()

    return data


def write_file(filename: str, datas: str) -> str:
    """
    Simple wrapper for write data in file

    Parameters
    ----------
    filename : str
        The filename where write the datas
    datas : str
        The datas to write in the filename
    """
    with open(filename, 'w') as file:
        file.write(json.dumps(datas))

    return datas
