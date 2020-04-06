#!/bin/bash

export LC_ALL=en_US.UTF-8
cd ~/nlpa/dependent-transformers/src 
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nla

model_name=$1
model_lang=$2
model_preds=$model_name"_preds.txt"
data_path="./../data/splits/test/"
mkdir -p "./../predictions/"
output_path="./../predictions/"$model_preds


onmt_translate \
	--model ./../models/$model_name \
	--beam_size 4 \
	--alpha 0.6 \
	--src $data_path"en_test.txt" \
	--length_penalty avg \
	--output $output_path 

python get_bleu_score.py $data_path$model_lang"_text.txt" $output_path
