import requests
from bs4 import BeautifulSoup
import re
import peewee

from parser.models import *


def add_to_base(arr):
    tag_data = set(arr.pop(2).split(', '))
    print(tag_data)
    with db:
        array_tags = []
        for tag_name in tag_data:
            create_tag = Tag.get_or_create(name=tag_name)
            array_tags.append(create_tag[0])

        Task.create(
            id=arr[0],
            name=arr[1],
            tags=array_tags,
            complexity=int(arr[2]),
            solution=arr[3]
        )


def get_rows(page_number):
    print(page_number)
    url = f'https://codeforces.com/problemset/page/{page_number}?order=BY_SOLVED_DESC'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')

    table1 = soup.find('table', class_='problems')
    try:
        for j in table1.find_all("tr")[1:]:
            row_data = j.find_all("td")
            row = []
            for i in row_data:
                if i.find_all("div"):
                    tags_or_names = i.find_all("div")
                    for tag_or_name in tags_or_names:
                        all_a = tag_or_name.find_all("a")
                        tags = []
                        for tag in all_a:
                            tags.append(re.sub("^\s+|\n|\r|\s+$", '', tag.text))
                        row.append(re.sub("^\s+|\n|\r|\s+$", '', ', '.join(tags)))
                else:
                    if re.sub("^\s+|\n|\r|\s+$", '', i.text):
                        row.append(re.sub("^\s+|\n|\r|\s+$", '', i.text))
            print(row)
            add_to_base(row)
        get_rows(page_number+1)
    except peewee.IntegrityError:
        print('Отсутствуют новые посты')


def parser():
    with db:
        db.create_tables(
            [
                Tag,
                Task,
                Task.tags.get_through_model()
            ]
        )
        print('CONNECTED (parser)')
    get_rows(1)


if __name__ == "__main__":
    parser()
