from onmt.utils.parse import ArgumentParser
from onmt.model_builder import load_test_model

def visualize_opts(parser):
    """ Visualization options """
    group = parser.add_argument_group('Model')
    group.add('--model', '-model', dest='models', metavar='MODEL', 
            type=str, default=[], required=True,
            help="Path to model .pt file.")

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