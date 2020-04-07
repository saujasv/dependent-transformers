#!/bin/bash

trg_lang=$1
source_file=$2
depparse_file=$3
constparse_file=$4
translations_file=$5

python prepare_data.py --source_sentences $source_file --target_task_tags TR --target_task_files $translations_file --train_src en_${trg_lang}_tr_train_src.txt --train_trg en_${trg_lang}_tr_train_trg.txt
python prepare_data.py --source_sentences $source_file --target_task_tags TR CP --target_task_files $translations_file $constparse_file --train_src en_${trg_lang}_tr_cp_train_src.txt --train_trg en_${trg_lang}_tr_cp_train_trg.txt
python prepare_data.py --source_sentences $source_file --target_task_tags TR DP --target_task_files $translations_file $depparse_file --train_src en_${trg_lang}_tr_dp_train_src.txt --train_trg en_${trg_lang}_tr_dp_train_trg.txt
python prepare_data.py --source_sentences $source_file --target_task_tags TR CP DP --target_task_files $translations_file $constparse_file $depparse_file --train_src en_${trg_lang}_tr_cp_dp_train_src.txt --train_trg en_${trg_lang}_tr_cp_dp_train_trg.txt