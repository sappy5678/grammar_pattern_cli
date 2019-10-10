# About The Project
This project is a repo for [GRAMMAR PATTERNS 1: VERBS](http://arts-ccr-002.bham.ac.uk/ccr/patgram/).
It is presented in form of command line interface and allows users to search for verb patterns recorded in this grammar book.

# Installation
## For UNIX-like Systems
1. [python 3.6+](https://www.python.org/downloads/) is required to run the code.
2. Install [w3m](http://w3m.sourceforge.net). (For Mac users, it can also be installed by running `brew install w3m` )
3. Install **prompt_toolkit jinja2**.
    ```
    pip install prompt_toolkit jinja2
    ```
4. Run program by typing `python main.py` in command line.

## For Microsoft Windows Systems
1. Install [msys2](https://www.msys2.org).
2. Execute **msys2** and then run the following command.
    ```
    pacman -S python w3m python3-pip
    ```
3. Clone the repo.
    ```
    git clone git@github.com:sappy5678/grammar_pattern_cli.git
    ```
4. Install **prompt_toolkit jinja2**.
    ```
    pip install prompt_toolkit jinja2
    ```
5. Get into directory (**ls/grammar_pattern_cli/**) and run `pyhton main.py`.

# Usage
This project allows users to search verbs in two ways:
1. `find_pattern` : Find all verb patterns that matches all the entered conditions. 
    - Verb Patterns
    - Structure
    - Verb Group
2. `search_word` : Get information about a specific verb.
    - All patterns of the searched verb
    - Information about a specific verb pattern
3. Example: 
    - Take `find_pattern` function as example:
        ```
        $ python main.py
        use help for more information
        press tab for show auto complete
        > find_pattern
        please input pattern
        > V -ing
        please input structure
        > Verb with Adjunct
        please input verb group
        > ALL
        ```
    - Output:
        V -ing
        
        |   | Verb group | -ing clause |
        |---|---|---|
        | Subject | Verb | Adjunct |
        | I | 'd die | feeling guilty. |
        
        Phrasal verbs: V P -ing
        
        || Verb group | Partical | -ing clause |
        |---|---|---|---|
        | Subject | Verb || Adjunct |
        | We | ended | up | having dinner. |
        | I | was hanging | around | hoping to see him. |
        
        Verbs with this structure are all concerned with beggining, ending, or spending time in a particular way.
        - The soldiers reasoned that they'd prefer to die fighting rather than waiting.
        - Their boat finished up pointing the wrong way.
        - I started off doing languages, which I quite enjoyed, but I switched to law and quantified as a solicitor.
        
        Structure information
        a) The '-ing' clause is an Adjunct.
        b) This structure has no passive.
        c) The phrasal verb pattern is the same except that there is a particle, P, which comes after the verb.
        
        |V -ing ||||
        |---|---|---|---|
        | die | end up | finish up | hang about |
        | hang around / round | start off | wind up ||
        
        chapter 1 page: 86
        

# Docker run
docker run --restart=always -d  -p 5101:5000  $(DOCKER) 