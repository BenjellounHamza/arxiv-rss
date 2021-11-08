import fitz
import os
import json

from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
from jsonmerge import merge

def author(source):

	authors = []
	dict = {}
	for name in source.find_all("persname"):
		surname = name.find("surname")
		forename = name.find("forename")
		if surname and forename:
			authors.append("%s %s" % (surname.text, forename.text))
	for i, author in enumerate(authors):
		dict["name and surname" + str(i)] = author
		
	return dict
                

def date(soup):
  source = soup.find("sourcedesc")
  published = None
  if source:
    published = source.find("monogr").find("date")
    try:
      published = parser.parse(published["when"]) if published and "when" in published.attrs else None
    except:
      published = None

  return published

def extract(path_directory):
  #files = os.listdir(path_directory + "/pdf")
  pdf_files = []
  #for f in files:
  #  if f[-4:] == '.pdf':
	#    pdf_files.append(f)
  d = datetime.today().strftime('%Y-%m-%d')
  for root, dirs, files in os.walk(path_directory):
    for name in files:
        if name.endswith((".pdf")) and d in root:
          pdf_files.append(root + "/" + name)
          #print(root + name)

  dicts = {}

  for article in pdf_files:
    try:
      dict = {}
      doc = fitz.open(article)
      whole_pdf = ""
      for page in doc:
        whole_pdf = whole_pdf + page.getText("text")  

      dict['text'] = whole_pdf
      cmd = 'curl -v --form input=@' + article + ' localhost:8070/api/processHeaderDocument > ' + article[:-4] + '.xml'
      os.system(cmd)
      tei_doc = article[:-4] + '.xml'
      with open(tei_doc, 'r') as tei:
        soup = BeautifulSoup(tei, 'lxml')

      dict['abstract'] = soup.abstract.getText(separator=' ', strip=True)
      dict['title'] = soup.title.getText()
      dict['autors'] = author(soup)
      dict['date'] = date(soup)
      
      dicts[article] = dict
    except:
      print("can't open file")
    
  return dicts




def merge_JsonFiles():

  namefile = []
  for root, dirs, files in os.walk("./database"):
    for name in files:
        if name.endswith((".json")) and "merged" not in root:
            namefile.append(root + "/" + name)
    result = {}

    for f1 in namefile:
        with open(f1) as infile:
            data = json.loads(infile.read())
            result = merge(result, data)
    with open('./database/merged/data.json', 'w') as output_file:
        json.dump(result, output_file)


def main():
    path = './papers'
    extractions = extract(path)
    # store data
    d = datetime.today().strftime('%Y-%m-%d')
    if not os.path.exists("database"):
            os.makedirs("database")
    if not os.path.exists("database/" + d):
            os.makedirs("database/" + d)
    with open("./database/" + d +"/data.json", 'w') as json_out:
        json.dump(extractions, json_out, default=str)

    # merge data
    if not os.path.exists("./database/merged"):
        os.makedirs("./database/merged")
    #TODO
    merge_JsonFiles()


if __name__ == '__main__':
    main()
