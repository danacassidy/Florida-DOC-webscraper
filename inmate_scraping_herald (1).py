#!/usr/bin/env python
# coding: utf-8

# In[30]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
import bs4
from bs4 import BeautifulSoup
import re
import time
import csv
import requests
import pandas as pd


# In[31]:


def getLinks(pageVals):
    global driver
    
    #find the table on the page
    pageSection = driver.find_element_by_class_name("small")
    # find the a tags within a the specific table
    pageNav = pageSection.find_elements_by_tag_name("a")
   
    #for each a tag among these a tags
    for pageLink in pageNav:
        
        #get the href (the url) and add it to the list called pagesVals
        pageVals.append(pageLink.get_attribute('href'))   


# In[32]:


#function to get the links for all of the pages after the first one 
def getPages(pageVals):
    
    global driver
    
    #variable instructs the driver to find the button on the page
    button = driver.find_element_by_tag_name("a")
   
    
    #while the button exists, run a loop. this will keep running until the button no longer exists
    while True:
        try:
            #wait for the page to load and after a certain amount of time has passed, find the button
            button = WebDriverWait(driver, 5, 0.25).until(EC.visibility_of_element_located([By.TAG_NAME, "a"]))
            #click the button
            button.click()
            #time to nap. scrapers get sleepy, too.
            time.sleep(3)
            
            #same thing from get links: find the part of the page with this class
            pageSection = driver.find_element_by_class_name("small")
            
            #find the a tags in the table
            pageNav = pageSection.find_elements_by_tag_name("a")

            #for each page, get all of the a tags
            for pageLink in pageNav:
                #for each of those links, get the href and add it to the same list called pageVals
                pageVals.append(pageLink.get_attribute('href'))   
            #run this function over and over, doing this for each page UNLESS it no longer works, in which case break the loop
        except:
            break


# In[41]:


#function to get the demographic information for each inmate    
def getDetails(pageVals):
    global driver
    global inmates
    
    #for each link in the list you have stored in pageVals
    for value in pageVals:
        #open each link
        html = urlopen(value)
        
        #we're using BeautifulSoup to scrape
        bsObj = BeautifulSoup(html, "html.parser")
        
        #find all of the td tags within a table 
        td_list = bsObj.findAll("td")
        
        # maybe use this , {"align":"LEFT"}
        
        #make a python dictionary, assigning a key and for each key, an attribute. Because these tags make have weird spacing, get their text and strip all formatting. This makes it easier to use when we export to a CSV
        inmate = {
            'id': td_list[0].get_text().strip(),
            'name': td_list[1].get_text().strip(),
            'race': td_list[2].get_text().strip(),
            'sex': td_list[3].get_text().strip(),
            'dob': td_list[4].get_text().strip(),    
        }
        #make a new python list called inmates and append your python dictionary, inmate, to that
        inmates.append(inmate)


# In[51]:


#function to save all of your hard work to a CSV        
def saveToCSV(inmates):
    global driver
    #give the csv file you want to export it to a name
    filename = 'heralds_inmates_2020_21.csv' 
    #open your new csv file with a 'w' so you can write to it
    with open(filename, 'w') as output_file:
        #make headers for you columns. these must match up with the keys you set in your python dictionary, inamte
        fieldnames = [	'id',
                        'name',
                        'race',
                        'sex',
                        'dob',
                        ]
       
        #write these into a csv, the headers being fieldnames and the rows your list of inmates
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inmates)


# Get the info from the main home page

# In[53]:


driver = webdriver.Chrome('/Users/danacassidy/Downloads/chromedriver')
driver.get('http://www.dc.state.fl.us/pub/mortality/2020-2021.html')
#your lists where info will be stored
pageVals = []
inmates = []
#run the functions, using the values (links) of the lists we created        
getLinks(pageVals) 
getPages(pageVals) 
driver.close() # close the driver 

getDetails(pageVals)
saveToCSV(inmates)


# merge the two together

# In[ ]:


res = requests.get('http://www.dc.state.fl.us/pub/mortality/2020-2021.html')
soup= bs4.BeautifulSoup(res.text,'lxml')
dfs = pd.read_html('http://www.dc.state.fl.us/pub/mortality/2020-2021.html')

table_= dfs[0]
table_.to_csv('heralds_inmates_2020_21.csv')


# In[ ]:


a = pd.read_csv('heralds_inmates_2020_21.csv') #'ID')
b = pd.read_csv('further_information2020_21.csv')

a_data = pd.DataFrame(a)
b_data = pd.DataFrame(b)

a_data = a_data.join(b_data['Date of Death'])
a_data = a_data.join(b_data['Institution Name'])
a_data = a_data.join(b_data['Manner of Death  Determined by ME'])
a_data = a_data.join(b_data['Investigative Status'])

a_data.to_csv('/Users/danacassidy/final_doc_webscrape_2020_21.csv')

#Investigative Status


# In[ ]:





# In[ ]:




