#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def read_file(filename):
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


def write_file(filename, data):
    """
    Simple wrapper for write data in file

    Parameters
    ----------
    filename : str
        The filename where write the datas
    data : str
        The datas to write in the filename
    """
    with open(filename, 'w') as file:
        file.write(json.dumps(data))

    return data
