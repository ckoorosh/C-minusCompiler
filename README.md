<br/>
<p align="center">
  <h1 align="center">C-minus Compiler</h3>

  <p align="center">
    A python-based compiler for the C-minus programming language
    <br/>
    <br/>
  </p>
</p>

## About The Project

This is a python-based compiler for the C-minus -- a simpler version of the C programming language. It is developed as a project for the "Compiler Design" course at Sharif University of Technology.
The compiler is developed in 3 phases:
* Scanner
* Parser
* Intermediate Code Generator


## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Python 3.7 or higher
* anytree 2.8.0

### Installation

1. Clone the repo

```sh
git clone https://github.com/ckoorosh/Compiler-Project-Fall21.git
```

2. Install Python packages

```sh
pip install -r requirements.txt
```

3. Your input should be in the `input.txt` file

4. Run the compiler

```sh
python compiler.py
```

The generated code will be in the `output.txt` file. The parse tree will be in the `parse_tree.txt` file. The semantic and syntax errors will be in the `semantic_errors.txt` and `syntax_errors.txt` files.