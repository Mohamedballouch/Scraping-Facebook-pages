# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
import sys
import time
import calendar
from bs4 import BeautifulSoup as bs
import json
import re
import requests
import datefinder
import re
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import datetime

def scarp_post(page_name,month1,month2):
    
    page=page_name
    depth=2
    delay=5
    
    options = Options()
    
    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    
    options.add_argument("--mute-audio")
    # options.add_argument("headless")
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options )
    
    
    browser.get('https://www.facebook.com/pg/'+page+'/posts')

    # Scroll down depth-times and wait delay seconds to load
    # between scrolls
        
    # Scroll down depth-times and wait delay seconds to load
    # between scrolls
    
    import datetime
    real_date= month1+' 00:00:00'
    real_date1=month2+' 00:00:00'
    
    
    date1=datetime.datetime.strptime(real_date, '%Y-%m-%d %H:%M:%S')
    date2=datetime.datetime.strptime(real_date1, '%Y-%m-%d %H:%M:%S')
        
    def search_month(item):

        ti_Posts = item.find_all(class_="_5ptz")
        for post in  ti_Posts:
            temp = datetime.datetime.fromtimestamp(int(post['data-utime'])).strftime('%Y-%m-%d %H:%M:%S')
         
        return temp
    
    
    
    def scroll_f(br):
        global source_data
        source_data1 = br.page_source
        bs_data = bs(source_data1, 'html.parser')
        k= bs_data.find_all(class_="_5pcr userContentWrapper")
        
        list_dates=[]
        
        for item in k:
            if item.find_all(class_="_5ptz")==[]:
                pass
            else:
                lis_date=search_month(item)
                list_dates.append(lis_date)
            
        del list_dates[0]

        
        for l in list_dates:
            p=datetime.datetime.strptime(l, '%Y-%m-%d %H:%M:%S')
            
            if  p < date1:
                
                 #source_data = browser.page_source
                source_data = br.page_source
                
                return source_data
    
        for scroll in range(depth):
        
            # Scroll down to bottom
            br.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        
            # Wait to load page
            time.sleep(delay)
      
        
        
        scroll_f(br)
        #return br
        

    time.sleep(delay)
    
    
    
    def _extract_post_id(item):
      
            
        links =item.select('a[href^="/'+page+'/"]')
            
        post_id = ""
        
        for postLink in links:
                if "/"+page+"/posts" in postLink['href']:
                    
                    p = re.compile("/"+page+"/posts/(\d+)")
                    post_id=p.findall(postLink['href'])[0]
                    
    
                elif  "/"+page+"/photos"  in postLink['href']:
                    
                    post_id = re.findall(r'\d+', postLink['href'])[0]
                   
    
                elif  "/"+page+"/videos" in postLink['href']:
                    
                    post_id = re.findall(r'\d+', postLink['href'])[0]
                    
                    
       
        return post_id
    
    
    def _extract_post_text(item):
        
        actualPosts = item.find_all(attrs={"data-testid": "post_message"})
        text = ""
        if actualPosts:
            for posts in actualPosts:
                paragraphs = posts.find_all('p')
                text = ""
                for index in range(0, len(paragraphs)):
                    text += paragraphs[index].text
                    
        def remove_symbols(msg):
            regrex_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags = re.UNICODE)
            return regrex_pattern.sub(r'',msg)

        return remove_symbols(text)
    
    
    
    def _extract_link(item):
        global post_type
    
        
        links =item.select('a[href^="/'+page+'/"]')
        
        post_type=""
        link = ""
        
        for postLink in links:
            
                if "/"+page+"/posts" in postLink['href']:
                    link = "www.facebook.com"+postLink['href']
               
                    post_type='Article'
                    
                elif  "/"+page+"/photos"  in postLink['href']:
                    link = "www.facebook.com"+postLink['href']
            
                    post_type='Image'
                    
                elif  "/"+page+"/videos" in postLink['href']:
                    link = "www.facebook.com"+postLink['href']
             
                    post_type='Video'
                
        return link,post_type
    
    
    
    def _extract_image(item):
        
        image = ""
        if post_type=='Video':
            postvideos = item.find_all(class_="_3chq")
            
            for postvid in postvideos:
            
                if postvid.get('src') is not None:
                    image = postvid.get('src')
                else:
                    image=''
        else:
            postPictures = item.find_all(class_="scaledImageFitWidth img")
          
            
            for postPicture in postPictures:
           
                if postPicture.get('src') is not None:
                    image = postPicture.get('src')
                else:
                    image=''
                    
        return image
    
    
    
    def _extract_shares(item):
        
        postShares = item.find_all(class_="_4vn1")

        if postShares!=[]:
    
            shares = ""
            
            for postShare in postShares:
                
                y=postShare.find_all( class_="_3rwx _42ft")
                if not y :
                    
                    shares = 0
        
                else:
                    for cc in postShare.find_all(class_="_3rwx _42ft"):
                        x = cc.string
                  
                  
                        if "K"  in x:
                            x = x.split(">", 1)
    
                            share = x[0].split()[0]
                            shares=int(float(share.replace(",", "."))*1000)
            
                        elif  "M" in x:
                            x = x.split(">", 1)

                            share = x[0].split()[0]
                            
                            shares=int(float(share.replace(",", "."))*1000000)
            
                        else:
                            x = x.split(">", 1)

                            share = x[0].split()[0]
                            
                            shares=int(share)
                            
                           
        else:
            shares = 0
        
        return shares
    
    
    
    def _extract_caption(item):
        
        postCaptions = item.find_all(class_="_52c6")
    
        caption = "" 
        
        for postCaption in postCaptions:
            
            if not postCaption.find_all('span') :
                
                caption = ""
    
            else:
                for Cap in postCaption.find_all('span'):
    
                    caption=Cap.string
                    #print(caption)
        
        return caption
    
    
    
    
    def _extract_comments(item):
        
        postComments = item.find_all(class_="_4vn1")
    
        comments = ""

        if postComments!=[]:
        
            for comment in postComments:
                
        
                r=comment.find_all( class_="_3hg- _42ft")
                if not r :
                    
                    comments = 0
                else :
                    for cc in comment.find_all(class_="_3hg- _42ft"):
        
                        m=cc.string
                        if "K"  in m:
                            m = m.split(">", 1)
                            comt = m[0].split()[0]
                            comments=int(float(comt.replace(",", "."))*1000)
            
                        elif  "M" in m:
                            m = m.split(">", 1)
                            comt = m[0].split()[0]
                            comments=int(float(comt.replace(",", "."))*1000000)
            
                        else:
                            m = m.split(">", 1)
                            comt = m[0].split()[0]
                            comments=int(comt)
                            
                  
        else:
            comments = 0
        
        return comments
    
    
    
    def _extract_like(item):
    
        likes_p = item.find_all("a", attrs = {'class' : '_1n9l'})
        
        post_likes=""

        if likes_p ==[]:
            post_likes=0
            return post_likes
        else:

            for lik in likes_p:
                #print(lik["aria-label"])
                if "J’aime" not in lik["aria-label"]:
                    post_likes=0
                else :
                    #print("dkhel hna")
                    x = lik["aria-label"]
            
                    if "K"  in x:
                        x = x.split(">", 1)
                        likes = x[0].split()[0]
             
                        post_likes=int(float(likes.replace(",", "."))*1000)
        
                    elif  "M" in x:
                        x = x.split(">", 1)
                        likes = x[0].split()[0]
                        post_likes=int(float(likes.replace(",", "."))*1000000)
        
                    else:
                        x = x.split(">", 1)
                        likes = x[0].split()[0]
                        post_likes=int(likes) 

                return post_likes
    
    
    
    #posts = browser.find_elements_by_class_name("userContentWrapper")
    import datetime
    def  _extract_dates(item):
        ti_Posts = item.find_all(class_="_5ptz")
        
        date=""
        for post in  ti_Posts:
            # Creating a time entry.
    
            if len(post['data-utime']) > 0:
                temp = datetime.datetime.fromtimestamp(int(post['data-utime'])).strftime('%Y-%m-%d %H:%M:%S')
    
                # date returned will be a datetime.datetime object.
                date1 = str(temp).split(":", 1)[0]
                date = re.sub('[- ]', '', date1)
    
            else:
                date='no dates found'
          
                
        return date
            
    
    scroll_f(browser)
    
    bs_data = bs(source_data, 'html.parser')
    
    k= bs_data.find_all(class_="_5pcr userContentWrapper")
    postBigDict = list()
    
    
    time.sleep(delay)
    
    
    
    for item in k:
        
        if item.find_all(class_="_5ptz")==[]:
            pass
        
        else:

            x=datetime.datetime.strptime(search_month(item), '%Y-%m-%d %H:%M:%S')
           
            if  x >= date1 and  x <= date2:
                postDict = dict()
                
                postDict['PostId'] = _extract_post_id(item)
                postDict['Date'] = _extract_dates(item)
                postDict['Message'] = _extract_post_text(item)
                postDict['Caption'] =_extract_caption(item)
                postDict['Link'],postDict['Post_type'] = _extract_link(item)
                postDict['Image'] = _extract_image(item)
                postDict['Likes']=_extract_like(item)
                postDict['Shares'] = _extract_shares(item)
                postDict['Comments']=_extract_comments(item)
                
                #Add to check
                postBigDict.append(postDict)
                with open('./postBigDict.json','w', encoding='utf-8') as file:
                    file.write(json.dumps(postBigDict, ensure_ascii=False).encode('utf-8').decode())
    

  

    return postBigDict
        
    
    
