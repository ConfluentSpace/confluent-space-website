import codecs
import os
import glob
import re
from ruamel.yaml import YAML

with codecs.open('src/shared/header.html', 'r', encoding='utf-8') as f:
    headerLong = f.read()

with codecs.open('src/shared/header-short.html', 'r', encoding='utf-8') as f:
    headerShort = f.read()

with codecs.open('src/shared/nav.html', 'r', encoding='utf-8') as f:
    nav = f.read()

with codecs.open('src/shared/businessinfo.html', 'r', encoding='utf-8') as f:
    businessInfo = f.read()

with codecs.open('src/shared/footer.html', 'r', encoding='utf-8') as f:
    footer = f.read()
    
codeTest = re.compile(r'\d+\.yml$')
ifTest = re.compile(r'#{if ([^}]+)}|#{/if}')
ext = re.compile(r'([^\\/]*)\.yml')
businessTest = re.compile(r'^(\s*)\${businessinfo}', flags=re.MULTILINE)

# http://lybniz2.sourceforge.net/safeeval.html
safe_list = ['abs', 'divmod', 'all', 'enumerate', 'int', 'ord', 'str', 'any', 'isinstance', 'pow', 'sum', 'issubclass', 'bin', 'iter', 'tuple', 'bool', 'filter', 'len', 'range', 'type', 'bytearray', 'float', 'list', 'unichr', 'callable', 'format', 'reduce', 'unicode', 'chr', 'frozenset', 'long', 'reload', 'vars', 'getattr', 'map', 'repr', 'xrange', 'cmp', 'max', 'reversed', 'zip', 'hasattr', 'round', 'complex', 'hash', 'min', 'set', 'next', 'dict', 'hex', 'slice', 'id', 'oct', 'sorted']
safe = dict([ (k, locals().get(k, None)) for k in safe_list ])

for file in glob.glob('src/pages/*.yml'):
    with codecs.open(file, 'r', encoding='utf-8') as f:

        yaml = YAML()
        yaml.allow_unicode = True
        ff = f.read()
        data = yaml.load(ff)

        header = headerLong
        content = data['content']
        subtitle = data['header']['subtitle'] if 'subtitle' in data['header'] else 'Confluent'

        if ff.find('\r\n') != -1:
            content = re.sub(r'\n', '\r\n', content)

        if codeTest.search(file):
            header = headerShort

        safe['path'] = data['header']['path'] if 'path' in data['header'] else None
        safe['page'] = data['header']['page'] if 'page' in data['header'] else None

        output = u''
        index = 0
        passed = False

        for match in ifTest.finditer(header):

            condition = match.group(1)
            if condition:
                output += header[index:match.start(0)]
                index = match.end(0)
                passed = eval(condition, { '__builtins__': None }, safe)
            else:
                if passed:
                    output += header[index:match.start(0)]
                index = match.end(0)
                passed = False

        output += header[index:]
        output = re.sub(r'\${title}', re.sub(r'&', '&amp;', data['header']['title']), output)
        output = re.sub(r'\${subtitle}', re.sub(r'&', '&amp;', subtitle), output)

        if 'description' in data['header']:
            output = re.sub(r'\${description}', data['header']['description'], output)
        else:
            output = re.sub(r'\${description}', '', output)

        if 'path' in data['header']:
            output = re.sub(r'\${path}', data['header']['path'], output)
        else:
            output = re.sub(r'\${path}', '', output)

        if 'page' in data['header']:
            output = re.sub(r'\${page}', data['header']['page'], output)
        else:
            output = re.sub(r'\${page}', '', output)

        # This may have to get fixed when the required library supports proper indication of
        # not eating ("chomping" according to spec) leading spaces
        content = re.sub(r'^(?=[^$])', '        ', content, flags=re.MULTILINE)

        indent = ''
        match = businessTest.search(content)
        if match:
            indent = match.group(1)

        output += nav
        output += re.sub(r'\${businessinfo}', re.sub(r'^\s+', '', re.sub(r'^(?=[^$])', indent, businessInfo, flags=re.MULTILINE)), content)

        match = businessTest.search(footer)
        if match:
            indent = match.group(1)

        output += re.sub(r'\${businessinfo}', re.sub(r'^\s+', '', re.sub(r'^(?=[^$])', indent, businessInfo, flags=re.MULTILINE)), footer)

        with codecs.open(os.path.join('site', ext.search(file).group(1)) + '.html', 'w', encoding='utf-8') as f2:
            f2.write(output)
