# _*_ coding=utf-8 _*_
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: E:/Users/MyDocuments/maya/2016/scripts\geometryWalker\utils\mayaTvwItem.py
# Compiled at: 2015-07-11 12:48:03
"""
Created on Mar 16, 2013

@author: Olygraph
"""
import maya.cmds as cmds

class mayaTvwItem(object):

    def __init__(self, **args):
        self.__itemIcon = None
        self.__itemSuffix = None
        self.__fontColor = None
        self.__label = None
        self.__itemID = args['itemID']
        if 'itemIcon' in args.keys():
            self.__itemIcon = args['itemIcon']
        if 'tvw' in args.keys():
            self.__tvw = args['tvw']
        if 'itemSuffix' in args.keys():
            self.__itemSuffix = args['itemSuffix']
        if 'itemLabel' in args.keys():
            self.__label = args['itemLabel']
        if 'fontColor' in args.keys():
            self.__fontColor = args['fontColor']
        return

    def Add(self, **args):
        cmds.treeView(self.__tvw, edit=True, addItem=(self.__itemID, ''))
        self.setIcon(self.__itemIcon)
        self.setSuffix(self.__itemSuffix)
        self.setFontColor(self.__fontColor)
        self.setLabel(self.__label)

    def setLabel(self, label):
        if label is not None:
            cmds.treeView(self.__tvw, edit=True, displayLabel=(self.__itemID, label))
            self.__label = label
        return

    def setIcon(self, icon):
        if icon is not None:
            cmds.treeView(self.__tvw, edit=True, image=(self.__itemID, 1, icon))
            self.__itemIcon = icon
        return

    def setSuffix(self, suffix):
        if suffix is not None:
            cmds.treeView(self.__tvw, edit=True, displayLabelSuffix=(self.__itemID, suffix))
            self.__itemSuffix = suffix
        return

    def setFontColor(self, fontColor):
        if fontColor is not None:
            cmds.treeView(self.__tvw, textColor=(self.__itemID, fontColor[0], fontColor[1], fontColor[2]), edit=True)
            self.__fontColor = fontColor
        return

    def remove(self):
        return True

    @property
    def itemID(self):
        return self.__itemID

    @property
    def selected(self):
        return cmds.treeView(self.__tvw, q=True, itemSelected=self.__itemID)