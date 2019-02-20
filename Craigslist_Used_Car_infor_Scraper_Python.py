#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# start scraping information from just one page

from urllib.request import urlopen
from bs4 import BeautifulSoup

url='https://boston.craigslist.org/search/cta?s=0'

html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
cars=bs.find_all('li',{ 'class':'result-row'})

scrapedCarsList=[]
for car in cars:
    salesTitle=car.find('a',{'class':'result-title hdrlnk'})
    price=car.find('span',{'class':'result-price'})
    postingDate=car.find('time',{'class':'result-date'})
    #Some listings do not have a price.
    if price!=None:
        new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
        #print(new_car) #uncomment to see all the cars with a newline
        scrapedCarsList.append(new_car)
print(scrapedCarsList[0:3]) #uncomment to see the list of cars on the first page
len(scrapedCarsList)


# In[ ]:


# now let's revise the code to write the results of the first page into a csv file named 'CarCraglist.csv'.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

with open('CarCraglist.csv', 'w',newline='') as myFile:
    writer = csv.writer(myFile)
    writer.writerow(["sales Title", "Listing Date", "Price"])

url='https://boston.craigslist.org/search/cta?s=0'
html = urlopen(url)
bs = BeautifulSoup(html.read(),'html.parser')
cars=bs.find_all('li',{ 'class':'result-row'})

scrapedCarsList=[]
for car in cars:
    salesTitle=car.find('a',{'class':'result-title hdrlnk'})
    price=car.find('span',{'class':'result-price'})
    postingDate=car.find('time',{'class':'result-date'})
    #Some listings do not have a price.
    if price!=None:
        new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
        scrapedCarsList.append(new_car)

with open('CarCraglist.csv', 'a',newline='',encoding='utf-8') as myFile:
    writer = csv.writer(myFile)
    writer.writerows(scrapedCarsList)


# In[ ]:


#  create the list of URL's for the most recent 1,200 posting

baseURL='https://boston.craigslist.org/search/cta?s='
urlList=[]
for i in range(0,1201,120):
    newURL=baseURL+str(i)
    urlList.append(newURL)

print(urlList[0:50]) #uncomment to see the urls
len(urlList)


# In[ ]:


#  trun the scraping script into a function so that it can  takes the page number (0, 120, 240, ...) as input and returns a list of all the cars on the page in a list of lists format.

def craigslistCarsScrape(pageNumber):
    print('*** Scraping cars on page:',int(pageNumber/120+1),'***\n\n')

    baseURL='https://boston.craigslist.org/search/cta?s='
    url=baseURL+str(pageNumber)
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'html.parser')
    cars=bs.find_all('li',{ 'class':'result-row'})
    scrapedCarsList=[]            
    for car in cars:
        salesTitle=car.find('a',{'class':'result-title hdrlnk'})
        price=car.find('span',{'class':'result-price'})
        postingDate=car.find('time',{'class':'result-date'})
        #Some listings do not have a price.
        if price!=None:
            new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
            scrapedCarsList.append(new_car)
    return scrapedCarsList


# In[ ]:


# error handling to make the codes more robust

from urllib.error import HTTPError
from urllib.error import URLError

def craigslistCarsScraper(pageNumber):
    print('*** Scraping cars on page:',int(pageNumber/120+1),'***\n\n')

    baseURL='https://boston.craigslist.org/search/cta?s='
    url=baseURL+str(pageNumber)
    
    try:
        
        html = urlopen(url)
    
    except HTTPError as e:
        print(e)
        print('-----------------------HTTPError----------------------')
        return None
    except URLError as e:
        print('Server cound not be found')
        print('-----------------------URLError----------------------')
        return None
    
    bs = BeautifulSoup(html.read(),'html.parser')
    
    try:
        
        cars=bs.find_all('li',{ 'class':'result-row'})
    
    except AttributeError as e:
        print('Tag was not found')
        print('-----------------------AttributeError----------------------')
    
    else:
        scrapedCarsList=[]
        for car in cars:
            salesTitle=car.find('a',{'class':'result-title hdrlnk'})
            price=car.find('span',{'class':'result-price'})
            postingDate=car.find('time',{'class':'result-date'})
            #Some listings do not have a price.
            if price!=None:
                new_car=[salesTitle.get_text(),postingDate.get_text(),price.get_text()]
                    
                scrapedCarsList.append(new_car)
               
        return scrapedCarsList


# In[ ]:


craigslistCarsScraper(600)


# In[ ]:


# run the function in a loop and write the resutls on a csv

with open('craigslist_cars_final.csv', 'w',newline='') as myFile:
    writer = csv.writer(myFile)
    writer.writerow(["Listing Title", "Listing Date", "Price"])

with open('craigslist_cars_final.csv', 'a',newline='',encoding='utf-8') as myFile:
    writer = csv.writer(myFile)
    for i in range(0,1201,120):
        scrapedCarsList=craigslistCarsScraper(i)
        writer.writerows(scrapedCarsList)

print('----------------------------------------Well done---------------------------------------------- ')
print('-----------------------------------Scraping completed------------------------------------------ ')
print('------------Please find the csv file in the folder where this scraping file exists------------- ')

