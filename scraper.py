from bs4 import BeautifulSoup
import requests
import time
import sys
import sqlite3
from Page import Page
# Attempts to solve issue of reaching recursion limit on certain websites
sys.setrecursionlimit(10000)
start_time = time.time()
def main():
    # Get name of root page from user
    rootPage = input("What is the homepage of the website you would like to graph?: ")
    # Get domain
    domainList = rootPage.split('/')
    domain = domainList[2]
    
    # Create and overwrite database if it does not already exist
    conn = sqlite3.connect('output/%s' % domain)
    c = conn.cursor()
    
    try:
        c.execute('''CREATE TABLE domain (
        title text,
        url text,
        childLinks text,
        notes text)
        ''')
    except sqlite3.OperationalError:
        # if table already exists, delete it and create a new one
        c.execute('''DROP TABLE domain''')
        c.execute('''CREATE TABLE domain (
        title text,
        url text,
        childLinks text,
        notes text)
        ''')

    conn.commit()

    conn.close()
    
    # Call recursiveScrape
    visitedLinks = []
    recursiveScrape(rootPage, visitedLinks, domain)

'''Scrapes through all linked pages on a domain
pre: url is a valid website
param: url Link to the page being scraped
param: visitedLinks All links previously visited by the routine
param: domain Domain name of the site being scraped
post: A file containing all pages linked to within the domain is written to output/domain'''
def recursiveScrape(url, visitedLinks, domain):
    if url in visitedLinks : return True
    try:
        if domain not in url : return True
    except TypeError:
        return True
    print(url)
    # page object for the current page
    curPage = Page()
    # open url
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    # set curPage elements
    try:
        curPage.title = soup.find('title').text
    except AttributeError:
        curPage.title = None
    curPage.url = url
    curPage.childLinks = []
    hyperLinks = soup.find_all('a')
    hyperLinks = list(filter((None).__ne__, hyperLinks))

    # get all links on a page
    for link in hyperLinks:
        # set hyperLink to href of link
        hyperLink = link.get('href')
        # remove '.' or '..' from the link
        if hyperLink == None:
            pass
        elif len(hyperLink) >= 2 and hyperLink[0:2] == '..':
            hyperLink = hyperLink.replace('..', '')
        elif len(hyperLink) == 1 and hyperLink[0] == '.':
            hyperLink = hyperLink.replace('.', '')
        
        # if not an external url add domain to hyperLink
        if hyperLink == None:
            pass
        elif hyperLink[0:4] != "http" and hyperLink[0] != '/':
            hyperLink = 'http://' + domain + '/' + hyperLink
        elif hyperLink[0:4] != "http":
            hyperLink = 'http://' + domain + hyperLink
        curPage.childLinks.append(hyperLink)

    # write curPage object to file
    curPage.appendToFile(domain)

    # add current link to visitedLinks
    visitedLinks.append(url)

    # for all child links in the page
    for link in curPage.childLinks:
        # call this function on that link
        recursiveScrape(link, visitedLinks, domain)


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
