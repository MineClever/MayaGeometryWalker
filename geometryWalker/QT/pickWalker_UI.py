# _*_ coding=utf-8 _*_
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: E:/Users/MyDocuments/maya/2016/scripts\geometryWalker\QT\pickWalker_UI.py
# Compiled at: 2016-02-11 12:17:41
"""
Created on Feb 7, 2016

@author: Olygraph
"""
import geometryWalker.utils.mayaQtUi as qtUi, os, maya.cmds as cmds
from geometryWalker.utils.callback import callback
import re, geometryWalker.walker as walker

class pickWalkerUI(object):
    UI_FILE = os.path.join(os.path.dirname(__file__), 'pickwalker')
    textVtx = {}

    def __init__(self):
        self._pickWalkerUI = qtUi.mayaQtUi('pickWalker', self.UI_FILE + '.ui')
        cmds.window(self._pickWalkerUI.windowName, edit=True, le=400, te=400)
        for i in range(0, 6):
            x = str(i)
            layoutVtx0 = self._pickWalkerUI.getParent('vtx' + x)
            self.textVtx[x] = cmds.textField(parent=layoutVtx0, enable=True)
            cmds.button(parent=layoutVtx0, label='<', width=30, command=callback(self.__cmdClick, x))
            cmds.deleteUI(self._pickWalkerUI.getUiItem('vtx' + x))
            cmds.deleteUI(self._pickWalkerUI.getUiItem('btnVtx' + x))

        layoutMask = self._pickWalkerUI.getParent('maskEnabled')
        self.txtMask = cmds.textField(parent=layoutMask, enable=False, text='MASK OFF')
        cmds.button(parent=layoutMask, label='Clear', width=30, command=callback(self.__maskClear), enable=False)
        cmds.button(parent=layoutMask, label='<', width=30, command=callback(self.__maskClick), enable=False)
        cmds.deleteUI(self._pickWalkerUI.getUiItem('maskEnabled'))
        cmds.deleteUI(self._pickWalkerUI.getUiItem('maskEnabledBtn'))
        layoutSpace = self._pickWalkerUI.getParent('btnObjSpace')
        self.spaceOption = cmds.radioButtonGrp(parent=layoutSpace, label='Vtx Coordinates Mode :   ', labelArray2=[
         'Object Space', 'World Space'], numberOfRadioButtons=2, sl=2)
        options = self._pickWalkerUI.getParent('btnCopyVtxPos')
        self.checkBox_VTX = cmds.checkBox(parent=options, label='Copy Vertex Position', v=True,ed=False)
        self.checkBox_VTXColor = cmds.checkBox(parent=options, label='Copy Vertex Color', enable=False)
        self.checkBox_UV = cmds.checkBox(parent=options, label='Copy UVs', enable=False)
        self.checkBox_UV = cmds.checkBox(parent=options, label='Keep Selection Info in Extra Attrs', enable=False)
        cmds.deleteUI(self._pickWalkerUI.getUiItem('btnCopyVtxPos'))
        cmds.deleteUI(self._pickWalkerUI.getUiItem('btnObjSpace'))
        cmds.deleteUI(self._pickWalkerUI.getUiItem('btnWorldSpace'))
        goBtnLayout = self._pickWalkerUI.getParent('btnGo')
        cmds.button(parent=goBtnLayout, label='Pick Walk (WATCH OUT no Undo on this command)', command=callback(self.__reorder))
        cmds.deleteUI(self._pickWalkerUI.getUiItem('btnGo'))

    def __reorder(self):
        verts = {}
        for i in range(0, 6):
            x = str(i)
            textField = cmds.textField(self.textVtx[x], query=True, text=True)
            if textField != '':
                verts[i] = textField

        coordSys = cmds.radioButtonGrp(self.spaceOption, query=True, select=True)
        faceRegEx = '^(.*)\\.f\\[([\\d]+)\\]$'
        vtxRegEx = '^(.*)\\.vtx\\[([\\d]+)\\]$'
        faceIdxA = int(re.match(faceRegEx, verts[0]).group(2))
        faceIdxB = int(re.match(faceRegEx, verts[3]).group(2))
        objA = re.match(faceRegEx, verts[0]).group(1)
        objB = re.match(faceRegEx, verts[3]).group(1)
        v0A = int(re.match(vtxRegEx, verts[1]).group(2))
        v1A = int(re.match(vtxRegEx, verts[2]).group(2))
        v0B = int(re.match(vtxRegEx, verts[4]).group(2))
        v1B = int(re.match(vtxRegEx, verts[5]).group(2))
        reload(walker)
        myWalker = walker.walker(objA, objB, int(coordSys))
        myWalker.pickWalkTwoMesh(faceIdxA, faceIdxB, [v0A, v1A], [v0B, v1B])

    def __maskClear(self):
        self.maskFaces = []
        cmds.textField(self.txtMask, edit=True, text='MASK OFF')

    def __maskClick(self):
        fExpend = cmds.filterExpand(ex=True, sm=34)
        faceRegEx = re.compile('^(.*)\\.f\\[([\\d]+)\\]$')
        self.maskFaces = []
        if fExpend != None:
            for face in fExpend:
                faceId = re.match(faceRegEx, face).group(2)
                self.maskFaces.append(int(faceId))

            cmds.textField(self.txtMask, edit=True, text='MASK ON')
        else:
            cmds.error('Please Select at least one Face')
        return

    def __cmdClick(self, vtxNum):
        sel = cmds.ls(sl=True)
        if vtxNum == '0' or vtxNum == '3':
            fExpend = cmds.filterExpand(ex=True, sm=34)
            itemName = 'face'
        else:
            fExpend = cmds.filterExpand(ex=True, sm=31)
            itemName = 'vertex'
        if fExpend is not None:
            if len(fExpend) > 1:
                cmds.error('Need to select only 1 %s' % itemName)
        else:
            cmds.error('Please Select at least 1 %s' % itemName)
        cmds.textField(self.textVtx[vtxNum], edit=True, text=sel[0])
        return