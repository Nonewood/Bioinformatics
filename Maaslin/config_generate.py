import sys
tsv = sys.argv[1]
last = int(sys.argv[2])
with open(tsv, 'r') as IN, open('generated_config', 'w') as out:
	head = IN.readline().strip('\n').split('\t')
	metadata = head[last-1]
	tax = head[last]
	print('Matrix: Metadata', file = out)
	print('Read_PCL_Rows: -' + metadata, file = out)
	print('\nMatrix: Abundance', file = out)
	print('Read_PCL_Rows: ' + tax + '-', file = out)
