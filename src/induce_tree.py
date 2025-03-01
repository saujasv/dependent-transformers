from allennlp.nn.chu_liu_edmonds import decode_mst
from utils import *
import pickle
import torchtext
import argparse

def get_parse_from_attention_matrix(sentence, attention_matrix):
    governors, _ = decode_mst(attention_matrix, len(sentence), False)
    return Sentence([Word(w, i + 1, g + 1) for i, (w, g) in enumerate(zip(sentence, governors))])

def from_file(f, layer, head):
    sentences = list()
    while True:
        try:
            batch_dict = pickle.load(f)
            batch = batch_dict['batch']
            attn_matrices = batch_dict['matrices']
            for i, example in enumerate(batch):
                sent = example.src[0]
                attn = attn_matrices[layer].cpu().detach().numpy()
                sentences.append(get_parse_from_attention_matrix(sent, attn[i, head, :, :]))
        except EOFError:
            break
    return sentences 

def write_to_conllu(sentences, outfile, metadata):
    i = 0
    j = 0
    curr_doc = metadata['all_docs'][i]
    for sent in sentences:
        if j == len(metadata[curr_doc]):
            i += 1
            j = 0
            curr_doc = metadata['all_docs'][i]
        if j == 0:
            outfile.write("# newdoc id = " + curr_doc + '\n')
        outfile.write("# sent_id = " + metadata[curr_doc][j] + '\n')
        outfile.write("# text = " + " ".join(sent.get_words()) + '\n')
        outfile.write(sent.to_conllu() + '\n\n')
        j += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--attention_matrices", type=argparse.FileType('rb'), help="File containing encoder outputs")
    parser.add_argument("--metadata", type=argparse.FileType('rb'), help="File to read CoNLL-U metadata")
    parser.add_argument("--output_file", type=argparse.FileType('w'), help="File to write CoNLL-U parses")
    parser.add_argument("--layer", type=int, help="Layer from which to extract attention")
    parser.add_argument("--head", type=int, help="Index of attention head")

    args = parser.parse_args()
    metadata = pickle.load(args.metadata)
    sentences = from_file(args.attention_matrices, args.layer, args.head)
    write_to_conllu(sentences, args.output_file, metadata)
