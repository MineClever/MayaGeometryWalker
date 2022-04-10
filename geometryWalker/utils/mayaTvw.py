# _*_ coding=utf-8 _*_
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: E:/Users/MyDocuments/maya/2016/scripts\geometryWalker\utils\mayaTvw.py
# Compiled at: 2016-02-11 12:16:49
"""
Created on Mar 16, 2013

@author: Olygraph
"""
import maya.cmds as cmds
from geometryWalker.utils.mayaTvwItem import mayaTvwItem

class mayaTvw(object):

    def __init__(self, tvwId=1, **args):
        self.__tvwId = tvwId
        self.__itemList = []
        self.__tvw = cmds.treeView(**args)

    def addItem(self, **args):
        args['tvw'] = self.__tvw
        nItem = mayaTvwItem(**args)
        nItem.Add()
        self.__itemList.append(nItem)
        return nItem

    def items(self, **args):
        return self.__itemList

    def item(self, itemID):
        for item in self.__itemList:
            if item.itemID == itemID:
                return item

    def removeItem(self, item):
        newList = []
        for items in self.__itemList:
            if self.item(item.itemID) != items:
                newList.append(items)

        cmds.treeView(self.__tvw, removeAll=True, edit=True)
        self.__itemList = newList

    @property
    def tvw(self):
        return self.__tvw

    @property
    def Id(self):
        return self.__tvwId

    @property
    def selectedItems(self):
        selectedItem = []
        for item in self.__itemList:
            if item.selected:
                selectedItem.append(item)

        return selectedItem

    @property
    def selectedItemsIndex(self):
        return list