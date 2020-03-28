#!/bin/bash

prefix=$1
src_lang=$2
trg_lang=$3

onmt_preprocess \
    --train_src $1/${src_lang}.txt \
    --train_tgt $1/${trg_lang}.txt \
    --src_words_min_frequency 2 \
    --tgt_words_min_frequency 2 \
    --shuffle \
    --save_data ${src_lang}_${trg_lang}_data