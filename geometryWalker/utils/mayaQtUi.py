# _*_ coding=utf-8 _*_
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: E:/Users/MyDocuments/maya/2016/scripts\geometryWalker\utils\mayaQtUi.py
# Compiled at: 2016-02-08 02:48:45
"""
Created on Mar 10, 2013

@author: Olygraph
"""
import maya.cmds as cmds

class mayaQtUi(object):

    def __init__(self, windowName, qtUiPath, closeBefore=True):
        self._windowName = windowName
        self._objectList = []
        if closeBefore:
            self.close()
        myWin = cmds.loadUI(f=qtUiPath)
        cmds.showWindow(myWin)
        self.window = myWin
        items = cmds.lsUI(dumpWidgets=True)
        for item in items:
            self._objectList.append(item)

    def getUiItem(self, uiItem):
        if type(self._objectList) is list:
            for item in self._objectList:
                nitem = item
                if len(item) > 2:
                    while nitem[(-1)] == '|' and len(nitem) > 1:
                        nitem = nitem[:-1]

                if nitem.endswith(uiItem):
                    return item

    def getParent(self, uiItem):
        uiItem = self.getUiItem(uiItem)
        if uiItem is not None:
            if len(uiItem) > 2:
                while uiItem[(-1)] == '|' and len(uiItem) > 1:
                    uiItem = uiItem[:-1]

            layoutItems = uiItem.split('|')
            parentUi = ''
            for i in range(len(layoutItems) - 1):
                parentUi += layoutItems[i] + '|'

            return parentUi[:-1]
        else:
            return

    def close(self):
        if cmds.window(self._windowName, q=True, exists=True):
            cmds.deleteUI(self._windowName)

    @property
    def windowName(self):
        return self.window