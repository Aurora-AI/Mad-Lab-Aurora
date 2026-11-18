
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('../../Elysian Consult/aori_rendered_dom.html', encoding='utf-8'), 'html.parser')
bf = 'boil_R_2opbrl6mivb_-0'
for el in soup.find_all(True):
    for attr, val in el.attrs.items():
        if bf in str(val):
            print('Found in attr:', el.name, attr, val)
