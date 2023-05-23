## Arivis Cloud (formerly APEER) Module Example: Filter CZI Image

### Introduction

This is an example python module. The aim of the module is filter an CZI image.
This module has 2 inputs:

* **input_image** - CZI image file to be processed
* **filter_kernel_size** - integer specifying the kernel size of mean filter

![Simple Python Module - Filter CZI Image](Module_Image.png)

The module consists of several files:

* **[Dockerfile](Dockerfile)** A dockerfile is a script, composed of various commands to automatically perform actions on a base image in order to create a new docker image. The dockerfile, that comes with this example, is very well commented and is very easy to understand.

* **[module_specification.json](module_specification.json)** This files defines the inputs and outputs as well as the ui components of the module. [More info](https://docs.apeer.com/)

* **[apeer_main.py](apeer_main.py)** This is the entrypoint for the module. It calls the actual processing function in `_filter_image.py`

* **[apply_filter.py](apply_filter.py)** This is the file which contains the actual processing this module does. It can be used and tested independent of any arivis Cloud functionality.

* **[requirements.txt](requirements.txt)** This file contains the list of libraries that are required by Python and that should be installed during the docker build process. You can see its use in DockerFile.

* **[wfe.env](wfe.env)** This file allows to set the input parameters for the docker_make.sh file.

For more details and tutorial please visit the [APEER Docs](https://docs.apeer.com/create-modules/the-apeer-architecture)


## FAQs

### How to trigger a build

Triggering a build of your module on arivis Cloud is quite simple. You just have to push some code on the master branch of your repository.

### Where do I see my build result

You can find the build of your module under the module page.

### What happens when the build is done

If the build is successful the module is pushed as draft into your workspace on the platform.
