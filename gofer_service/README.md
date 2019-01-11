# Gofer_nb service

This repo contains a tornado flask app that accepts .ipynb files and grades them in a dockerized environment. Assuming you are running a Jupyterhub, you can ask it to run this app as a service so that you don't have to run it as a standalone. The grade out of 1 will be returned.

Paired with the submit_extension, the user simply clicks a button to submit their notebook and will receive a popup with their submission score.

# Configuration

There are three critical steps to set up ahead of time for this to work.

First, the ipynb notebooks should have the metadata for which assignment they are. In the case of Data 8x, there are two pieces of information that are relevant, the section and the lab number.

Second, tests should be placed in a location that can be specified by the assignment metadata. This could simply be done by making the directory structure correspond to numbers, or by having a python dict from assignment names to test directories.

Third, a docker image should be made that specifies the user environment. This prevents their (arbitrary) notebook code from being run on the server that hosts everyone.

# Service installation

Instructions can be found here: https://jupyterhub.readthedocs.io/en/stable/reference/services.html#launching-a-hub-managed-service
