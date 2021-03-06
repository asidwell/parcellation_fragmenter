import nibabel as nib
import numpy as np


class Extractor(object):
    """
    Class to extract unique indices of all regions in a
    label / annotation file.
    Parameters:
    - - - - -
    label_file : string
        path to input label or annotation file
    """

    def __init__(self):

        pass

    def get_label_table(self, label_file):

        try:
            label_obj = nib.load(label_file)
            cdata = label_obj.darrays[0].data
            label_table = label_obj.labeltable.get_labels_as_dict()

            rois = list(map(str, label_table.values()))
            rois = [r[2:] for r in rois]
            roi_index = list(label_table.keys())

        except nib.filebasedimages.ImageFileError:
            cdata, ctab, roi_names = nib.freesurfer.io.read_annot(label_file)
            rois = [k.decode('utf-8') for k in roi_names]
            roi_index = [roi_names.index(np.bytes_(n)) for n in rois[1:]]
        else:
            pass
        finally:
            reg2val = dict(zip(rois, roi_index))

        parcels = {reg: np.where(
            cdata == reg2val[reg])[0] for reg in reg2val.keys()}

        return parcels
