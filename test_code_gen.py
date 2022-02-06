from glob import glob
from compiler import main
from os import mkdir, chdir, path
import subprocess
import shutil

for file in glob('D:/MM/Uniwork/Semesters/5    00-01 Fall/Compiler/Assignments/Practical/A3/TestCases/T3/input.txt'):
    file = file.replace('\\', '/')
    folder = file.split('/')[-2]
    input_path = 'D:/MM/Uniwork/Semesters/5    00-01 Fall/Compiler/Assignments/Practical/A3/TestCases/' + folder

    if not path.exists(input_path + '/output'):
        mkdir(input_path + '/output')

    shutil.copyfile(
        'D:/MM/Uniwork/Semesters/5    00-01 Fall/Compiler/Assignments/Practical/A3/Interpreter/tester_Windows.exe',
        input_path + '/output/tester_Windows.exe')

    chdir(input_path)
    main(input_path + '/input.txt')
    if folder[0] != 'S':
        chdir(input_path + '/output')
        result = subprocess.Popen(['tester_Windows'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = result.communicate()
        out = stdout.decode('utf-8')
        result = ''
        while out.find('\nPRINT') > 0:
            line = out[out.find('\nPRINT'):]
            line = line[1:line.find('\r')]
            out = out[out.find('\nPRINT') + 1:]
            result += line + '\n'
        result = result.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '').lower()
        with open(input_path + '/expected.txt', 'r') as f:
            expected_result = f.read().replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '').lower()
    else:
        with open(input_path + '/semantic_errors.txt', 'r') as f:
            expected_result = f.read().replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '').lower()
        with open(input_path + '/output/semantic_errors.txt', 'r') as f:
            result = f.read().replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '').lower()
    if expected_result == result:
        print('Test ' + folder + ': PASS\n')
    else:
        print('Test ' + folder + ': FAIL\n')
        print(result)
