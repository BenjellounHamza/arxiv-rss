import os
import sys
import re
from datetime import datetime
import time

#domain = ['astro-ph', 'cond-mat', 'cs', 'econ', 'eess', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th', 'math', 'math-ph', 'nlin', 'nucl-ex', 'nucl-th'
#            , 'physics', 'q-bio', 'q-fin', 'quant-ph', 'stat']

domain = {'intelligence_artificielle' : ['cs.AI', 'cs.LG'],
    'cybersecurity' : ['cs.DB'],
    'robotic' : ['cs.RO'],
    'electronic' : ['eecss'],
    'biology' : ['q-bio'],
    'telecomunication' : ['cs.NI'],
    'energy' : ['astro-ph.HE', 'hep-ph', 'hep-ex', 'hep-lat'],
    'management' : ['q-fin.PM', 'q-fin.RM'],
    'aeronotic' : ['astro-ph'],
    'cloud_computing': ['cs.DC']}



def find_new_articles():
    name = ""
    while name not in domain:
        name = input("veillez choisir un des sujets suivants: \n " + str(domain) + " : \n\n")
    
    os.system("sudo ./arxiv-rss.sh " + name)

    directory = "./papers"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "./papers/" + name
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "./papers/" + name + "/" + datetime.today().strftime('%Y-%m-%d')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file = open('/home/hamza/Bureau/arxiv-rss-master/arxiv-others', 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if i > 1:
            link = get_link(line)
            os.system("arxiv-downloader --url " + link + " --directory " + directory)


def find_all_articles():

    directory = "./papers"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for name, category in domain.items():
        print("waiting 15 min to extract new category")
        #time.sleep(900)
        directory = "./papers/" + name
        if not os.path.exists(directory):
                os.makedirs(directory)
        directory = "./papers/" + name + "/" + datetime.today().strftime('%Y-%m-%d')
        if not os.path.exists(directory):
            os.makedirs(directory)

        for cat in category:
            os.system("sudo ./arxiv-rss.sh " + cat)
            file = open('/home/hamza/Bureau/arxiv-rss-master/arxiv-others', 'r')
            lines = file.readlines()
            for i, line in enumerate(lines):
                if i > 1 and i < 6:
                    link = get_link(line)
                    if link is not None:
                        #time.sleep(10)
                        os.system("arxiv-downloader --url " + link + " --directory " + directory)


def get_link(line):
    try:
        return re.search("(?P<url>https?://[^\s]+)", line).group("url")
    except:
        return 

if len(sys.argv) > 1:
    for name in sys.argv[1:]:
        find_new_articles()
else:
    find_all_articles()