from scanner import *
from parser import *


def main(input_path):
    scanner = Scanner(input_path)
    parser = Parser(scanner)
    parser.parse()
    parser.save_parse_tree()
    parser.save_errors()


if __name__ == '__main__':
    main('input.txt')
