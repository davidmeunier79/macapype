import os.path as op

import json

from bids.layout import BIDSLayout

import nipype.interfaces.io as nio
import nipype.pipeline.engine as pe

from .utils_nodes import BIDSDataGrabberParams

def create_datasource(data_dir, subjects=None, sessions=None,
                      acquisitions=None, reconstructions=None):
    """ Create a datasource node that have iterables following BIDS format """
    bids_datasource = pe.Node(
        interface=nio.BIDSDataGrabber(),
        name='bids_datasource'
    )

    bids_datasource.inputs.base_dir = data_dir
    bids_datasource.inputs.output_query = {
        'T1': {
            "datatype": "anat", "suffix": "T1w",
            "extension": ["nii", ".nii.gz"]
        },
        'T2': {
            "datatype": "anat", "suffix": "T2w",
            "extension": ["nii", ".nii.gz"]
        }
    }

    layout = BIDSLayout(data_dir)

    # Verbose
    print("BIDS layout:", layout)
    print("\t", layout.get_subjects())
    print("\t", layout.get_sessions())

    if subjects is None:
        subjects = layout.get_subjects()

    if sessions is None:
        sessions = layout.get_sessions()

    iterables = []
    iterables.append(('subject', subjects))

    if sessions != []:
        iterables.append(('session', sessions))

    if acquisitions is not None:
        iterables.append(('acquisition', acquisitions))

    if reconstructions is not None:
        iterables.append(('reconstruction', reconstructions))

    bids_datasource.iterables = iterables

    return bids_datasource


def create_datasource_indiv_params(data_dir, indiv_params, subjects=None,
                                   sessions=None, acquisitions=None,
                                   reconstructions=None):
    """ Create a datasource node that have iterables following BIDS format,
    including a indiv_params file"""

    bids_datasource = pe.Node(
        interface=BIDSDataGrabberParams(indiv_params),
        name='bids_datasource'
    )

    bids_datasource.inputs.base_dir = data_dir
    bids_datasource.inputs.output_query = {
        'T1': {
            "datatype": "anat", "suffix": "T1w",
            "extension": ["nii", ".nii.gz"]
        },
        'T2': {
            "datatype": "anat", "suffix": "T2w",
            "extension": ["nii", ".nii.gz"]
        }
    }

    layout = BIDSLayout(data_dir)

    # Verbose
    print("BIDS layout:", layout)
    print("\t", layout.get_subjects())
    print("\t", layout.get_sessions())

    if subjects is None:
        subjects = layout.get_subjects()

    if sessions is None:
        sessions = layout.get_sessions()

    iterables = []
    iterables.append(('subject', subjects))
    iterables.append(('session', sessions))

    if acquisitions is not None:
        iterables.append(('acquisition', acquisitions))

    if reconstructions is not None:
        iterables.append(('reconstruction', reconstructions))

    bids_datasource.iterables = iterables

    return bids_datasource


def create_datasource_indiv_params_FLAIR(data_dir, indiv_params, subjects=None,
                                         sessions=None, acquisitions=None,
                                         reconstructions=None):
    """ Create a datasource node that have iterables following BIDS format,
    including a indiv_params file"""

    bids_datasource = pe.Node(
        interface=BIDSDataGrabberParams(indiv_params),
        name='bids_datasource'
    )

    bids_datasource.inputs.base_dir = data_dir
    bids_datasource.inputs.output_query = {
        'T1': {
            "datatype": "anat", "suffix": "T1w",
            "extension": ["nii", ".nii.gz"]
        },
        'T2': {
            "datatype": "anat", "suffix": "T2w",
            "extension": ["nii", ".nii.gz"]
        },
        'FLAIR': {
            "datatype": "anat", "suffix": "FLAIR",
            "extension": ["nii", ".nii.gz"]
        },
        'MD': {
            "datatype": "dwi", "acquisition": "MD", "suffix": "dwi",
            "extension": ["nii", ".nii.gz"]
        },
        'b0mean': {
            "datatype": "dwi", "acquisition": "b0mean", "suffix": "dwi",
            "extension": ["nii", ".nii.gz"]
        }
    }

    layout = BIDSLayout(data_dir)

    # Verbose
    print("BIDS layout:", layout)
    print("\t", layout.get_subjects())
    print("\t", layout.get_sessions())

    if subjects is None:
        subjects = layout.get_subjects()

    if sessions is None:
        sessions = layout.get_sessions()

    iterables = []
    iterables.append(('subject', subjects))
    iterables.append(('session', sessions))

    if acquisitions is not None:
        iterables.append(('acquisition', acquisitions))

    if reconstructions is not None:
        iterables.append(('reconstruction', reconstructions))

    bids_datasource.iterables = iterables

    return bids_datasource


def create_datasink(iterables, name = "output"):
    """ Description: reformating relevant outputs

    """

    print("Datasink name: ", name)

    datasink = pe.Node(nio.DataSink(container=name),  # the name of the sub-folder of base_dirctory
               name = 'datasink')

    print (iterables)
    subjFolders = [('_session_%s_subject_%s' % (ses, sub), 'sub-%s/ses-%s/' % (sub, ses))
               for ses in iterables[1][1]
               for sub in iterables[0][1]]

    datasink.inputs.substitutions = subjFolders

    json_regex_subs = op.join(op.dirname(op.abspath(__file__)),
                            "regex_subs.json")

    dict_regex_subs = json.load(open(json_regex_subs))

    print(dict_regex_subs)

    regex_subs = [(key, value) for key, value in dict_regex_subs.items()]

    print(regex_subs)

    datasink.inputs.regexp_substitutions = regex_subs  # (r'(/_.*(\d+/))', r'/run\2')

    return datasink
