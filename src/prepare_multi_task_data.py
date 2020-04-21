from utils import *
import argparse

def generate_training_pairs(src_sentences, target_tasks, train_src, train_trg):
    src_lc = get_line_count(src_sentences)
    trg_lc = [get_line_count(trg_file) for trg_tag, trg_file in target_tasks]

    for lc in trg_lc:
        if lc != src_lc:
            raise CountError

    for trg_tag, trg_file in target_tasks:
        src_sentences.seek(0, 0)
        trg_file.seek(0, 0)
        i = 0
        while i < src_lc:
            s = src_sentences.readline().strip()
            t = trg_file.readline().strip()
            train_src.write('<' + trg_tag + '> ' + s + ' <' + trg_tag + '>' + '\n')
            train_trg.write(t + '\n')
            i += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_sentences", type=argparse.FileType('r'), help="File containing source sentences")
    parser.add_argument("--target_task_files", type=argparse.FileType('r'), nargs='+', help="Files containing target task sentences")
    parser.add_argument("--target_task_tags", type=str, nargs='+', help="File containing target task tags")
    parser.add_argument("--train_src", type=argparse.FileType('w'), help="File to write source sentences for training")
    parser.add_argument("--train_trg", type=argparse.FileType('w'), help="File to write target sentences for training")

    args = parser.parse_args()
    generate_training_pairs(args.source_sentences, list(zip(args.target_task_tags, args.target_task_files)), args.train_src, args.train_trg)