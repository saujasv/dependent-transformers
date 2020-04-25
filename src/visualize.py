import torch
from onmt.utils.parse import ArgumentParser
from onmt.model_builder import load_test_model
from onmt.utils.misc import sequence_mask
from onmt.translate import max_tok_len
from onmt.utils.misc import split_corpus
import onmt.inputters as inputters

def visualize_opts(parser):
    """ Visualization options """
    group = parser.add_argument_group('Model')
    group.add('--model', '-model', dest='models', metavar='MODEL', 
            nargs='+', type=str, default=[], required=True,
            help="Path to model .pt file.")
    group.add('--fp32', '-fp32', action='store_true',
              help="Force the model to be in FP32 "
                   "because FP16 is very slow on GTX1080(ti).")
    group.add('--avg_raw_probs', '-avg_raw_probs', action='store_true',
              help="If this is set, during ensembling scores from "
                   "different models will be combined by averaging their "
                   "raw probabilities and then taking the log. Otherwise, "
                   "the log probabilities will be averaged directly. "
                   "Necessary for models whose output layers can assign "
                   "zero probability.")

    group = parser.add_argument_group('Efficiency')
    group.add('--batch_size', '-batch_size', type=int, default=30,
              help='Batch size')
    group.add('--batch_type', '-batch_type', default='sents',
              choices=["sents", "tokens"],
              help="Batch grouping for batch_size. Standard "
                   "is sents. Tokens will do dynamic batching")
    group.add('--gpu', '-gpu', type=int, default=-1,
              help="Device to run on")
    
    group = parser.add_argument_group('Data')
    group.add('--data_type', '-data_type', default="text",
              help="Type of the source input. Options: [text|img].")

    group.add('--src', '-src', required=True,
              help="Source sequence to decode (one line per "
                   "sequence)")
    group.add('--src_dir', '-src_dir', default="",
              help='Source directory for image or audio files')
    group.add('--tgt', '-tgt',
              help='True target sequence (optional)')
    group.add('--shard_size', '-shard_size', type=int, default=10000,
              help="Divide src and tgt (if applicable) into "
                   "smaller multiple src and tgt files, then "
                   "build shards, each shard will have "
                   "opt.shard_size samples except last shard. "
                   "shard_size=0 means no segmentation "
                   "shard_size>0 means segment dataset into multiple shards, "
                   "each shard has shard_size samples")
    group.add('--output', '-output', default='pred.txt',
              help="Path to output the predictions (each line will "
                   "be the decoded sequence")
    group.add('--report_align', '-report_align', action='store_true',
              help="Report alignment for each translation.")
    group.add('--report_time', '-report_time', action='store_true',
              help="Report some translation time metrics")

    # Options most relevant to summarization.
    group.add('--dynamic_dict', '-dynamic_dict', action='store_true',
              help="Create dynamic dictionaries")
    group.add('--share_vocab', '-share_vocab', action='store_true',
              help="Share source and target vocabulary")

def _get_parser():
    parser = ArgumentParser(description='visualize.py')
    visualize_opts(parser)
    return parser

def transformer_encoder_forward_with_attn(layer, inputs, mask):
    input_norm = layer.layer_norm(inputs)
    context, attns = layer.self_attn(input_norm, input_norm, input_norm,
                                mask=mask, attn_type="self")
    out = layer.dropout(context) + inputs
    return layer.feed_forward(out), attns

def get_transformer_encoder_attn(model, src, lengths=None):
    emb = model.embeddings(src)
    model._check_args(src, lengths)

    out = emb.transpose(0, 1).contiguous()
    mask = ~sequence_mask(lengths).unsqueeze(1)
    attn_matrices = list()
    # Run the forward pass of every layer of the tranformer.
    for layer in model.transformer:
        out, attns = transformer_encoder_forward_with_attn(layer, out, mask)
        attn_matrices.append(attns)

    return emb, out.transpose(0, 1).contiguous(), lengths, attn_matrices

def get_encoder_attn_for_batch(model, batch):
    src, src_lengths = batch.src if isinstance(batch.src, tuple) \
                        else (batch.src, None)

    enc_states, memory_bank, src_lengths, attns = get_transformer_encoder_attn(model, src, src_lengths)
    return attns

def get_encoder_attn(model, src, fields, batch_size, gpu):
    src_data = {"reader": inputters.TextDataReader.from_opts(None), "data": src, "dir": None}
    _readers, _data, _dir = inputters.Dataset.config([('src', src_data)])

    data = inputters.Dataset(
        fields, readers=_readers, data=_data, dirs=_dir,
        sort_key=inputters.str2sortkey["text"],
        filter_pred=None
    )

    _use_cuda = gpu > -1
    _dev = torch.device("cuda", gpu) \
            if _use_cuda else torch.device("cpu")

    data_iter = inputters.OrderedIterator(
        dataset=data,
        device=_dev,
        batch_size=batch_size,
        batch_size_fn=max_tok_len,
        train=False,
        sort=False,
        sort_within_batch=True,
        shuffle=False
    )

    attns = list()
    for batch in data_iter:
        batch_attn = get_encoder_attn_for_batch(model, batch)
        attns.append(batch_attn)
    
    return attns

def main():
    parser = _get_parser()
    opt = parser.parse_args()
    fields, model, model_opts = load_test_model(opt)
    src_shards = split_corpus(opt.src, opt.shard_size)
    for src in src_shards:
        attns = get_encoder_attn(model, src, fields, opt.batch_size, opt.gpu)
        print(attns[0][0].shape)
        break

if __name__ == "__main__":
    main()