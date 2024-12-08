import os
import time
import pandas as pd
import openai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

# Changable Terms
term = 'AI'
term2 = 'Tech'
summarizer = True
sen_num = 5
story_lim = 4
latest = True

# Loading essentials
display = Display(visible=0, size=(800, 800))  
display.start()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
       if type(k) == str:
          title = k
       else:
          if len(k.text) > 5: 
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
def summarize(pairs, sen_num):
    summaries = []
    for i in pairs:
        content = f"""
        Summarize the following information in a concise format with about {sen_num} sentences 
        for easier consumption. Do not include the term TL:DR in the final output. 
        If nothing is given, reply with "No article".
        Do not repeat the title of the text. Fix all grammar and syntax errors from the input if applicable.
        Capture key points, interesting facts, and figures used in this article:
        title: {i[0]}
        article: {i[1]}
        """

        completion = openai.chat.completions.create(
                 messages=[
                     {
                         "role": "user",
                         "content": content,
                     }
                 ],
                 model="gpt-4-turbo",
             )
         final_summary = completion.choices[0].message.content.strip()
         summaries.append([i[0], final_summary, i[2], i[3]])
       
    return summaries
   
## Format for functions ## 
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

# # Firstpost # 
# termfp = term.replace(" ", "%20")
# firstpost_links = scrape_links(f"https://www.firstpost.com/search/?query={termfp}", "a.jsx-235a319a3b55c7b5.str-ln", By.CSS_SELECTOR)
# fp_pairs = scrape_articles(firstpost_links[0:story_lim], "//h1[@class='art-sec-ttl literatafont']", "//div[@class='main-dtls-wrap max-dtls-width formobilereadmore noredmoreforliveblog adcls']", "xpath", 'Firstpost')
# if summarizer == True:
#   fp_summaries = summarize(fp_pairs, sen_num)
# # print(fp_summaries)

# Verge # 
termv = term.replace(" ", "+")
verge_links = scrape_links(f"https://www.theverge.com/search?q={termv}", "//h2//a", "xpath")
v_pairs = scrape_articles(verge_links[0:story_lim], "//h1", "//div//p", 'xpath', 'Verge')
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

# # ArsTechnica # not best
# termat = term.replace(" ", "+")
# arstechnica_links = scrape_links(f"https://arstechnica.com/search/?q={termat}", "//div[@class='gs-title']//a", "xpath")
# at_pairs = scrape_articles(arstechnica_links[0:story_lim], "//h1[@class='mb-3 font-serif text-4xl font-bold text-gray-100 md:text-6xl md:leading-[1.05]']", "//div//p", 'xpath', 'ArsTechnica')
# if summarizer == True:
#   at_summaries = summarize(at_pairs, sen_num)
# # # print(at_summaries)

# Wired #
termw = term.replace(" ", "+")
wired_links = scrape_links(f"https://www.wired.com/search/?q={termw}&sort=publishdate+desc", "//div[@class='SummaryItemContent-eiDYMl ePPNpk summary-item__content']//a", "xpath")
w_pairs = scrape_articles(wired_links[0:story_lim], "//h1[@class='BaseWrap-sc-gjQpdd BaseText-ewhhUZ ContentHeaderHed-NCyCC iUEiRd cvHIvL kctZMs']", "//div//p", 'xpath', 'Wired')
if summarizer == True:
  w_summaries = summarize(w_pairs, sen_num)
# print(w_summaries)

# Getting csv
# + at_summaries + at_pairs 
if summarizer == True:
  total = tc_summaries + v_summaries + bi_summaries + w_summaries
else:
  total = tc_pairs + fp_pairs + v_pairs + bi_pairs + w_pairs
df = pd.DataFrame(total, columns=['Title', 'Text', 'Origin', 'Link'])
df.to_csv('newssummaries.csv', index=False)

def complete_missing_fields(row):
    title = row['Title']
    text = row['Text']

    # If both 'Title' and 'Text' are missing, skip this row
    if (title == "N/A" or pd.isna(title)) and (text == "N/A" or text == "No article" or pd.isna(text)or text == "No article."):
        return row

    # If 'Title' is missing, generate a title based on the text
    if (title == "N/A" or pd.isna(title) or title == "") and not (text == "N/A" or text == "No article." or pd.isna(text) or text == "" or text == "No article"):
      try:
        content = f"Generate a suitable title for the following tech article: {text}"
        completion = openai.chat.completions.create(
           messages=[
               {
                   "role": "user",
                   "content": content,
               }
           ],
           model="gpt-4-turbo",
           )
        titler = str("GENERATED: " + (completion.choices[0].message.content.replace('\\n',' ').replace('\n',' ')))
        row['Title'] = titler
      except Exception as e:
            print(f"Error generating title: {e}")

    # If 'Text' is missing, generate the content based on the title
    if (text == "N/A" or text == "No article." or pd.isna(text) or text == "" or text == "No article") and not (title == "N/A" or pd.isna(title) or title == ""):
        content = f"Generate a summation of an article in {sen_num} sentences for the following title using the best and latest data you know: {title}"
        try:
          completion = openai.chat.completions.create(
          messages=[ 
               {
                   "role": "user",
                   "content": content,
               }
           ],
          model="gpt-4-turbo",
          )
          textr = str("GENERATED: " + (completion.choices[0].message.content.replace('\\n',' ').replace('\n',' ')))
          row['Text'] = textr
        except Exception as e:
            print(f"Error generating text: {e}")
    return row

# Fill missing titles or info with AI 
df = df.apply(complete_missing_fields, axis=1)
   
# Email sending setup
gmail_address = os.getenv("GMAIL_ADDRESS")
gmail_password = os.getenv("GMAIL_PASSWORD")
assert gmail_address and gmail_password, "Gmail credentials not loaded"

date = datetime.now().strftime("%d-%m-%Y")
subscriber_email_addresses = ['nossorc2@gmail.com', 'boyuan.lu22@gmail.com', 'Wilson.huahung@gmail.com']
news_summaries = df

# Build the newsletter HTML content
html_content = f'''
<html>
<head></head>
<body>
    <h1>Daily {term} News - {date}</h1>
    <p>Brought to you by <b><a href="michaelcrosson.github.io/">Michael Crosson</a></b></p>
    <hr>
    <ul>
'''

# Loop through each news item and add it to the HTML content
for index, row in news_summaries.iterrows():
    html_content += f'''
    <li>
        <h3>{row['Title']}</h3>
        <p>{row['Text']}</p>
        <p><a href="{row['Link']}">Read more</a></p>
        <p><i>Source: {row['Origin']}</i></p>
    </li>
    <hr>
    '''

# Close the HTML content
html_content += '''
      <p><b><i>Psst</i><b> please support <a href="https://www.buymeacoffee.com/MichaelCrosson">here</a> | <a href="https://michaelcrosson.github.io/subscribe.html">unsubscribe</a>.</p>
    </ul>
</body>
</html>
'''
 
def send_email(to_address, content):
    email = EmailMessage()
    email["Subject"] = f"{date} - Daily Dose of {term} News"
    email["From"] = f"Daily {term} News"
    email["To"] = to_address
    email.add_alternative(content, subtype='html')
    smtp_server.send_message(email)

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as smtp_server:
        smtp_server.login(gmail_address, gmail_password)
        for email in subscriber_email_addresses:
            send_email(email, html_content)
except Exception as e:
    print(f"Error sending email: {e}")

