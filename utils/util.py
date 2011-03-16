#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: util.py
# @Date: 2011年03月10日 星期四 09时26分44秒

import re

from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError
from antidote.red.models import Entry


def lines(file):
    for line in file: yield line
    yield '\n'

def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []

def slugify(string):
    string = re.sub('\s+', '-', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip().lower()

def markdown_factory(uploadObj, post):
    content = uploadObj.readlines()
    title = None if len(post['title']) == 0 else post['title']
    filename = None
    date = None
    tags = None if len(post['tags']) == 0 else post['tags'].split(',')
    output = []

    for line in content:
        line = line.strip('\n\r')
        if title == None:
            if line.startswith('title:'):
                title = line[6:].strip()
            else:
                title = line
        elif filename is None and line.startswith('file:'):
            filename = line[5:].strip().lower()
        elif tags is None and line.startswith('tags:'):
            tags = line[5:].split(',')
        elif date is None and line.startswith('date:'):
            if line[-1] == ":":
                date = post['date']
            else:
                date = line[5:].strip()
            filename = date + '-' + filename
        else:
            output.append(line)

    if filename is None:
        filename = slugify(title)

    if date is None:
        date = post['date']
        filename = date + '-' + filename

    if not content[-1].strip() == 'EOF':
        output.append('\nEOF')
    output = '\n'.join(output)

    cd = {'title': title,
          'filename': filename,
          'taglist': tags,
          'pub_date': datetime.strptime(date, '%Y-%m-%d'),
          'content': output,
         }
    try:
        if post['save'] == 'on':
            save_to_db(**cd)
    except MultiValueDictKeyError:
        pass
    return (filename, cd)

def save_to_db(**kwargs):
    title = kwargs.pop('title', {})
    Entry.objects.get_or_create(title=title, defaults=kwargs)
