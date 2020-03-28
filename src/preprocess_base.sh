#!/bin/bash

prefix=$1
src_lang=$2
trg_lang=$3

onmt_preprocess \
    --train_src $1/${src_lang}_train.txt \
    --train_tgt $1/${trg_lang}_train.txt \
    --valid_src $1/${src_lang}_valid.txt \
    --valid_tgt $1/${trg_lang}_valid.txt \
    --save_data ${src_lang}_${trg_lang}_data \
    --src_words_min_frequency 2 \
    --tgt_words_min_frequency 2

    