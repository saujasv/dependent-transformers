#!/bin/bash
#SBATCH -A research
#SBATCH -n 40
#SBATCH --gres=gpu:4
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=ujwal.narayan@research.iiit.ac.in


export LC_ALL=en_US.UTF-8
cd ~/nlpa/dependent-transformers/src 
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nla

bash translate.sh model_en_fi_unlex_dep_averaged.pt "fi"

