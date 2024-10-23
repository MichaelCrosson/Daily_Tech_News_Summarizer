import pandas as pd
import openai
from dotenv import load_dotenv
import smtplib
import ssl
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

load_dotenv()
openai.api_key = os.getenv("OPENAI")

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()  
options = [
   "--window-size=1200,1200",
    "--ignore-certificate-errors"]

for option in options:
    chrome_options.add_argument(option)
    
# Scrape inital links 
def scrape_links(url, xpath, selector):
    url = url
    driver = webdriver.Chrome(options = chrome_options)
    try:
      driver.get(url)
    except: 
       print("link get error")

    time.sleep(1)
    try:
      linksraw = driver.find_elements(selector, xpath)
    except:
       linksraw = 'Error'

    links = []
    for link in linksraw:
        try: 
          links.append(link.get_attribute("href"))
        except:
          pass

    driver.quit()
    print(links)
    return links

# Scrape Articles using links 
def scrape_articles(links, xpath_title, xpath_text, selector, origin):
  pairs = []
  m = 0
  driver = webdriver.Chrome(options = chrome_options)
  for i in list(links):
    try: 
      driver.get(i)
    except: 
       print("error with link")

    time.sleep(1)
    try: 
      titles = driver.find_elements(selector, xpath_title)
    except:
       titles = 'Error'
    try:
      text = driver.find_elements(selector, xpath_text)
    except:
       text = 'Error'

    title = 'N/A'
    for k in titles:
      try: 
        title = str(k.text)
      except:
        title = 'N/A'

    textcorpus = []
    for j in text:
      try:
        textcorpus.append(j.text)
      except:
         textcorpus.append('N/A')

    texter = ""
    for z in textcorpus:
      texter = texter + " " + z

    pairs.append([title, texter, origin, i])

  driver.quit()
  return pairs

### Summarizer ###
# needs [title, text, origin]
def summarize(pairs, sen_num):
    summaries = []
    for i in pairs:
        content = f"""
        Sumarize the following information in a TL:DR format with at least {sen_num} sentences 
        for easier cosumption. Do not include the term TL:DR in the final output. 
        If nothing is given simply reply with "No article".
        Do not repeat the title of the text. Fix all grammaer and syntax errors from the input if applicable.
        Capture key points, interesting facts, and figures used in this article:
        title: {i[0]}
        aritcle: {i[1]}
        """

        completion = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
        )
        
        text = completion.choices[0].message.content.replace('\\n',' ').replace('TL;DR','').replace('TL;DR:',' ').replace('\n',' ').replace('TL:DR','').replace('TL:DR:','')
        summaries.append([i[0], text, i[2], i[3]])
    return summaries

##### Main #####
term = 'ai'
summarizer = True
sen_num = 6
story_lim = 5
latest = True
## scrape_links(url, xpath, selector)
## scrape_articles(links, xpath_title, xpath_text, selector, origin)

# Tech Crunch #
if latest != True:
  termtc = term.replace(" ", "+")
  techurl = f"https://techcrunch.com/?s={termtc}"
else: 
  techurl = "https://techcrunch.com/latest/"
techcrunch_links = scrape_links(techurl, "//h3//a[@href]", 'xpath')
tc_pairs = scrape_articles(techcrunch_links[0:story_lim], "//h1[@class='article-hero__title wp-block-post-title']", "//p", "xpath", 'TechCrunch')
if summarizer == True:
  tc_summaries = summarize(tc_pairs, sen_num)
# print(tc_summaries)

# Firstpost # 
termfp = term.replace(" ", "%20")
firstpost_links = scrape_links(f"https://www.firstpost.com/search/?query={termfp}", "a.jsx-235a319a3b55c7b5.str-ln", By.CSS_SELECTOR)
fp_pairs = scrape_articles(firstpost_links[0:story_lim], "//h1[@class='art-sec-ttl literatafont']", "//div[@class='main-dtls-wrap max-dtls-width formobilereadmore noredmoreforliveblog adcls']", "xpath", 'Firstpost')
if summarizer == True:
  fp_summaries = summarize(fp_pairs, sen_num)
# print(fp_summaries)

# Verge # not best
termv = term.replace(" ", "+")
verge_links = scrape_links(f"https://www.theverge.com/search?q={termv}", "//h2//a", "xpath")
v_pairs = scrape_articles(verge_links[0:story_lim], "//h1[@class='inline font-polysans text-22 font-bold leading-110 md:text-33 lg:hidden']", "//div//p", 'xpath', 'Verge')
if summarizer == True:
  v_summaries = summarize(v_pairs, sen_num)
# print(v_summaries)

# Business Insider # 
if latest != True:
  termbi = term.replace(" ", "+")
  bi_links = scrape_links(f"https://www.businessinsider.com/s?q={termbi}", "//h3//a", "xpath")
else: 
  bi_links = scrape_links("https://www.businessinsider.com/tech", "//h3//a", "xpath")
bi_pairs = scrape_articles(bi_links[0:story_lim], "//h1[@class='post-headline  ']", "//div//p", 'xpath', 'BusinessInsider')
if summarizer == True:
  bi_summaries = summarize(bi_pairs, sen_num)
# print(bi_summaries)

# ArsTechnica # not best
termat = term.replace(" ", "+")
arstechnica_links = scrape_links(f"https://arstechnica.com/search/?q={termat}", "//div[@class='gs-title']//a", "xpath")
at_pairs = scrape_articles(arstechnica_links[0:story_lim], "//h1[@class='mb-3 font-serif text-4xl font-bold text-gray-100 md:text-6xl md:leading-[1.05]']", "//div//p", 'xpath', 'ArsTechnica')
if summarizer == True:
  at_summaries = summarize(at_pairs, sen_num)
# # print(at_summaries)

# Wired #
termw = term.replace(" ", "+")
wired_links = scrape_links(f"https://www.wired.com/search/?q={termw}&sort=publishdate+desc", "//div[@class='SummaryItemContent-eiDYMl ePPNpk summary-item__content']//a", "xpath")
w_pairs = scrape_articles(wired_links[0:story_lim], "//h1[@class='BaseWrap-sc-gjQpdd BaseText-ewhhUZ ContentHeaderHed-NCyCC iUEiRd cvHIvL kctZMs']", "//div//p", 'xpath', 'Wired')
if summarizer == True:
  w_summaries = summarize(w_pairs, sen_num)
# print(w_summaries)

# Getting csv
if summarizer == True:
  total = tc_summaries + fp_summaries + v_summaries + bi_summaries + at_summaries + w_summaries
else:
  total = tc_pairs + fp_pairs + v_pairs + bi_pairs + at_pairs + w_pairs
df = pd.DataFrame(total, columns=['Title', 'Text', 'Origin', 'Link'])
df.to_csv('newssummaries.csv', index=False)
print('done')
