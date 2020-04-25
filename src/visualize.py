from onmt.utils.parse import ArgumentParser
from onmt.model_builder import load_test_model

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

def main():
    parser = _get_parser()
    opt = parser.parse_args()
    fields, model, model_opts = load_test_model(opt)
    print(model.__dict__)

if __name__ == "__main__":
    main()