#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import shutil
import subprocess
import tarfile

from distutils.core import setup


__dir__ = os.path.dirname(__file__)
picosat_directory = os.path.join(__dir__, 'picosat')
picosat_library = os.path.join(picosat_directory, 'libpicosat.so')
picosat_download = os.path.join(__dir__, 'picosat.tar.gz')
picosat_target = os.path.join(__dir__, 'verification', 'libpicosat.so')

PICOSAT_NAME = 'picosat-965'
PICOSAT_URL = 'http://fmv.jku.at/picosat/{}.tar.gz'.format(PICOSAT_NAME)


def download_picosat():
    if os.path.exists(picosat_download):
        return
    from urllib.request import urlopen
    print('Downloading PicoSAT...')
    response = urlopen(PICOSAT_URL)
    with open(picosat_download, 'wb') as target:
        target.write(response.read())


def extract_picosat():
    if os.path.exists(picosat_directory):
        return
    download_picosat()
    print('Extracting PicoSAT...')
    with tarfile.open(picosat_download, 'r') as archive:
        archive.extractall(__dir__)
    shutil.move(os.path.join(__dir__, PICOSAT_NAME), os.path.join(__dir__, 'picosat'))


def build_picosat():
    if os.path.exists(picosat_target):
        return
    extract_picosat()
    print('Building PicoSAT...')
    subprocess.call(['sh', 'configure.sh', '-shared'], cwd=picosat_directory)
    subprocess.call(['make'], cwd=picosat_directory)
    shutil.copy(picosat_library, picosat_target)


build_picosat()

setup(
    name='verification',
    version='0.1.0',
    description='Verification Project – Python Libraries',
    author='Maximilian Köhl',
    author_email='mail@koehlma.de',
    url='https://github.com/koehlma/verification',
    packages=['verification'],
    package_data={'verification': ['libpicosat.so']}
)
