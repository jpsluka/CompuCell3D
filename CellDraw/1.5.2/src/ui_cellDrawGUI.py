# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cellDrawGUI.ui'
#
# Created: Fri Nov  4 16:19:33 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CellDrawGUI(object):
    def setupUi(self, CellDrawGUI):
        CellDrawGUI.setObjectName(_fromUtf8("CellDrawGUI"))
        CellDrawGUI.setEnabled(True)
        CellDrawGUI.resize(996, 704)
        CellDrawGUI.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        CellDrawGUI.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(CellDrawGUI)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        CellDrawGUI.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(CellDrawGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 996, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        CellDrawGUI.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(CellDrawGUI)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        CellDrawGUI.setStatusBar(self.statusbar)
        self.inputControlsDockWidget = QtGui.QDockWidget(CellDrawGUI)
        self.inputControlsDockWidget.setMinimumSize(QtCore.QSize(180, 432))
        self.inputControlsDockWidget.setObjectName(_fromUtf8("inputControlsDockWidget"))
        self.inputControlsContentsWidget = QtGui.QWidget()
        self.inputControlsContentsWidget.setMinimumSize(QtCore.QSize(180, 400))
        self.inputControlsContentsWidget.setObjectName(_fromUtf8("inputControlsContentsWidget"))
        self.graphicsScenePIFF_checkBox = QtGui.QCheckBox(self.inputControlsContentsWidget)
        self.graphicsScenePIFF_checkBox.setGeometry(QtCore.QRect(10, 180, 161, 23))
        self.graphicsScenePIFF_checkBox.setObjectName(_fromUtf8("graphicsScenePIFF_checkBox"))
        self.pickColorRegion_checkBox = QtGui.QCheckBox(self.inputControlsContentsWidget)
        self.pickColorRegion_checkBox.setGeometry(QtCore.QRect(10, 200, 161, 23))
        self.pickColorRegion_checkBox.setObjectName(_fromUtf8("pickColorRegion_checkBox"))
        self.ignoreWhiteRegions_checkBox = QtGui.QCheckBox(self.inputControlsContentsWidget)
        self.ignoreWhiteRegions_checkBox.setGeometry(QtCore.QRect(10, 220, 161, 23))
        self.ignoreWhiteRegions_checkBox.setObjectName(_fromUtf8("ignoreWhiteRegions_checkBox"))
        self.ignoreBlackRegions_checkBox = QtGui.QCheckBox(self.inputControlsContentsWidget)
        self.ignoreBlackRegions_checkBox.setGeometry(QtCore.QRect(10, 240, 161, 23))
        self.ignoreBlackRegions_checkBox.setObjectName(_fromUtf8("ignoreBlackRegions_checkBox"))
        self.textBrowser = QtGui.QTextBrowser(self.inputControlsContentsWidget)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QtCore.QRect(10, 270, 161, 51))
        self.textBrowser.setAcceptDrops(False)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.label_7 = QtGui.QLabel(self.inputControlsContentsWidget)
        self.label_7.setGeometry(QtCore.QRect(10, 150, 161, 23))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setFrameShape(QtGui.QFrame.Panel)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.line = QtGui.QFrame(self.inputControlsContentsWidget)
        self.line.setGeometry(QtCore.QRect(10, 130, 161, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_8 = QtGui.QLabel(self.inputControlsContentsWidget)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 161, 23))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setFrameShape(QtGui.QFrame.Panel)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.graphicsScenePIFF_saveMetadataCheckbox = QtGui.QCheckBox(self.inputControlsContentsWidget)
        self.graphicsScenePIFF_saveMetadataCheckbox.setGeometry(QtCore.QRect(10, 40, 161, 23))
        self.graphicsScenePIFF_saveMetadataCheckbox.setObjectName(_fromUtf8("graphicsScenePIFF_saveMetadataCheckbox"))
        self.graphicsScenePIFF_saveMetadataCheckbox_2 = QtGui.QCheckBox(self.inputControlsContentsWidget)
        self.graphicsScenePIFF_saveMetadataCheckbox_2.setGeometry(QtCore.QRect(10, 60, 161, 23))
        self.graphicsScenePIFF_saveMetadataCheckbox_2.setObjectName(_fromUtf8("graphicsScenePIFF_saveMetadataCheckbox_2"))
        self.inputControlsDockWidget.setWidget(self.inputControlsContentsWidget)
        CellDrawGUI.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.inputControlsDockWidget)
        self.action_Open_Image = QtGui.QAction(CellDrawGUI)
        self.action_Open_Image.setObjectName(_fromUtf8("action_Open_Image"))
        self.action_Export_PIFF = QtGui.QAction(CellDrawGUI)
        self.action_Export_PIFF.setObjectName(_fromUtf8("action_Export_PIFF"))
        self.action_Exit = QtGui.QAction(CellDrawGUI)
        self.action_Exit.setObjectName(_fromUtf8("action_Exit"))
        self.action_Preferences = QtGui.QAction(CellDrawGUI)
        self.action_Preferences.setObjectName(_fromUtf8("action_Preferences"))
        self.action_Open_PIFF = QtGui.QAction(CellDrawGUI)
        self.action_Open_PIFF.setObjectName(_fromUtf8("action_Open_PIFF"))
        self.action_Open_DICOM = QtGui.QAction(CellDrawGUI)
        self.action_Open_DICOM.setObjectName(_fromUtf8("action_Open_DICOM"))
        self.action_Save_Scene = QtGui.QAction(CellDrawGUI)
        self.action_Save_Scene.setObjectName(_fromUtf8("action_Save_Scene"))
        self.action_Open_Scene = QtGui.QAction(CellDrawGUI)
        self.action_Open_Scene.setObjectName(_fromUtf8("action_Open_Scene"))
        self.action_New_Scene = QtGui.QAction(CellDrawGUI)
        self.action_New_Scene.setObjectName(_fromUtf8("action_New_Scene"))
        self.action_Open_Multi_Page_TIFF = QtGui.QAction(CellDrawGUI)
        self.action_Open_Multi_Page_TIFF.setObjectName(_fromUtf8("action_Open_Multi_Page_TIFF"))
        self.action_Import_Image_Sequence = QtGui.QAction(CellDrawGUI)
        self.action_Import_Image_Sequence.setObjectName(_fromUtf8("action_Import_Image_Sequence"))
        self.menuFile.addAction(self.action_New_Scene)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Open_Scene)
        self.menuFile.addAction(self.action_Open_Image)
        self.menuFile.addAction(self.action_Import_Image_Sequence)
        self.menuFile.addAction(self.action_Open_DICOM)
        self.menuFile.addAction(self.action_Open_Multi_Page_TIFF)
        self.menuFile.addAction(self.action_Open_PIFF)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Save_Scene)
        self.menuFile.addAction(self.action_Export_PIFF)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Preferences)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Exit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(CellDrawGUI)
        QtCore.QMetaObject.connectSlotsByName(CellDrawGUI)

    def retranslateUi(self, CellDrawGUI):
        CellDrawGUI.setWindowTitle(QtGui.QApplication.translate("CellDrawGUI", "CellDraw", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("CellDrawGUI", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsScenePIFF_checkBox.setText(QtGui.QApplication.translate("CellDrawGUI", "PIFF from Region Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.pickColorRegion_checkBox.setText(QtGui.QApplication.translate("CellDrawGUI", "Pick color region", None, QtGui.QApplication.UnicodeUTF8))
        self.ignoreWhiteRegions_checkBox.setText(QtGui.QApplication.translate("CellDrawGUI", "Ignore white regions", None, QtGui.QApplication.UnicodeUTF8))
        self.ignoreBlackRegions_checkBox.setText(QtGui.QApplication.translate("CellDrawGUI", "Ignore black regions", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("CellDrawGUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Click on an image color in the Input Image Layer to generate a corresponding region in the PIFF Scene.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("CellDrawGUI", "Input Image Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("CellDrawGUI", "PIFF Output Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsScenePIFF_saveMetadataCheckbox.setToolTip(QtGui.QApplication.translate("CellDrawGUI", "Selecting the \"Save metadata in PIFF\" checkbox will cause the saved PIFF files to include XML-formatted information about the dataset dimensions, units, etc.\n"
"This information is ignored by CompuCell3D releases 3.5.0 and earlier.", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsScenePIFF_saveMetadataCheckbox.setText(QtGui.QApplication.translate("CellDrawGUI", "Save metadata in PIFF", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsScenePIFF_saveMetadataCheckbox_2.setToolTip(QtGui.QApplication.translate("CellDrawGUI", "Selecting \"Metadata in header\" will position the XML metadata at the beginning of saved PIFF files.\n"
"Note: this will save PIFF files that are not readable by CompuCell3D release 3.5.0 and earlier.\n"
"To save PIFF files in a format compatible with older CompuCell3D releases, de-select this checkbox.\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsScenePIFF_saveMetadataCheckbox_2.setText(QtGui.QApplication.translate("CellDrawGUI", "Metadata in header", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Image.setText(QtGui.QApplication.translate("CellDrawGUI", "Import &Image", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Image.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+Shift+I", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export_PIFF.setText(QtGui.QApplication.translate("CellDrawGUI", "Export &PIFF", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export_PIFF.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Exit.setText(QtGui.QApplication.translate("CellDrawGUI", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Exit.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Preferences.setText(QtGui.QApplication.translate("CellDrawGUI", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_PIFF.setText(QtGui.QApplication.translate("CellDrawGUI", "Import PIFF", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_PIFF.setToolTip(QtGui.QApplication.translate("CellDrawGUI", "Open PIFF File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_PIFF.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+Shift+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_DICOM.setText(QtGui.QApplication.translate("CellDrawGUI", "Import DICOM", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_DICOM.setToolTip(QtGui.QApplication.translate("CellDrawGUI", "Open DICOM file", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_DICOM.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+Alt+Shift+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_Scene.setText(QtGui.QApplication.translate("CellDrawGUI", "&Save Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_Scene.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Scene.setText(QtGui.QApplication.translate("CellDrawGUI", "&Open Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Scene.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Scene.setText(QtGui.QApplication.translate("CellDrawGUI", "&New Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Scene.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Multi_Page_TIFF.setText(QtGui.QApplication.translate("CellDrawGUI", "Import Multi-Page TIFF", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Multi_Page_TIFF.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+Shift+T", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Import_Image_Sequence.setText(QtGui.QApplication.translate("CellDrawGUI", "Import Image Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Import_Image_Sequence.setShortcut(QtGui.QApplication.translate("CellDrawGUI", "Ctrl+Alt+I", None, QtGui.QApplication.UnicodeUTF8))

