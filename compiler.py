# Mohammadreza Mofayezi 98106059
# Pouria Momtaz 98106061

from scanner import *
from parserr import *


def main(input_path):
    scanner = Scanner(input_path)
    parser = Parser(scanner)
    parser.parse()
    parser.save_errors()


if __name__ == '__main__':
    main('input2.txt')
