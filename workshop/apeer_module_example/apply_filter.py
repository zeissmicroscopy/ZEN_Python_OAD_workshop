import os
from pylibCZIrw import czi as pyczi
from czitools import metadata_tools as czimd
from czitools import misc_tools as misc
from skimage.morphology import disk, rectangle
from skimage import filters
import os
import numpy as np
from tqdm.contrib.itertools import product
from typing import List, Dict, Tuple, Optional, Type, Any, Union
from pathlib import Path


def execute(image_path, filtertype: str = "Median",
            kernelsize: int = 5) -> str:

    # get the image name and create the savepath
    image_name = os.path.basename(image_path)
    savepath = misc.get_fname_woext(image_name) + "_filtered.czi"
    mdata = czimd.CziMetadata(image_path)

    # check if dimensions are None (because the might not exist for that image)
    sizeC = misc.check_dimsize(mdata.image.SizeC, set2value=1)
    sizeZ = misc.check_dimsize(mdata.image.SizeZ, set2value=1)
    sizeT = misc.check_dimsize(mdata.image.SizeT, set2value=1)
    sizeS = misc.check_dimsize(mdata.image.SizeS, set2value=1)

    # open the original CZI document to read 2D image planes
    with pyczi.open_czi(image_path) as czidoc_r:

        # open new CZI document for writing
        with pyczi.create_czi(savepath, exist_ok=True) as czidoc_w:

            # read the image data plane-by-plane
            for s, t, z, c in product(range(sizeS),
                                      range(sizeT),
                                      range(sizeZ),
                                      range(sizeC)):

                # read 2D plane in case there are (no) scenes
                if mdata.image.SizeS is None:
                    img2d = czidoc_r.read(plane={"T": t, "Z": z, "C": c})
                else:
                    img2d = czidoc_r.read(plane={"T": t, "Z": z, "C": c}, scene=s)

                # process the image
                img2d = _filter_image(img2d,
                                      filtertype=filtertype,
                                      kernelsize=kernelsize)

                if mdata.image.SizeS is None:
                    # write 2D plane in case of no scenes
                    czidoc_w.write(img2d, plane={"T": t,
                                                 "Z": z,
                                                 "C": c})
                else:
                    # write 2D plane in case scenes exist
                    czidoc_w.write(img2d, plane={"T": t,
                                                 "Z": z,
                                                 "C": c},
                                   scene=s)

            # write scaling the the new czi
            czidoc_w.write_metadata(scale_x=mdata.scale.X,
                                    scale_y=mdata.scale.Y,
                                    scale_z=mdata.scale.Z)

    print("Finished processing and writing the image.")

    return {"output_image": savepath}


def _filter_image(image2d,
                  filtertype: str = "Median",
                  kernelsize: int = 3) -> np.ndarray:

    # reduce to 2d array
    image2d = np.squeeze(image2d)

    # define the correct calls for the different filter types
    if filtertype == "Median":
        image2d = filters.median(image2d, disk(kernelsize),
                                 mode="reflect")

    if filtertype == "Mean":
        selem = rectangle(kernelsize, kernelsize)
        image2d = filters.rank.mean(image2d, selem=selem)

    if filtertype == "Tophat":
        image2d = filters.rank.tophat(image2d, disk(kernelsize))

    if filtertype == "Bottomhat":
        image2d = filters.rank.bottomhat(image2d, disk(kernelsize))

    # add dimension for CZI pixel type at the end of array - [Y, X, 1]
    image2d = image2d[..., np.newaxis]

    # convert to desired dtype in place
    image2d = image2d.astype(image2d.dtype, copy=False)

    return image2d


# Test Code locally
if __name__ == "__main__":

    #filename = r"Osteosarcoma_01.czi"
    filename = r"T=6_Z=15_CH=2.czi"

    # get the current working directory
    directory = Path(os.getcwd())

    # find the path mathcing the input file and get the path as a string
    d1 = list(directory.rglob("*/input/" + filename))
    file2open = str(d1[0])

    # execute the main function of the module
    out = execute(file2open,
                  filtertype="Median",
                  kernelsize=5)

    print(out)
