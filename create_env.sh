#!/usr/bin/env bash
set -e

conda create -y -n made_matching python=3.8
conda run -n made_matching pip install -r requirements.txt
aria2c -x 8 http://files.deeppavlov.ai/embeddings/ft_native_300_ru_wiki_lenta_lemmatize/ft_native_300_ru_wiki_lenta_lemmatize.bin
