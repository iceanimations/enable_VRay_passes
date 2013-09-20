#-------------------------------------------------------------------------------
# Name:        enable_VRay_passes
# Purpose:     To enable or disable the VRay passes (VRayRenderElement)
#
# Author:      Qurban Ali (qurban.ali@iceanimations.com)
#
# Created:     29/12/2012
# Copyright:   (c) ice-animations (Pvt.) Ltd. 2012
# Licence:     <ice-animations>
#-------------------------------------------------------------------------------

import pymel.core as pc
import site
site.addsitedir(r"R:/Python_Scripts")
from plugins import utilities as utl
import enablePasses
reload(enablePasses)
#import plugins.utilities as utl
import PyQt4
from PyQt4 import QtGui, QtCore, uic
import os.path as osp
import time

Form, Base = uic.loadUiType(r"%s\ui\ui.ui"%osp.dirname(enablePasses.__file__))
class UI(Form, Base):
    def __init__(self, parent = utl.getMayaWindow()):
        super(UI, self).__init__(parent)
        self.setupUi(self)
        self.passes = [] # list of passes as checkBox
        self.f = QtGui.QFont("Arial", 10)
        self.refresh()
        self.refreshButton.clicked.connect(self.refresh)

    def refresh(self):
        '''
        refreshes the list of passes in the GUI
        '''
        # if GUI list already contain passes, remove them
        if self.passes:
            for p in self.passes:
                p.deleteLater()
            self.passes[:] = []
        try:
            # list existing passe(s) (VRayRenderElements) and their set(s)
            passesList = pc.ls(type = ['VRayRenderElement', 'VRayRenderElementSet'])
        except RuntimeError:
            pc.warning('vray plugin is not loaded...')
            return
        if passesList:
            self.listPasses(passesList)
        else:
            pc.warning('pass(es) not found...')
            return

    def listPasses(self, passesList):
        '''
        lists all the passes as checkBox within scrollArea on the GUI
        '''
        for passName in passesList:
            # see if the 'pass.enable' is true or false
            enabled = passName.enabled.get()
            ps = QtGui.QCheckBox(str(passName), self)
            ps.setFont(self.f)
            self.passes.append(ps)
            if enabled:
                ps.setChecked(True)
            self.passesLayout.addWidget(ps)
            self.bindClickEvent(ps, self.setEnable, passesList)

    def bindClickEvent(self, btn, func, passesList):
        '''
        binds the click event with the checkBox and calls
        self.setEnable when the user changes the state of checkBox
        '''
        btn.stateChanged.connect(lambda value: func( btn , passesList))

    def setEnable(self, btn, passesList):
        '''
        sets the enable property of the pass according to the checkBox on GUI
        '''
        text = btn.text()
        for p in passesList:
            if text == str(p):
                try:
                    # override the the enable property of pass
                    pc.editRenderLayerAdjustment(p.enabled)
                except RuntimeError:
                    pc.warning('Default layer is selected...')
                    return
                break
        def setEn(val):
            try:
                p.enabled.set(val)
            except general.MayaNodeError:
                pc.warning('Pass does not exists, refresh the list...')
                return
        if btn.isChecked():
            setEn(1)
        else:
            setEn(0)
            
class Thread(QThread):
        

def main():
    global ui
    ui = UI()
    ui.show()
