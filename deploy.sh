#!/usr/bin/env bash
rm -rf dist
python3 setup.py sdist
twine upload dist/*

# git remote add fury https://tflander@git.fury.io/tflander/esp_net_config.git
# git push fury master
