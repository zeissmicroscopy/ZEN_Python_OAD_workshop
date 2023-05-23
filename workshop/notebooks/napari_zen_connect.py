# -*- coding: utf-8 -*-

#################################################################
# File        : napari_zen_connect.py
# Author      : czsrh
# Date        : 23.05.2023
# Institution : Carl Zeiss Microscopy GmbH
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk. Especially be aware of the fact
# that automated stage movements might damage hardware if
# one starts an experiment and the the system is not setup properly.
# Please check everything in simulation mode first!
#
# Copyright (c) 2023 Carl Zeiss AG, Germany. All Rights Reserved.
#
#################################################################

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFileSystemModel,
    QFileDialog,
    QTreeView,
    QDialogButtonBox,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QAbstractItemView,
    QComboBox,
    QPushButton,
    QLineEdit,
    QLabel,
    QGridLayout,
)

from PyQt5.QtCore import Qt, QDir
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont

import napari
import numpy as np
from czitools import pylibczirw_metadata as czimd
from czitools import pylibczirw_tools as czird
from czitools import misc, napari_tools
import os
from zencontrol import ZenExperiment, ZenDocuments
from typing import List, Dict, Tuple, Optional, Type, Any, Union, Mapping


class OptionsWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        # Create a grid layout instance
        self.grid_opt = QGridLayout()
        self.grid_opt.setSpacing(10)
        self.setLayout(self.grid_opt)

        # add checkbox to open CZI after the experiment execution
        self.cbox_openczi = QCheckBox("Open CZI after Acquisition", self)
        self.cbox_openczi.setChecked(True)
        self.cbox_openczi.setStyleSheet(
            "font:bold;" "font-size: 10px;" "width :14px;" "height :14px;"
        )
        self.grid_opt.addWidget(self.cbox_openczi, 0, 0)


class StartExperiment(QWidget):
    def __init__(self, expfiles_short, savefolder=r"c:\temp", default_cziname="myimage.czi"):
        super(QWidget, self).__init__()

        self.expfiles_short = expfiles_short
        self.savefolder = savefolder

        # Create a grid layout instance
        self.grid_exp = QGridLayout()
        self.grid_exp.setSpacing(10)
        self.setLayout(self.grid_exp)

        # add widgets to the grid layout
        self.expselect = QComboBox(self)
        self.expselect.addItems(self.expfiles_short)
        self.expselect.setStyleSheet("font: bold;" "font-size: 10px;")
        self.grid_exp.addWidget(self.expselect, 0, 0)

        self.startexpbutton = QPushButton("Run Experiment")
        self.startexpbutton.setStyleSheet(
            "font: bold;"
            # "background-color: red;"
            "font-size: 10px;"
            # "height: 48px;width: 120px;"
        )
        self.grid_exp.addWidget(self.startexpbutton, 0, 1)

        self.namelabel = QLabel(self)
        self.namelabel.setText("Save Experiment result as CZI :")
        self.namelabel.setStyleSheet("font: bold;" "font-size: 10px;" "")
        self.grid_exp.addWidget(self.namelabel, 1, 0)

        self.nameedit = QLineEdit(self)
        self.nameedit.setText(default_cziname)
        self.nameedit.setFixedWidth(200)
        self.nameedit.setStyleSheet("font: bold;" "font-size: 10px;")
        self.grid_exp.addWidget(self.nameedit, 1, 1)

        # Set the layout on the application's window
        self.startexpbutton.clicked.connect(self.on_click)

    def on_click(self):
        
        # get name of the selected experiment
        current_exp = self.expselect.currentText()
        print("Selected ZEN Experiment : ", current_exp)

        # get the desired savename
        desired_cziname = self.nameedit.text()

        # disable the button while the experiment is running
        self.startexpbutton.setText("Running ...")

        # not nice, but this "redraws" the button
        # QtCore.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

        # initialize the experiment with parameters
        czexp = ZenExperiment(
            experiment=current_exp, savefolder=self.savefolder, cziname=desired_cziname
        )

        # start the actual experiment
        self.saved_czifilepath = czexp.startexperiment()
        print("Saved CZI : ", self.saved_czifilepath)

        # enable the button again when experiment is over
        self.startexpbutton.setEnabled(True)
        self.startexpbutton.setText("Run Experiment")

        # not nice, but this "redraws" the button
        QtWidgets.QApplication.processEvents()

        # open the just acquired CZI and show it inside napari viewer
        if self.saved_czifilepath is not None:
            open_image_stack(self.saved_czifilepath)


def open_image_stack(filepath: str):
    """Open a CZI file using pylibCZIrw and display it using napari

    :param path: filepath of the image
    :type path: str
    """

    if os.path.isfile(filepath):
        # remove existing layers from napari
        # viewer.layers.select_all()
        # viewer.layers.remove_selected()

        # return array with dimension order STZCYXA
        array6d, mdata, dimstring6d = czird.read_6darray(filepath,
                                                         dimorder="STCZYX",
                                                         output_dask=False,
                                                         remove_Adim=True)

        # show array inside napari viewer
        layers = napari_tools.show(
            viewer,
            array6d,
            mdata,
            dim_string=dimstring6d,
            blending="additive",
            contrast="from_czi",
            gamma=0.85,
            add_mdtable=True,
            name_sliders=True,
        )


###########################################################

if __name__ == "__main__":
    # make sure this location is correct if you specify this
    workdir = r"f:\Testdata_Zeiss\CZI_Testfiles"

    if os.path.isdir(workdir):
        print("SaveFolder : ", workdir, "found.")
    if not os.path.isdir(workdir):
        print("SaveFolder : ", workdir, "not found.")

    # specify directly or try to discover folder automatically
    zenexpfolder = r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups"

    # check if the ZEN experiment folder was found
    expfiles_long = []
    expfiles_short = []

    if os.path.isdir(zenexpfolder):
        print("ZEN Experiment Setups Folder :", zenexpfolder, "found.")
        # get lists with existing experiment files
        expdocs = ZenDocuments()
        expfiles_long, expfiles_short = expdocs.getfilenames(folder=zenexpfolder, pattern="*.czexp")

    if not os.path.isdir(zenexpfolder):
        print("ZEN Experiment Setups Folder :", zenexpfolder, "not found.")

    # default for saving an CZI image after acquisition
    default_cziname = "myimage.czi"

    # initialize the napari viewer
    print("Initializing Napari Viewer ...")

    viewer = napari.Viewer()

    # create the widget elements to be added to the napari viewer

    # table for the metadata and for options
    # mdbrowser = napari_tools.TableWidget()
    checkboxes = OptionsWidget()

    # widget to start an experiment in ZEN remotely
    expselect = StartExperiment(expfiles_short, savefolder=workdir, default_cziname=default_cziname)

    # add widget to activate the dask delayed reading
    cbwidget = viewer.window.add_dock_widget(checkboxes, name="checkbox", area="bottom")

    # add the Table widget for the metadata
    # mdwidget = viewer.window.add_dock_widget(mdbrowser, name="mdbrowser", area="right")

    # add the Experiment Selector widget
    expwidget = viewer.window.add_dock_widget(expselect, name="expselect", area="bottom")

    napari.run()
