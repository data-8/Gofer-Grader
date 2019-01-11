# Submit Extension

This repo contains the code for a Jupyter notebook extension that sends the JSON of a .ipynb file as an HTML POST request.
Currently, the extension assumes that you are running your course on a Jupyterhub with the `gofer_nb` service running. However, if you are accepting submissions at another URL, you may update the link in `submit_extension.js`.

# Installation

Installation is standard for nbextensions. Run the following commands to install and enable the extension on your jupyter installation. These should be run from the parent directory of this directory.

`jupyter nbextension install --sys-prefix submit_extension`
`jupyter nbextension enable --sys-prefix submit_extension/submit_extension`
To disable the extension, simply run

`jupyter nbextension disable --sys-prefix submit_extension/submit_extension`
