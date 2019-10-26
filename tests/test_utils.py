""" Tests for utils module
"""

import os
import os.path as op
from tempfile import TemporaryDirectory

from gofer.utils import cd


def test_cd():
    # Test InGivenDirectory
    cwd = op.realpath(os.getcwd())
    with TemporaryDirectory() as tmpdir:
        # Ok, it's paranoid, but just in case
        tmp_path = op.realpath(tmpdir)
        assert cwd == op.realpath(os.getcwd())
        assert tmp_path != cwd
        with cd(tmpdir):
            assert tmp_path == op.realpath(os.getcwd())
        assert cwd == op.realpath(os.getcwd())
