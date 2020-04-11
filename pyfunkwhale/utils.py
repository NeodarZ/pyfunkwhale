#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read()

    return data


def write_file(filename, data):
    with open(filename, 'w') as file:
        file.write(json.dumps(data))

    return data
