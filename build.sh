#!/bin/bash
chmod +x ./setup.py
./setup.py sdist 

./setup.py bdist_wheel
./setup.py bdist_wheel --others
./setup.py bdist_wheel --have-ffmpeg