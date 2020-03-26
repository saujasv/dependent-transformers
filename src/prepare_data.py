from utils import *
from linearize import linearize_dep_tree
import re
import argparse

def extract_sentences_from_parse(input_file, depparse_file, text_file, lexicalized=False):
    words = list()
    for line in input_file:
        if line == '\n':
            sentence = Sentence(words)
            text_file.write(' '.join(sentence.get_words()) + '\n')
            depparse_file.write(linearize_dep_tree(sentence, lexicalized) + '\n')
            words = list()
        else:
            words.append(line)
                
    if len(words) > 0:
        sentence = Sentence(words)
        text_file.write(' '.join(sentence.get_words()) + '\n')
        depparse_file.write(linearize_dep_tree(sentence, lexicalized) + '\n')

def generate_training_pairs(src_sentences, target_tasks, train_src, train_trg):
    src_lc = get_line_count(src_sentences)
    trg_lc = [get_line_count(trg_file) for trg_tag, trg_file in target_tasks]

    for lc in trg_lc:
        if lc != src_lc:
            raise CountError

    for trg_tag, trg_file in enumerate(target_tasks):
        s = src_sentences.readline()
        t = trg_file.readline()
        train_src.write(trg_tag + s + trg_tag + '\n')
        train_trg.write(t + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--from_dep_parse", type=bool, help="Extract source sentences from parses specified as argument --parses")
    parser.add_argument("--lexicalize_dep_parses", type=bool, default=False, help="Use lexicalized dependency parses")
    parser.add_argument("--dep_parses", type=argparse.FileType('r'), nargs='?', help="File containing parses of source sentences")
    parser.add_argument("--source_sentences", type=str, nargs='?', help="File containing source sentences")
    parser.add_argument("--linearized_dep_parses", type=argparse.FileType('w'), nargs='?', help="File containing linearized parses")
    parser.add_argument("--target_task_files", type=argparse.FileType('r'), nargs='+', help="File containing target task sentences")
    parser.add_argument("--target_task_tags", type=str, nargs='+', help="File containing target task tags")
    parser.add_argument("--train_src", type=argparse.FileType('w'), help="File to write source sentences for training")
    parser.add_argument("--train_trg", type=argparse.FileType('w'), help="File to write target sentences for training")

    args = parser.parse_args()
    if args.from_dep_parse:
        with open(args.source_sentences, 'w') as src:
            extract_sentences_from_parse(args.dep_parses, args.linearized_dep_parses, src, args.lexicalize_dep_parses)
        
    with open(args.source_sentences, 'r') as src:
        generate_training_pairs(src, list(zip(args.target_task_tags, args.target_task_files)), args.train_src, args.train_trg)