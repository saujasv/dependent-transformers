#!/bin/bash

en_train_json=$1
unlex_dep_parses=$2
unlex_const_parses=$3
lex_dep_parses=$4
lex_const_parses=$5

python extract_data.py \
    --parses $en_train_json \
    --linearized_dep_parses $unlex_dep_parses \
    --linearized_const_parses $unlex_const_parses

python extract_data.py \
    --parses $en_train_json \
    --linearized_dep_parses $lex_dep_parses --lexicalize_dep_parses \
    --linearized_const_parses $lex_const_parses --lexicalize_const_parses