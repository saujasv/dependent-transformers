#!/bin/bash

src_lang=$1
trg_lang=$2
parses=$3
translations=$4

python prepare_data.py \
    --from_dep_parse \
    --dep_parses $parses \
    --source_sentences ${src_lang}_sentences.txt \
    --linearized_dep_parses ${src_lang}_lin_parses.txt \
    --target_task_files $translations ${src_lang}_lin_parses.txt \
    --target_task_tags "<TR>" "<DP>" \
    --train_src ${src_lang}_${trg_lang}_src.txt \
    --train_trg ${src_lang}_${trg_lang}_trg.txt

onmt_preprocess \
    --train_src ${src_lang}_${trg_lang}_src.txt \
    --train_tgt ${src_lang}_${trg_lang}_trg.txt \
    --src_words_min_frequency 2 \
    --tgt_words_min_frequency 2 \
    --shuffle \
    --save_data ${src_lang}_${trg_lang}_data