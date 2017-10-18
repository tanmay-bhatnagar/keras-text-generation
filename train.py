from __future__ import print_function
import argparse
import time
import os

from utils import TextLoader
from model import Model

def main():
    parser = argparse.ArgumentParser(
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data-dir', type=str, default='data/nietzsche',
                        help='data directory containing input.txt')
    parser.add_argument('--embedding-size', type=int, default=32,
                        help='size of the embedding')
    parser.add_argument('--rnn-size', type=int, default=128,
                        help='size of RNN hidden state')
    parser.add_argument('--num-layers', type=int, default=2,
                        help='number of layers in the RNN')
    parser.add_argument('--model', type=str, default='lstm',
                        help='rnn, gru, or lstm')
    parser.add_argument('--batch-size', type=int, default=100,
                        help='minibatch size')
    parser.add_argument('--seq-length', type=int, default=50,
                        help='training sequence length')
    parser.add_argument('--seq-step', type=int, default=10,
                        help='how often to pull a training sequence from the data')
    parser.add_argument('--num-epochs', type=int, default=50,
                        help='number of epochs')
    # FIXME: unused
    parser.add_argument('--grad-clip', type=float, default=5.,
                        help='clip gradients at this value')
    parser.add_argument('--learning-rate', type=float, default=0.002,
                        help='learning rate')
    parser.add_argument('--decay-rate', type=float, default=0.97,
                        help='decay rate for rmsprop')
    parser.add_argument('--skip-sampling', action='store_true',
                        help='skip the live sampling stage of training')
    args = parser.parse_args()
    train(args)

def train(args):
    load_start = time.time()
    loader = TextLoader(args.data_dir)
    load_end = time.time()
    print('Data load time', load_end - load_start)
    train_start = time.time()
    model = Model(args, loader)
    model.train(loader.data, args.num_epochs, not args.skip_sampling)
    train_end = time.time()
    print('Training time', train_end - train_start)
    model.save(filepath=os.path.join(args.data_dir, 'model.h5'))

if __name__ == '__main__':
    main()
