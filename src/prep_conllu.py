import re
import pickle
import argparse

def extract_sentences(conllu_file, sentences_file, metadata_file):
    metadata = dict()
    metadata['all_docs'] = list()
    curr_doc = None
    for line in conllu_file:
        mo = re.match("# newdoc id = (.+)", line)
        if mo:
            metadata[mo.group(1)] = list()
            curr_doc = mo.group(1)
            metadata['all_docs'].append(curr_doc)
        mo = re.match("# sent_id = (.+)", line)
        if mo:
            metadata[curr_doc].append(mo.group(1))
        mo = re.match("# text = (.+)", line)
        if mo:
            sentences_file.write(str(mo.group(1)) + '\n')
    pickle.dump(metadata, metadata_file)

    sentences_file.close()
    conllu_file.close()
    metadata_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=argparse.FileType('r'), help="File containing CoNLL-U data")
    parser.add_argument("--metadata", type=argparse.FileType('wb'), help="File to write metadata")
    parser.add_argument("--sentences", type=argparse.FileType('w'), help="File to write sentences")

    args = parser.parse_args()
    extract_sentences(args.source, args.sentences, args.metadata)