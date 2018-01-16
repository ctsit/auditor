# enter some transforms you want to make
# templates the files that you want
# updates the init.py
# updates the version

from jinja2 import Template
import os
import sys


with open(os.path.join(os.getcwd(), '../transforms/transform_template.txt')) as tempfile:
    transform_template = Template(tempfile.read())

with open(os.path.join(os.getcwd(), '../transforms/init_template.txt')) as tempfile:
    init_template = Template(tempfile.read())

for item in sys.argv[1:]:
    context = {
        'camel_case_name': ''.join(x for x in item.title() if not x.isspace()),
        'snake_case_name': item
    }
    with open(os.path.join(os.getcwd(), '../transforms/{}.py'.format(item))) as outfile:
        outfile.write(transform_template.render(**context))

transforms = []
for root, dirs, files in os.walk(os.path.join(os.getcwd(), '../transforms')):
    for path in files:
        if path != '__init__.py' and path != 'transform_template.txt' and path != 'init_template.txt':
            transforms.append(path.split('.')[0])


with open(os.path.join(os.getcwd(), '../transforms/__init__.py')) as outfile:
    outfile.write(init_template.render(transforms=transforms))
