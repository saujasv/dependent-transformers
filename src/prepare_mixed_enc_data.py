from utils import *
import argparse

def generate_training_pairs(trg_sentences, src_tasks, train_src, train_trg):
    trg_lc = get_line_count(trg_sentences)
    src_lc = [get_line_count(src_file) for src_file in src_tasks]

    for lc in trg_lc:
        if lc != src_lc:
            raise CountError

    for src_file in src_tasks:
        trg_sentences.seek(0, 0)
        src_file.seek(0, 0)
        i = 0
        while i < src_lc:
            t = trg_sentences.readline().strip()
            s = src_file.readline().strip()
            train_src.write(s + '\n')
            train_trg.write(t + '\n')
            i += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_sentences", type=argparse.FileType('r'), help="File containing source sentences")
    parser.add_argument("--source_task_files", type=argparse.FileType('r'), nargs='+', help="Files containing target task sentences")
    parser.add_argument("--train_src", type=argparse.FileType('w'), help="File to write source sentences for training")
    parser.add_argument("--train_trg", type=argparse.FileType('w'), help="File to write target sentences for training")

    args = parser.parse_args()
    generate_training_pairs(args.target_sentences, args.source_task_files, args.train_src, args.train_trg)