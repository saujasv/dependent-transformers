#!/bin/bash
#SBATCH -A research
#SBATCH -n 40
#SBATCH --gres=gpu:4
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=saujas.vaduguru@research.iiit.ac.in

src=$1
trg=$2

export LC_ALL=en_US.UTF-8
cd ~/nlpa/dependent-transformers/src 
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nla

./preprocess_base.sh ../data/splits $src $trg
./train.sh /scratch ${src}_${trg}_data ${src}_${trg}_base_tr.pt ~/nlpa/dependent-transformers/models  
