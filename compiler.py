from scanner import *
from parserr import *


def main(input_path):
    scanner = Scanner(input_path)
    par = Parser(scanner)
    par.parse(0)
    par.save_parse_tree()
    par.save_errors()


if __name__ == '__main__':
    main('input.txt')
