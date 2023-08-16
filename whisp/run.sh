#!/usr/bin/env bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(dirname $(poetry run python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))/lib

poetry run python main.py