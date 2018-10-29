#!/usr/bin/env python3
"""Make absolyte path to working with database on different platforms."""

import sys
import os


def make_absolyte_path(relative_path):
    """Make absolyte path of dataBASE file."""
    script_name = sys.argv[0]
    script_path = os.path.dirname(script_name)
    absolute_path = os.path.abspath(script_path)
    os_path = os.path.join(absolute_path, *relative_path)
    return os_path


RECIPE_PATH = make_absolyte_path(['data', 'resipe_class'])
COLLECTION_PATH = make_absolyte_path(['data', 'collection_class'])
