# _*_ coding=utf-8 _*_

"""
Created on Jan 17, 2016

@author: Olygraph
"""
import maya.OpenMaya as om
import maya.mel as mel
import maya.cmds as cmds
import geometryWalker.utils.mayaApiHelper as mayaApiHelper
import time
# from Queue import Queue
# from threading import Thread


class walker(object):
    vtxListA = []
    edgeListA = []
    queueA = []

    def __init__(self, meshA, meshB="", coordSys=0):
        self._meshA = meshA
        self._meshB = meshB
        if coordSys == 1:
            self._coordSys = om.MSpace.kObject
        elif coordSys == 2:
            self._coordSys = om.MSpace.kWorld

    def getNextVtx(self, mApi, faceID, vtxID):
        mApi.setIndex(vtxID[1], mApi.VTX)
        mApi.setIndex(faceID, mApi.POLY)
        connectedEdges = mApi.getConnectedComponent(mApi.VTX, mApi.EDGE)
        faceVertices = mApi.getComponent(mApi.POLY, mApi.VTX)
        for edge in connectedEdges:
            mApi.setIndex(edge, mApi.EDGE)
            edgeVertices = mApi.getComponent(mApi.EDGE, mApi.VTX)
            for vtx in edgeVertices:
                if vtx not in vtxID and vtx in faceVertices:
                    return (edge, vtx)

    def walkFace(self, mApi, faceID, vtxID):
        seenVtx = []
        queueItem = []
        while True:
            if vtxID[1] in seenVtx:
                break
            (nEdge, nVtx) = self.getNextVtx(mApi, faceID, vtxID)
            vtxID[0] = vtxID[1]
            vtxID[1] = nVtx
            seenVtx.append(vtxID[0])
            queueItem.append([faceID, nEdge, [vtxID[0], vtxID[1]]])

        return queueItem

    def walkFaceDouble(self, mApiA, faceIDA, vtxIDA, mApiB, faceIDB, vtxIDB):
        seenVtxA = []
        seenVtxB = []
        queueItem = []
        while True:
            if vtxIDA[1] in seenVtxA:
                if vtxIDB[1] not in seenVtxB:
                    om.MGlobal.displayError("FACE MISTMATCHE FOUNDED!")
                break
            if vtxIDB[1] in seenVtxB and vtxIDA[1] not in seenVtxA:
                om.MGlobal.displayError("FACE MISTMATCHE FOUNDED!")
            (nEdgeA, nVtxA) = self.getNextVtx(mApiA, faceIDA, vtxIDA)
            vtxIDA[0] = vtxIDA[1]
            vtxIDA[1] = nVtxA
            (nEdgeB, nVtxB) = self.getNextVtx(mApiB, faceIDB, vtxIDB)
            vtxIDB[0] = vtxIDB[1]
            vtxIDB[1] = nVtxB
            seenVtxA.append(vtxIDA[0])
            seenVtxB.append(vtxIDB[0])
            queueItem.append(
                [
                    mApiA,
                    faceIDA,
                    nEdgeA,
                    [vtxIDA[0], vtxIDA[1]],
                    mApiB,
                    faceIDB,
                    nEdgeB,
                    [vtxIDB[0], vtxIDB[1]],
                ]
            )

        return queueItem

    def getOppositeFace(self, mApi, faceId, edgeId):
        mApi.setIndex(edgeId, mApi.EDGE)
        faces = mApi.getConnectedComponent(mApi.EDGE, mApi.POLY)
        for face in faces:
            if face != faceId:
                return face

    def pickWalkTwoMesh(self, f1, f2, vtxA, vtxB):
        mA = mayaApiHelper.mayaApiHelper(self._meshA)
        mB = mayaApiHelper.mayaApiHelper(self._meshB)
        mA.initObject()
        mB.initObject()
        seenEdges = []
        benchmarkStart = time.time()
        numEdges = mA.mesh.numEdges()
        queues = self.walkFaceDouble(mA, f1, vtxA, mB, f2, vtxB)
        gMainProgressBar = mel.eval("$tmp = $gMainProgressBar")
        cmds.progressBar(
            gMainProgressBar,
            edit=True,
            beginProgress=True,
            isInterruptable=True,
            status='"Pick Walking Mesh ...',
            maxValue=numEdges,
        )
        while True:
            if cmds.progressBar(gMainProgressBar, query=1, isCancelled=1):
                break
            if queues == []:
                break
            for queue in queues:
                (
                    mApiA,
                    faceIDA,
                    edgeIDA,
                    vtxIDA,
                    mApiB,
                    faceIDB,
                    edgeIDB,
                    vtxIDB,
                ) = queue
                if edgeIDA not in seenEdges:
                    seenEdges.append(edgeIDA)
                    nFaceA = self.getOppositeFace(mApiA, faceIDA, edgeIDA)
                    nFaceB = self.getOppositeFace(mApiB, faceIDB, edgeIDB)
                    myPoint = om.MPoint()
                    mApiA.mesh.getPoint(vtxIDA[1], myPoint, self._coordSys)
                    mApiB.mesh.setPoint(vtxIDB[1], myPoint, self._coordSys)
                    mApiA.mesh.getPoint(vtxIDA[0], myPoint, self._coordSys)
                    mApiB.mesh.setPoint(vtxIDB[0], myPoint, self._coordSys)
                    if nFaceA and nFaceB:
                        queues = queues + self.walkFaceDouble(
                            mApiA, nFaceA, vtxIDA, mApiB, nFaceB, vtxIDB
                        )
                        cmds.progressBar(gMainProgressBar, edit=True, step=1)

                queues.remove(queue)

        cmds.progressBar(gMainProgressBar, edit=True, endProgress=1)
        om.MGlobal.displayInfo ("DONE! Thank mapping successfully! Done in: {} Seconds".format(time.time() - benchmarkStart))
        om.MGlobal.displayInfo ("DONE! Thank mapping successfully! Done in: {} Minutes".format((time.time() - benchmarkStart) / 60))
        cmds.displaySmoothness(
            self._meshB, du=0, dv=0, pointsWire=4, pointsShaded=1, polygonObject=1
        )
        cmds.refresh()