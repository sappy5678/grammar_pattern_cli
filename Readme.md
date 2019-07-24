# Introduction
This repo is command line interface for [GRAMMAR PATTERNS 1: VERBS](http://arts-ccr-002.bham.ac.uk/ccr/patgram/).
It can search word and show describe that writed in the book.

# Installation
## Unix like user
1. please install [python 3.6+](https://www.python.org/downloads/) first.
2. install [w3m](http://w3m.sourceforge.net), mac user can use `brew install w3m`.
3. type this command in terminal
    ```
    pip install prompt_toolkit jinja2
    ```
4. type `python main.py` to run program.

## Microsoft Windows user
1. install [msys2](https://www.msys2.org)
2. run msys2 and use below command to install packages
    ```
    pacman -S python w3m python3-pip
    ```
3. clone this repo
    ```
    git clone git@github.com:sappy5678/grammar_pattern_cli.git
    ```
4. install python package
    ```
    pip install prompt_toolkit jinja2
    ```
5. go into directory and run
    ```
    pyhton main.py
    ```
