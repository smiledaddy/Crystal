# -*- coding: utf-8 -*-
import argparse
import json
from io import open

from jinja2 import Template


def main():
    parser = argparse.ArgumentParser(
        description='A code generator demo for news',
        add_help=True)
    parser.add_argument('template', help='template file path')
    parser.add_argument('params', help='a json file path or literal')
    parser.add_argument('-o', '--output', help='output file path',
                        default='a.out')
    parser.add_argument('-e', '--encoding', help='input/output file encoding',
                        default='utf-8')

    args = parser.parse_args()
    params = {}
    if args.params.startswith('{'):
        params = json.loads(args.params)
    else:
        with open(args.params) as source:
            params = json.load(source)

    template = None
    with open(args.template, encoding=args.encoding) as template_file:
        template = template_file.read()

    template = Template(template)
    generated_data = template.render(params=params)

    with open(args.output, 'w', encoding=args.encoding) as outfile:
        outfile.write(generated_data)

if __name__ == '__main__':
    main()
