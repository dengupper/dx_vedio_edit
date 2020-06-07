# _*_ encoding: utf-8 _*-

import os, sys

__version__ = "1.0.0"
__version_info__ = (1, 0, 0, "", "")

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)

from .style_window import *
from .image_button import *
from .auxiliary import *
from .title import *