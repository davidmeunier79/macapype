:orphan:

.. _docker_install:

******
docker
******


Dockerfile
-----------

Downloading Dockerfile and building an image:

.. code:: bash

    # Downloading Dockerfile
    $ wget https://github.com/Macatools/macapype/blob/master/Dockerfile

    # Building your image from the Dockerfile
    $ docker build -t macapype_docker .

Example of workflows (see :ref:`Workflows <workflows>` for more explanations):

.. code:: bash

    # Given your dataset follows BIDS standard and is located in ~/Data_maca
    # - running the workflow ants_based on full dataset
    $ docker run -ti -v ~/Data_maca:/data/macapype macapype_docker python /opt/packages/macapype/workflows/segment_pnh.py -soft ANTS -data /data/macapype -out /data/macapype -params /opt/packages/macapype/workflows/params_segment_pnh_ants_based.json

    # - running the workflow segment_multi_pnh_ants_based on one subject/session
    $ docker run -ti -v ~/Data_maca:/data/macapype macapype_docker python /opt/packages/macapype/workflows/segment_pnh.py -soft ANTS -data /data/macapype -out /data/macapype -subjects Apache -ses 01 -params /opt/packages/macapype/workflows/params_segment_pnh_ants_based.json

Docker image
------------

A docker image can also be downloaded directly from `DockerHub repo <https://hub.docker.com/r/macatools/macapype>`_ :

.. code:: bash

    $ docker pull macatools/macapype:latest

    # Given your dataset follows BIDS standard and is located in ~/Data_maca
    # - running the workflow ants_based on full dataset
    $ docker run -ti -v ~/Data_maca:/data/macapype macatools/macapype:latest python /opt/packages/macapype/workflows/segment_pnh.py -soft ANTS -data /data/macapype -out /data/macapype -params /opt/packages/macapype/workflows/params_segment_pnh_ants_based.json

    # - running the workflow segment_multi_pnh_ants_based on one subject/session
    $ docker run -ti -v ~/Data_maca:/data/macapype macatools/macapype:latest python /opt/packages/macapype/workflows/segment_pnh.py -soft ANTS -data /data/macapype -out /data/macapype -subjects Apache -ses 01 -params /opt/packages/macapype/workflows/params_segment_pnh_ants_based.json

