#!/usr/bin/env bash

rm -rf build dist pusnowlib.egg-info
python3 setup.py sdist bdist_wheel
twine upload dist/*