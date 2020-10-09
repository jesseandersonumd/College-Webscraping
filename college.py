import requests
import bs4
import re
import pandas as pd
import string
import random 

result = requests.get("http://doors.stanford.edu/~sr/universities.html")
soup = bs4.BeautifulSoup(result.text,'lxml')

college_selection = []
corresponding_urls = []
for line in soup.select('li'):
    text_of_line = str(line.get_text())
    urls = re.findall(r"\([^)]*\)", text_of_line)
    if urls == []:
        continue
    else:
        corresponding_urls.append(urls)
    cleaned = re.sub(r"\([^)]*\)","",text_of_line)
    if cleaned in string.ascii_uppercase:
        continue
    else:
        college_selection.append(cleaned.strip("\n\t").rstrip().lstrip())
        
colleges = random.sample(college_selection, k=100)

indexes = [college_selection.index(college) for college in colleges]

urls_for_dataset = [corresponding_urls[i] for i in indexes]

data_set = pd.DataFrame({'Colleges': colleges,
     'Address': urls_for_dataset
    })

excel = pd.ExcelWriter('output.xlsx')
data_set.to_excel(excel)
excel.save()