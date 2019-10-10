from flask import Flask, escape, request, jsonify
import json

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

# style = Style.from_dict({
#     'ul': '#00e1ff',
# })

def print_html(html):
    with open('tmp.html', 'w') as f:
        f.write(html)
    import subprocess
    full = subprocess.run(["w3m", "-dump","-cols" ,f'{WIDTH}','tmp.html'], stdout=subprocess.PIPE)

    # with open('tmp.txt') as f:
    #     full = f.read()
    return full.stdout.decode('utf-8')

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


    # print_html(full)
    return full


def at_to_slash(string: str):
    if string is None:
        return None
    else:
        return string.replace("@", '/')

def slash_to_at(string: str):
    if string is None:
        return None
    else:
        return string.replace("/", '@')


app = Flask(__name__)

PT = load_json('./pattern_tree.json')
VT = load_json('./verb_tree.json')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/verb')
@app.route('/verb/<string:verb>')
@app.route('/verb/<string:verb>/<int:index>')
def get_verb(verb = None, index = None):
    return_format = request.args.get("format", "json")

    pattern_info = ""
    candidate = []

    if verb is None:
        candidate = list(VT.keys())
    elif index is None:
        candidate = list(VT[verb])
    else:
        candidate = []
        pattern_info = get_verb_describe(VT[verb][index])

    reval = {}
    reval['pattern_info'] = pattern_info
    reval['candidate'] = candidate
    

    all_filled =  (verb is not None and index is not None)
    print(all_filled, verb, index)
    if return_format == 'json' or not all_filled:
        return jsonify(reval)

    html = UI_list_verb_describe(pattern_info)
    if return_format == 'html':
        return html
    elif return_format == 'ascii':
        return print_html(html)
    else:
        return jsonify(reval)


@app.route('/pattern')
@app.route('/pattern/<string:pattern>')
@app.route('/pattern/<string:pattern>/<string:struct>')
@app.route('/pattern/<string:pattern>/<string:struct>/<string:verb_group>')
def get_pattern(pattern = None, struct = None, verb_group = None):
    return_format = request.args.get("format", "json")

    verb_info = ""
    candidate = []

    pattern = at_to_slash(pattern)
    struct = at_to_slash(struct)
    verb_group = at_to_slash(verb_group)

    if pattern is None:
        candidate = list(map(slash_to_at, PT.keys()))
    elif struct is None:
        candidate = list(map(slash_to_at, PT[pattern].keys()))
    elif verb_group is None:
        candidate = list(map(slash_to_at, PT[pattern][struct].keys()))
    else:
        candidate = []
        verb_info = PT[pattern][struct][verb_group]

    reval = {}
    reval['verb_info'] = verb_info
    reval['candidate'] = candidate

    all_filled = pattern is not None and struct is not None and verb_group is not None
    if return_format == 'json' or not all_filled:
        return jsonify(reval)


    html = UI_list_verb_describe(verb_info)
    if all_filled and return_format == 'html':
        return html
    elif all_filled and return_format == 'ascii':
        return print_html(html)
    else:
        return jsonify(reval)



if __name__ == "__main__":
    app.run(host="0.0.0.0")