# enter some transforms you want to make
# templates the files that you want
# updates the init.py
# updates the version

from jinja2 import Template
import os
import sys

def get_root():
    return os.path.split(os.getcwd())[0]


with open(os.path.join(get_root(), 'transforms/transform_template.txt')) as tempfile:
    transform_template = Template(tempfile.read())

with open(os.path.join(get_root(), 'transforms/init_template.txt')) as tempfile:
    init_template = Template(tempfile.read())

for item in sys.argv[1:]:
    context = {
        'camel_case_name': ''.join(x for x in item.title() if not x.isspace()),
        'snake_case_name': item
    }
    with open(os.path.join(get_root(), 'transforms/{}.py'.format(item)), 'w') as outfile:
        outfile.write(transform_template.render(**context))

transforms = []
for root, dirs, files in os.walk(os.path.join(get_root(), 'transforms')):
    for path in files:
        if path != '__init__.py' and path != 'transform_template.txt' and path != 'init_template.txt':
            transforms.append(path.split('.')[0])


with open(os.path.join(get_root(), 'transforms/__init__.py'), 'w') as outfile:
    outfile.write(init_template.render(transforms=transforms))
