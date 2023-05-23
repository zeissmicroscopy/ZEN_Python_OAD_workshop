- [General Remarks](#general-remarks)
  - [Prerequisites](#prerequisites)
  - [Content](#content)
  - [Read, process and write CZIs using pylibCZIrw and cztile](#read-process-and-write-czis-using-pylibczirw-and-cztile)
  - [Create a simple APEER Module](#create-a-simple-apeer-module)
  - [Train a Deep-Learning Model in APEER](#train-a-deep-learning-model-in-apeer)
  - [Use the model in your python code](#use-the-model-in-your-python-code)
  - [Use the model inside Napari (optional)](#use-the-model-inside-napari-optional)
  - [Train your own model and package it a using the czmodel package](#train-your-own-model-and-package-it-a-using-the-czmodel-package)
  - [Using the czitools package (experimental)](#using-the-czitools-package-experimental)
  - [Control ZEN via TCP-IP](#control-zen-via-tcp-ip)
- [Disclaimer](#disclaimer)



# General Remarks

This repository contains all the material for the workshop held during the ZEN & Python & OAD Workshop.

***

## Prerequisites

To run the notebooks locally it is recommended to create a fresh conda environment. Please feel to use the provided [YML file](workshop/notebooks/zen_python.yml) (at your own risk) to create such an environment:

    conda env create --file zen_python.yml

> Important: If one wants to test the labeling & training directly on [arivis Cloud] or create a module it is required to have an account.

## Content

The workshop is focusing on various tools and python packages published be ZEISS for reading CZI images, exchanging Deep-Learning models and general image processing The following topics will be covered:

* Read, process and write CZIs using [pylibCZIrw] and [cztile]
* Create a simple [arivisCloud] Module
* Train a Deep-Learning Model in [arivisCloud]
* Use the model in your python code
* Use the model inside [Napari]
* Train your own model and package it a using the [czmodel] package
* Using [czitools] package (experimental)
* Control ZEN via TCP-IP (experimental)

## Read, process and write CZIs using pylibCZIrw and cztile

This package provides a simple and easy-to-use Python wrapper for [libCZI] - a cross-platform C++ library to read and write multi-dimensional CZI image documents.

* At the moment, **pylibCZIrw** completely abstracts away the subblock concept, both in the reading and in the writing APIs.
* If pylibCZIrw is extended in the future to support subblock-based access (e.g. accessing acquisition tiles), this API must not be altered.
* The core concept of pylibCZIrw is focussing on reading and writing 2D image planes by specifying the dimension indices and its location in order to only read or write **what is really needed**.

* [Usage oy pylibCZIrw](./workshop/notebooks/Using_pylibCZIrw_3_4_0.ipynb)

For more detailed information refer to the pylibCZIrw-documentation.html shipped with the source distribution of this package (see the **Download files** section).


## Create a simple APEER Module

the [arivisCloud] platform does not allow to train deep learning models but also has tools to create so-called arivis Cloud modules and even workflows built upon a container infrastructure.

![arivis Cloud Architecture](./images/apeer_architecture.png)

In short - APEER modules are Docker containers with a UI specification that allows using them on APEER or inside the ZEN software platform. For details please visit: **[APEER Architecture and Modules](https://docs.apeer.com/create-modules/the-apeer-architecture)**

![APEER Module - UI Creation](./images/apeer_module_ui.png)

A simple example module based on python can be found here: **[APEER - Simple Python Module](./workshop/apeer_module_example/README.md)**

Please follow the instruction on how to create an [APEER] module using the built-in documentation and copy this code into your own module repository.

## Train a Deep-Learning Model in APEER

The general idea is to learn how to label a dataset on [arivisCloud] which will be shared among the participants.

Dataset Name: **cyto2022_nuclei**

![Annotated Dataset on APEER](./images/apeer_dataset_nuc.png)

* label some nuclei "precisely"
* label background areas and edges
* embrace the idea of partial labeling

![Partial Annotation on APEER](./images/APEER_annotation_auto_background.gif)

* start a training to get a trained model as a *.czann file

Remark: To save time the modelfile: **cyto2022_nuc.czann** will be provided

For more detailed information please visit: **[APEER Docs - Partial Annotations](https://docs.apeer.com/machine-learning/annotation-guidelines)**

## Use the model in your python code

Once the model is trained it can be downloaded directly to your hard disk and used to segment images.

* [Run a prediction using a *.czann file](./workshop/notebooks/run_prediction_from_czann.ipynb)

***

## Use the model inside Napari (optional)

In order to use such a model one needs a running python environment with [Napari] and the napari-czann-segment plugin installed.

It can install it via [pip]:

    pip install napari-czann-segment

For more detailed information about the plugin please go to: [Napari Hub - napari-czann-segment](https://www.napari-hub.org/plugins/napari-czann-segment)

![Train on arivis Cloud and use model in Napari](https://github.com/sebi06/napari-czann-segment/raw/main/readme_images/Train_APEER_run_Napari_CZANN_no_highlights_small.gif)


***

## Train your own model and package it a using the czmodel package

The package provides simple-to-use conversion tools to generate a CZANN file from a [PyTorch], 
[TensorFlow] or [ONNX] model that resides in memory or on disk to be usable in the
ZEN, arivis Cloud, APEER, Vison4D software platforms and also in your own code. For details and more information examples please go to: [czmodel]

* [Train a simple model and package as *.czann file](./workshop/notebooks/SingleClassSemanticSegmentation_PyTorch.ipynb)

***

## Using the czitools package (experimental)

For details please visit: [czitools]

* [Read CZI metadata](./workshop/notebooks/read_czi_metadata.ipynb)

* [Show CZI Planetable](./workshop/notebooks/show_czi_surface.ipynb)

* [Save CZI as OME_ZARR](./workshop/notebooks/omezarr_from_czi_5d.ipynb)

## Control ZEN via TCP-IP

For details please check: [TCP-IP Interface](https://github.com/zeiss-microscopy/OAD/tree/master/Interfaces/TCP-IP_interface)


# Disclaimer

This content of this repository is free to use for everybody. Carl Zeiss Microscopy GmbH's ZEN software undertakes no warranty concerning the use of those scripts, image analysis settings and ZEN experiments. Use them on your own risk.

**By using any of those examples you agree to this disclaimer.**

Version: 2023.05.23

Copyright (c) 2023 Carl Zeiss AG, Germany. All Rights Reserved.


[Napari]: https://github.com/napari/napari
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
[pylibCZIrw]: https://pypi.org/project/pylibCZIrw/
[czmodel]: https://pypi.org/project/czmodel/
[cztile]: https://pypi.org/project/cztile/
[arivisCloud]: https://www.apeer.com
[napari-czann-segment]: https://github.com/sebi06/napari_czann_segment
[CZI]: https://www.zeiss.com/microscopy/int/products/microscope-software/zen/czi.html
[PyTorch]: https://pytorch.org/
[TensorFlow]: https://www.tensorflow.org/
[ONNX]: https://onnx.ai/
[libCZI]: https://github.com/ZEISS/libczi
[CytoData2022]: https://alleninstitute.org/what-we-do/cell-science/events-training/cytodata-symposium-2022/
[czitools]: https://pypi.org/project/czitools/
