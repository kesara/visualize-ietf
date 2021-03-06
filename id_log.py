# id_log: Create custom log of IETF Internet Drafts

from os import fspath, scandir
from random import randrange
from sys import exit
from time import mktime, strptime
from urllib.parse import urlparse

from lxml import etree

from areas import AREAS
from colours import AREA_COLOURS, IETF_COLOUR, IRTF_COLOUR, OTHER_COLOUR


BIBXML_PATH = fspath('bibxml3')


def get_date(date_tag):
    date = '{year} {month} {day} {hour:02}:{min:02}:00'.format(
                year=date_tag.get('year'),
                month=date_tag.get('month', 'January'),
                day=date_tag.get('day', 1),
                hour=randrange(0, 24),
                min=randrange(0, 60))
    return int(mktime(strptime(date, '%Y %B %d %H:%M:%S')))


def get_area(wg):
    return next((k for k, v in AREAS.items() if wg in v), None)


def get_id_dict(filename):
    name_parts = filename[:-4].split('-')
    id_dict = {}

    if name_parts[1] == 'ietf':
        id_dict = {
                'org': name_parts[1],
                'area': get_area(name_parts[2]),
                'wg': name_parts[2],
                'name': '-'.join(name_parts[3:-1]),
                'file_name': '-'.join(name_parts)}
    elif name_parts[1] == 'irtf':
        id_dict = {
                'org': name_parts[1],
                'rg': name_parts[2],
                'name': '-'.join(name_parts[3:-1]),
                'file_name': '-'.join(name_parts)}
    elif name_parts[1] == '':
        id_dict = {
                'org': name_parts[2],
                'name': '-'.join(name_parts[3:-1]),
                'file_name': '-'.join(name_parts)}
    else:
        id_dict = {
                'org': name_parts[1],
                'name': '-'.join(name_parts[2:-1]),
                'file_name': '-'.join(name_parts)}
    return id_dict


def get_id_file(id_dict):
    return '/'.join(id_dict.values())


def get_colour(id_dict):
    if 'area' in id_dict.keys():
        return AREA_COLOURS[id_dict['area']]
    elif id_dict['org'] == 'ietf':
        return IETF_COLOUR
    elif id_dict['org'] == 'irtf':
        return IRTF_COLOUR
    else:
        return OTHER_COLOUR


def main():
    files = scandir(BIBXML_PATH)
    for file in files:
        try:
            with open(file, 'rb') as xml_file:
                xml = xml_file.read()

            root = etree.fromstring(xml)

            title = root.xpath('/reference/front/title')[0].text
            date = get_date(root.xpath('/reference/front/date')[0])

            text_url = root.xpath(
                    "/reference/format[@type='TXT']")[0].get('target')
            text_url_path = urlparse(text_url).path
            id_filename = text_url_path.split('/')[-1]

            id_dict = get_id_dict(id_filename)
            id_file = get_id_file(id_dict)
            id_colour = get_colour(id_dict)

            for author in root.xpath('/reference/front/author'):
                print('{timestamp}|{username}|{type}|{file}|{colour}'.format(
                    timestamp=date,
                    username=author.get('fullname'),
                    type='M',
                    file=id_file,
                    colour=id_colour))
        except Exception as e:
            pass
    exit(0)


if __name__ == '__main__':
    main()
