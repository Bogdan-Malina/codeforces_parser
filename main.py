import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

url = 'https://codeforces.com/problemset?order=BY_SOLVED_DESC'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')

table1 = soup.find('table', class_='problems')

headers = ['id', 'name', 'tags', '', 'complexity', 'solutions']
# for i in table1.find_all('th'):
#     title = i.text.strip().strip().strip('\n').strip('\r')
#     headers.append(title)

# print(headers)

mydata = pd.DataFrame(columns=headers)

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
            row.append(re.sub("^\s+|\n|\r|\s+$", '', i.text))

    length = len(mydata)
    mydata.loc[length] = row

print(mydata)
mydata.to_csv('covid_data.csv', index=False)