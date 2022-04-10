# _*_ coding=utf-8 _*_
#!/usr/bin/python2.7

import os , sys

def runScript(*args, **kw):
    
    filePath = os.path.realpath(__file__)
    if filePath not in sys.path:
        sys.path.append(filePath)
    import geometryWalker.QT.pickWalker_UI as pickWalker_UI
    reload(pickWalker_UI)
    pickWalker_UI.pickWalkerUI()
    
def onMayaDroppedPythonFile (*args, **kw):
    runScript()