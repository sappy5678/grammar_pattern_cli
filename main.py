from prompt_toolkit import *
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import message_dialog

from copy import deepcopy

from typing import List
import json
from jinja2 import Environment, PackageLoader, select_autoescape

from jinja2 import Environment, FileSystemLoader
import pathlib


WIDTH = 80

# print(__file__)
p = pathlib.Path(__file__)
path = '{}/templates/'.format(p.parent.absolute())

# print(path)
env = Environment(
    loader=FileSystemLoader(path),
)

style = Style.from_dict({
    'ul': '#00e1ff',
})

def print_html(html):
    with open('tmp.html', 'w') as f:
        f.write(html)
    import subprocess
    full = subprocess.run(["w3m", "-dump","-cols" ,f"{WIDTH}",'tmp.html'], stdout=subprocess.PIPE)

    # with open('tmp.txt') as f:
    #     full = f.read()
    print(full.stdout.decode('utf-8'))

def load_json(path: str):
    value = None
    with open(path) as f:
        value = json.load(f)
    return value


def get_possible_patterns(word: str):
    return VT[word]

def get_verb_detail_info(verb_index):
    info = deepcopy(verb_index)
    verb = PT[verb_index[0]][verb_index[1]][verb_index[2]]['verb'][verb_index[3]][verb_index[4] + 1]
    info = info[:3] + [verb] + info[5:]
    # info.insert(,verb)
    return info

def get_verb_describe(verb_index):
    return PT[verb_index[0]][verb_index[1]][verb_index[2]]

def UI_list_verb_describe(verb_describe):
    full = ''.join(verb_describe['describe'])
    verb_lists = verb_describe['verb']

    verb_html_lists = []

    for verb_list in verb_lists:
        header = verb_list[0]
        datas = []
        data = []
        for idx, verb in enumerate(verb_list[1:]):
 
            data.append(verb)

            if (idx + 1) % 4 == 0:
                datas.append(data)
                data = []
        datas.append(data)
        template = env.get_template('verb_table.html')
        html = template.render(header=header, datas=datas)
        verb_html_lists.append(html)
    
    full += '<br>'.join(verb_html_lists)
    full += f"<div> chapter: {verb_describe['chapter']} page: {verb_describe['page']} </div> "


    print_html(full)
    # print_formatted_text(HTML(''.join(verb_describe['describe'])), style=style)

def UI_list_possible_patterns(possibles: List):
    data = []
    for idx, elem in enumerate(possibles):
        info = get_verb_detail_info(elem)
        verb = [idx]
        verb.extend(info)
        data.append(verb)
    header = ['index', 'pattern', 'structure', 'group', 'verb', 'chapter', 'page']
    width = 11
    for i in data:
        for j in i:
            width = max(width, len(str(j)))
    template = env.get_template('verb_list.html')
    tmp = template.render(headers=header, datas=data)
    print_html(tmp)
    # print(tabulate(data, headers=header, tablefmt="presto"))
 

def UI_search_word():
    print_formatted_text('please input word that you want to find')
    word_for_search = session.prompt('> ', completer=verbs_completer, complete_while_typing=True, validator=verbs_validator,)
    possible_pattern = get_possible_patterns(word_for_search)
    UI_list_possible_patterns(possible_pattern)

    range_validator = get_range_validator(0, len(possible_pattern))

    print_formatted_text('please input index')
    select = session.prompt('> ', validator=range_validator, validate_while_typing=True)
    select = int(select)
    verb_index = possible_pattern[select]
    verb_describe = get_verb_describe(verb_index)
    UI_list_verb_describe(verb_describe)

    return


def get_range_validator(start: int, end: int):
    return Validator.from_callable(
    lambda x: x.isdigit() and int(x) in range(start, end),
    error_message='This input is not valid digit or not in range.',
    move_cursor_to_end=True)

def UI_find_pattern():
    completer, validator = get_list_prompt(PT.keys())
    print('please input pattern')
    pattern = session.prompt('> ', completer=completer, validator=validator)

    completer, validator = get_list_prompt(PT[pattern].keys())
    print('please input structure')
    structure = session.prompt('> ', completer=completer, validator=validator)
    
    completer, validator = get_list_prompt(PT[pattern][structure].keys())
    print('please input verb group')
    verb_group = session.prompt('> ', completer=completer, validator=validator)

    UI_list_verb_describe(PT[pattern][structure][verb_group])


PT = load_json('./pattern_tree.json')
VT = load_json('./verb_tree.json')

def get_list_prompt(lists, error_message='the input is not in list'):
    completer = WordCompleter(lists)
    validator = Validator.from_callable(
        lambda x: x in lists,
        error_message='This verb is not in this book. ',
        move_cursor_to_end=True)
    
    return completer, validator

# verb tree
verbs_name = VT.keys()
verbs_completer = WordCompleter(verbs_name)
verbs_validator = Validator.from_callable(
    lambda x: x in verbs_name,
    error_message='This verb is not in this book. ',
    move_cursor_to_end=True)



# function
function_name = ['find_pattern', 'help', 'search_word', 'quit']
function_completer = WordCompleter(function_name)
function_validator = Validator.from_callable(
    lambda x: x in function_name,
    error_message='This input is not valid function.',
    move_cursor_to_end=True)

with open('templates/help.html') as f:
    help_message = f.read()

if __name__ == "__main__":
    session = PromptSession()


    print_formatted_text(HTML('use <b>help</b> for more information'))
    print_formatted_text(HTML('press <b>tab</b> for show auto complete'))

    while True:
        which_function = session.prompt('> ', completer=function_completer, complete_while_typing=True, validator=function_validator,)

        if 'help' == which_function:
            message_dialog(
                title='Help Windows',
                text= HTML(help_message)
            )
        elif 'search_word' == which_function:
            UI_search_word()

        elif 'find_pattern' == which_function:
            UI_find_pattern()
            pass
            
        elif 'quit' == which_function:
            break

    