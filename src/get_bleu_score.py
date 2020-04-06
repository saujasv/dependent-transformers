import sacrebleu
import sys, getopt

def main(args):
	actual_data_path = args[1]
	predicted_data_path = args[2]
	with open(actual_data_path, 'r') as handle:
		test_data = handle.read().splitlines()
	refs = [test_data]
	with open(predicted_data_path,'r') as handle:
		pred_data = handle.read().splitlines()
	sys = pred_data
	bleu = sacrebleu.corpus_bleu(sys, refs)
	score = bleu.score
	print(score)
	bleu_ouput = predicted_data_path[:-4] + "_bleu.txt"
	with open(bleu_ouput,'w') as handle:
		handle.write(str(score))
		handle.write('\n')

args =(sys.argv)
main(args)
