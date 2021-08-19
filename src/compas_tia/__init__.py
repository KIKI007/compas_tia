"""
********************************************************************************
compas_tia
********************************************************************************

.. currentmodule:: compas_tia


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os


__author__ = ["ziqi wang"]
__copyright__ = "Ziqi Wang"
__license__ = "MIT License"
__email__ = "qiqiustc@gmail.com"
__version__ = "0.1.0"

HERE = os.path.dirname(__file__)
HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

from ._tia_datastructure import *  # noqa: F401 F403
__all__ = [name for name in dir() if not name.startswith('_')]
