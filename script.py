import os
import sys
import re
from datetime import datetime
import time

#domain = ['astro-ph', 'cond-mat', 'cs', 'econ', 'eess', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th', 'math', 'math-ph', 'nlin', 'nucl-ex', 'nucl-th'
#            , 'physics', 'q-bio', 'q-fin', 'quant-ph', 'stat']

domain = {'intelligence_artificielle' : ['cs.AI', 'cs.LG'],
    'robotic' : ['cs.RO'],
    'big_data' : ['cs.DB'],
    'electronic' : ['eecss'],
    'biology' : ['q-bio'],
    'cybersecurity' : ['cs.CR'],
    'telecomunication' : ['cs.NI'],
    'energy' : ['astro-ph.HE', 'hep-ph', 'hep-ex', 'hep-lat'],
    'management' : ['q-fin.PM', 'q-fin.RM'],
    'aeronotic' : ['astro-ph'],
    'cloud_computing': ['cs.DC'],
    'chimie': ['physics.chem-ph'],
    'sante': ['physics.med-ph']}



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
    os.system("sudo rm /home/hamza/Bureau/arxiv-rss-master/articles_added")
    os.system("sudo echo 'Subject : scientific papers added' > /home/hamza/Bureau/arxiv-rss-master/articles_added")
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
            if name == 'cybersecurity':
                os.system("echo blockchain > /home/hamza/Bureau/arxiv-rss-master/arxiv_keywords.txt")
                os.system("echo cryptocurrency >> /home/hamza/Bureau/arxiv-rss-master/arxiv_keywords.txt")
            if name == 'intelligence_artificielle':
                os.system("echo autonomous driving > /home/hamza/Bureau/arxiv-rss-master/arxiv_keywords.txt")
                os.system("echo vehicle >> /home/hamza/Bureau/arxiv-rss-master/arxiv_keywords.txt")
                os.system("echo vehicles >> /home/hamza/Bureau/arxiv-rss-master/arxiv_keywords.txt")

                

            os.system("sudo ./arxiv-rss.sh " + cat)
            try:
                file = open('/home/hamza/Bureau/arxiv-rss-master/arxiv-others', 'r')
                lines = file.readlines()
                directory = "./papers/" + name + "/" + datetime.today().strftime('%Y-%m-%d')

                for i, line in enumerate(lines):
                    if i > 0 and i < 2:
                        link = get_link(line)
                        if link is not None:
                            #time.sleep(10)
                            os.system("arxiv-downloader --url " + link + " --directory " + directory)

                os.system('sudo rm arxiv-others')
            except:
                print("files doesn't exist")

            if name == 'cybersecurity':
                try:
                    file = open('/home/hamza/Bureau/arxiv-rss-master/arxiv-filtered', 'r')
                    directory = "./papers/blockchain"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    directory = "./papers/blockchain/" + datetime.today().strftime('%Y-%m-%d')
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    lines = file.readlines()

                    for i, line in enumerate(lines):
                        print(line)
                        if i > 0:
                            link = get_link(line)
                            if link is not None:
                                os.system("arxiv-downloader --url " + link + " --directory " + directory)
                    os.system('sudo rm arxiv-filtered')
                except:
                    print("no file exist for blockchain")

            if name == 'intelligence_artificielle':
                try:
                    file = open('/home/hamza/Bureau/arxiv-rss-master/arxiv-filtered', 'r')
                    directory = "./papers/autombile"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    directory = "./papers/autombile/" + datetime.today().strftime('%Y-%m-%d')
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    lines = file.readlines()

                    for i, line in enumerate(lines):
                        if i > 0:
                            link = get_link(line)
                            print(link)
                            if link is not None:
                                os.system("arxiv-downloader --url " + link + " --directory " + directory)

                    os.system('sudo rm arxiv-filtered')
                except:
                    print("no file exist for autombile")
    os.system("sendmail recsysHamza@gmail.com < ./articles_added")    

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