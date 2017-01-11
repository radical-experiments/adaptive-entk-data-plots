import argparse
import random

if __name__ =='__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--min', help='lower bound')
    parser.add_argument('--max', help='upper bound')

    args = parser.parse_args()

    f = open('output.txt','w')
    f.write('%s'%(random.randint(int(args.min), int(args.max))))
    f.close()



