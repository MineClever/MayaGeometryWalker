# _*_ coding=utf-8 _*_
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: E:/Users/MyDocuments/maya/2016/scripts\geometryWalker\utils\callback.py
# Compiled at: 2015-07-11 12:45:35
import maya.cmds

class callback(object):

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args):
        maya.cmds.undoInfo(openChunk=1)
        try:
            return self.func(*self.args, **self.kwargs)
        finally:
            maya.cmds.undoInfo(closeChunk=1)