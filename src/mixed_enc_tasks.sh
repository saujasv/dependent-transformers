#!/bin/bash

trg_lang=$1
source_file=$2
depparse_file=$3
constparse_file=$4
translations_file=$5

# python prepare_mixed_enc_data.py --source_sentences $source_file --target_task_files $translations_file --train_src en_${trg_lang}_tr_train_src.txt --train_trg en_${trg_lang}_tr_train_trg.txt
python prepare_mixed_enc_data.py --target_sentences $translations_file --source_task_files $source_file $constparse_file --train_src en_${trg_lang}_mixed_enc_tr_cp_train_src.txt --train_trg en_${trg_lang}_mixed_enc_tr_cp_train_trg.txt
subword-nmt learn-joint-bpe-and-vocab --input en_${trg_lang}_mixed_enc_tr_cp_train_src.txt en_${trg_lang}_mixed_enc_tr_cp_train_trg.txt -s 10000 -o en_${trg_lang}_mixed_enc_tr_cp_train.codes --write-vocabulary en_${trg_lang}_mixed_enc_tr_cp_train_en.vocab en_${trg_lang}_mixed_enc_tr_cp_train_${trg_lang}.vocab
subword-nmt apply-bpe -c en_${trg_lang}_mixed_enc_tr_cp_train.codes --vocabulary en_${trg_lang}_mixed_enc_tr_cp_train_en.vocab --vocabulary-threshold 50 < en_${trg_lang}_mixed_enc_tr_cp_train_src.txt > en_${trg_lang}_mixed_enc_tr_cp_train_src.BPE.txt
subword-nmt apply-bpe -c en_${trg_lang}_mixed_enc_tr_cp_train.codes --vocabulary en_${trg_lang}_mixed_enc_tr_cp_train_${trg_lang}.vocab --vocabulary-threshold 50 < en_${trg_lang}_mixed_enc_tr_cp_train_trg.txt > en_${trg_lang}_mixed_enc_tr_cp_train_trg.BPE.txt

python prepare_mixed_enc_data.py --target_sentences $translations_file --source_task_files $source_file $depparse_file --train_src en_${trg_lang}_mixed_enc_tr_dp_train_src.txt --train_trg en_${trg_lang}_mixed_enc_tr_dp_train_trg.txt
subword-nmt learn-joint-bpe-and-vocab --input en_${trg_lang}_mixed_enc_tr_dp_train_src.txt en_${trg_lang}_mixed_enc_tr_dp_train_trg.txt -s 10000 -o en_${trg_lang}_mixed_enc_tr_dp_train.codes --write-vocabulary en_${trg_lang}_mixed_enc_tr_dp_train_en.vocab en_${trg_lang}_mixed_enc_tr_dp_train_${trg_lang}.vocab
subword-nmt apply-bpe -c en_${trg_lang}_mixed_enc_tr_dp_train.codes --vocabulary en_${trg_lang}_mixed_enc_tr_dp_train_en.vocab --vocabulary-threshold 50 < en_${trg_lang}_mixed_enc_tr_dp_train_src.txt > en_${trg_lang}_mixed_enc_tr_dp_train_src.BPE.txt
subword-nmt apply-bpe -c en_${trg_lang}_mixed_enc_tr_dp_train.codes --vocabulary en_${trg_lang}_mixed_enc_tr_dp_train_${trg_lang}.vocab --vocabulary-threshold 50 < en_${trg_lang}_mixed_enc_tr_dp_train_trg.txt > en_${trg_lang}_mixed_enc_tr_dp_train_trg.BPE.txt

python prepare_mixed_enc_data.py --target_sentences $translations_file --source_task_files $source_file $constparse_file $depparse_file --train_src en_${trg_lang}_mixed_enc_tr_cp_dp_train_src.txt --train_trg en_${trg_lang}_mixed_enc_tr_cp_dp_train_trg.txt
subword-nmt learn-joint-bpe-and-vocab --input en_${trg_lang}_mixed_enc_tr_cp_dp_train_src.txt en_${trg_lang}_mixed_enc_tr_cp_dp_train_trg.txt -s 10000 -o en_${trg_lang}_mixed_enc_tr_cp_dp_train.codes --write-vocabulary en_${trg_lang}_mixed_enc_tr_cp_dp_train_en.vocab en_${trg_lang}_mixed_enc_tr_cp_dp_train_${trg_lang}.vocab
subword-nmt apply-bpe -c en_${trg_lang}_mixed_enc_tr_cp_dp_train.codes --vocabulary en_${trg_lang}_mixed_enc_tr_cp_dp_train_en.vocab --vocabulary-threshold 50 < en_${trg_lang}_mixed_enc_tr_cp_dp_train_src.txt > en_${trg_lang}_mixed_enc_tr_cp_dp_train_src.BPE.txt
subword-nmt apply-bpe -c en_${trg_lang}_mixed_enc_tr_cp_dp_train.codes --vocabulary en_${trg_lang}_mixed_enc_tr_cp_dp_train_${trg_lang}.vocab --vocabulary-threshold 50 < en_${trg_lang}_mixed_enc_tr_cp_dp_train_trg.txt > en_${trg_lang}_mixed_enc_tr_cp_dp_train_trg.BPE.txt
