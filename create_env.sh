#!/usr/bin/env bash
set -e

conda create -y -n made_matching python=3.8
conda run -n made_matching pip install -r requirements.txt
