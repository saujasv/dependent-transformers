#!/bin/bash

prefix=$1
data_file=$2
model_file=$3
dest_dir=$4

onmt_train -data ${prefix}/$data_file -save_model ${prefix}/$model_file \
        -layers 6 -rnn_size 512 -word_vec_size 512 -transformer_ff 2048 -heads 8  \
        -encoder_type transformer -decoder_type transformer -position_encoding \
        -train_steps 100000  -max_generator_batches 2 -dropout 0.1 \
        -batch_size 4096 -batch_type tokens -normalization tokens  -accum_count 2 \
        -optim adam -adam_beta2 0.98 -decay_method noam -warmup_steps 4000 -learning_rate 2 \
        -max_grad_norm 0 -param_init 0 -param_init_glorot \
        -label_smoothing 0.1 -valid_steps 1500 -save_checkpoint_steps 1500 -keep_checkpoint 5 \
        -world_size 4 -gpu_ranks 0 1 2 3


onmt_average_models -models ${prefix}/${model_file}_step_* -output ${prefix}/${model_file}_averaged.pt

mv ${prefix}/${model_file}_averaged.pt $dest_dir
