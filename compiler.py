from scanner import *


def main(input_path):
    scanner = Scanner(input_path)
    scanner.scan()


if __name__ == '__main__':
    main('input.txt')
