
# Copyright (c) 2010 Double Cluepon Software
# Licensed for use under the GPL version 2.0 or later

from setuptools import setup, find_packages

setup(
    name                = "SwfConduit",
    version             = "0.0.1",
    package_dir         = { "" : "lib" },
    packages            = find_packages( "lib" ),
    install_requires    = [ "PyAMF >= .5.1" ],
)
