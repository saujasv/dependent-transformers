#!/bin/bash

src_train_file=$1
trg_train_file=$2
src_valid_file=$3
trg_valid_file=$4
data_file_name=$5

paste -d \| $src_train_file $trg_train_file | shuf | awk -v FS='|' '{ print $1 > "dump_src.txt" ; print $2 > "dump_trg.txt" }'
rm $src_train_file $trg_train_file
mv dump_src.txt $src_train_file
mv dump_trg.txt $trg_train_file

onmt_preprocess \
    --train_src $src_train_file \
    --train_tgt $trg_train_file \
    --valid_src $src_valid_file \
    --valid_tgt $trg_valid_file \
    --save_data $data_file_name \
    --src_words_min_frequency 2 \
    --tgt_words_min_frequency 2
