:orphan:

.. command:

~~~~~~~~~~~~~~~~~~~~~~
Launching a processing
~~~~~~~~~~~~~~~~~~~~~~

Commands
********

The main file is located in workflows and is called segment_pnh.py and should be called like a python script:

.. code:: bash

    $ python workflows/segment_pnh.py

**N.B. if you have installed the pypi version (e.g. using pip install skullTo3d) or a docker/singularity version, you can replace the previous command by the following command:**

.. code:: bash

    $ segment_pnh



For container (docker and singularity), here are some examples - add your proper bindings:

.. code:: bash

    $ docker run -B binding_to_host:binding_guest macatools/macapype:latest segment_pnh

.. code:: bash

    $ singularity run -v binding_to_host:binding_guest /path/to/containers/macapype_v0.0.4.1.sif segment_pnh

Expected input data
*******************


All the data have to be in BIDS format to run properly (see `BIDS specification <https://bids-specification.readthedocs.io/en/stable/index.html>`_ for more details)

In particular:

* ``_T1w`` (BIDS) extension is expected for T1 weighted images (BIDS)
* ``_T2w`` (BIDS) extension is expected for T2 weighted images (BIDS)

.. image:: ./img/images/BIDS_orga.jpg
    :width: 600
    :align: center

**Note** : All files with the same extension (T1w or T2w) will be aligned to the first one and averaged


Command line parameters
***********************

--------------------
mandatory parameters
--------------------

* ``-data`` : path to your data dataset (existing BIDS format directory)
* ``-out`` : path to the output results (an existing path)
* ``-soft`` : can be one of these : SPM or ANTS ( **NB:** SPM requires a specific version of macapype/skullTo3d, not available by default)

  For ``-soft`` value, it is possible to add some key words (e.g. ``-soft ANTS_robustreg_prep``) all these options are available (to place after SPM or ANTS, e.g) and will change the brain extraction:

  * ``_4animal`` :  will use bet4animal (FSL) for brain extraction, for faster computation (by default atlas_brex is used)
  * ``_quick`` : will use hd-bet (Deep Learning) for brain extraction, for faster computation (by default atlas_brex is used)
  **NB: ** hd-bet requires a specific version of macapype/skullTo3d, not available by default

  This option should be used if the coregistration to template in preparation is not performed correctly:

  * ``_robustreg`` (at the end) to have a more robust registration (in two steps)

  Finally, these option are available (to place after SPM or ANTS) and will modify the parameters but can be launched in sequence:

  * ``_test`` : (at the end) to check if the full pipeline is coherent (will only generate the graph.dot and graph.png)
  * ``_prep`` (at the end) will perform data preparation (no brain extraction and segmentation)
  * ``_noseg`` (at the end) will perform data preparation and brain extraction (no segmentation)

--------------------
exclusive parameters
--------------------
*(but one is mandatory)*

* ``-params`` : *(mandatory if -species is omitted)* a json file specifiying the global parameters of the analysis. See :ref:`Parameters <params>` for more details
* ``-species`` : *(mandatory if -params is omitted)* followed the NHP species corresponding to the image, e.g. {macaque | marmo | baboon | chimp}

**NB** : marmoT2 can be used for segmenting from the T2w image (by default, T1w is used for marmo)

**NB** : baboon0, baboon1, baboon2 baboon3 can be used for template `Baba21 <doi:10.18112/openneuro.ds005424.v1.0.0>`_
and matching

**NB** : some templates are available in downgraded versions: baboon1_0p6, baboon2_0p6 baboon3_0p6 and macaque_0p5 and show significant decrease in processing time with low redection in quality. However, not all combinations are available

-------------------
optional parameters
-------------------
*(but highly recommanded)*

* ``-dt`` : specifies the datatype available to perform brain segmentation (can be "T1", or "T1 T2")

**Note** : default is T1 if the attribute is omitted

* ``-deriv`` : creates a derivatives directory, with all important files, properly named following BIDS derivatives convertion. See :ref:`Derivatives <derivatives>` for a descrition of the outputs

* ``-padback`` : exports most important files in native (original) space

------------------------
more optional parameters
------------------------

* ``-indiv`` or ``-indiv_params`` : a json file overwriting the default parameters (both macapype default and parameters specified in -params json file) for specific subjects/sessions. See :ref:`Individual Parameters <indiv_params>` for more details
* ``-sub`` (-subjects), ``-ses`` (-sessions), ``-acq`` (-acquisions), ``-rec`` (-reconstructions) allows to specifiy a subset of the BIDS dataset respectively to a range of subjects, session, acquision types and reconstruction types. The arguments can be listed with space seperator. **Note** if not specified, the full BIDS dataset will be processed
* ``-nprocs`` : an integer, to specifiy the number of processes that should be allocated by the parralel engine of macapype

  * typically equals to the number of subjects*session (i.e. iterables).
  * can be multiplied by 2 if T1*T2 pipelines are run (the first steps at least will benefit from it)
  * default = 4 if unspecified ; if is put to 1, then the sequential processing is used

* ``-mask`` allows to specify a precomputed binary mask file (skipping brain extraction). The best usage of this option is: precomputing the pipeline till brain_extraction_pipe, modify by hand the mask and use the mask for segmentation. Better if only one subject*session is specified (one file is specified at a time...).

**Warning:** the mask should be in the same space as the data. And only works with -soft ANTS so far

Command line examples
*********************

.. code:: bash

    $ python workflows/segment_pnh.py -data ~/Data_maca -out ./local_test -soft ANTS -params params.json

.. code:: bash

    $ python workflows/segment_pnh.py -data ~/Data_maca -out ./local_test -soft ANTS_robustreg -species macaque

.. code:: bash

    $ python workflows/segment_pnh.py -data ~/Data_maca -out ./local_test -soft ANTS -params params.json -sub Apache Baron -ses 01 -rec mean -deriv -padback
