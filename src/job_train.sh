#!/bin/bash
#SBATCH -A research
#SBATCH -n 40
#SBATCH --gres=gpu:4
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ujwal.narayan@research.iiit.ac.in


export LC_ALL=en_US.UTF-8
cd ~/nlpa/dependent-transformers/src 
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nla

mkdir /scratch/en_fi/
cp /home/athreya/nlpa/en-fi/preproc/* /scratch/en_fi/

bash train.sh /scratch/en_fi/ en_fi_lex_const model_en_fi_lex_const /home/athreya/nlpa/en-fi/models/
