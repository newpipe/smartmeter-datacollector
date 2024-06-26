#!/usr/bin/env python3
#
# Copyright (C) 2024 Supercomputing Systems AG
# This file is part of smartmeter-datacollector.
#
# SPDX-License-Identifier: GPL-2.0-only
# See LICENSES/README.md for more information.
#
from os import path

from setuptools import find_packages, setup

from smartmeter_datacollector.__version__ import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smartmeter-datacollector",
    version=__version__,
    description="Smart Meter Data Collector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scs/smartmeter-datacollector",
    project_urls={
        "Source": "https://github.com/scs/smartmeter-datacollector",
        "Bug Reports": "https://github.com/scs/smartmeter-datacollector/issues",
        "Pull Requests": "https://github.com/scs/smartmeter-datacollector/pulls",
        "SCS": "https://www.scs.ch",
    },
    author="Supercomputing Systems AG",
    author_email="info@scs.ch",
    maintainer="Supercomputing Systems AG",
    maintainer_email="info@scs.ch",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    license="GPLv2",
    python_requires=">=3.8",
    packages=find_packages(
        exclude=["contrib", "doc", "LICENSES", "scripts", "tests", "tests."]
    ),
    include_package_data=True,
    install_requires=["aioserial==1.3.1; python_version >= '3.6' and python_version < '4.0'", "asyncio-mqtt==0.16.2; python_version >= '3.7'", "certifi==2024.2.2; python_version >= '3.6'", "charset-normalizer==3.3.2; python_full_version >= '3.7.0'", 'gurux-dlms==1.0.150', "idna==3.7; python_version >= '3.5'", 'influxdb==5.3.2', "msgpack==1.0.8; python_version >= '3.8'", 'paho-mqtt==1.6.1', 'pyserial==3.5', "python-dateutil==2.9.0.post0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'pytz==2024.1', "requests==2.31.0; python_version >= '3.7'", "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "urllib3==2.2.1; python_version >= '3.8'"





                      ],
    scripts=["bin/smartmeter-datacollector"],
    zip_safe=True,
    dependency_links=[],
)
