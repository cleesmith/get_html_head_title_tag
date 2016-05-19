from __future__ import print_function
import json
import requests
import bs4
from bs4 import BeautifulSoup
import re

def get_html_with_bs4(url):
  error = None
  soup = None
  try:
    # page = requests.get(
    #   video_data['url'],
    #   headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36'}
    # )
    # fool'em: no spider just firefox:
    firefox_header = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=firefox_header)
    page.raise_for_status() # if not 200 raise an exception
    raw_html = page.text
    # remove comments, to avoid BeautifulSoup hiccups:
    clean_html = re.sub(r'<!--.*?-->', r'', raw_html.encode('utf-8'), flags=re.DOTALL)
    soup = BeautifulSoup(clean_html, "html.parser")
  except Exception as e:
    error = "Error: can not scrape url: %s\nexception: %s" % (url, e)
  return (page.text, soup, error)

def title(url):
  page, soup, error = get_html_with_bs4(url)
  if error:
    return error
  try:
    response = soup.title.text
  except:
    response = ''
  return response

def lambda_handler(event, context):
  page_title = title(event['url'])
  results = "url: " + event['url'] + " title: " + page_title
  return results

if __name__ == '__main__':
  event = {"url": "http://cleesmith.github.io/"}
  pt = lambda_handler(event, 'handler')
  print(pt)
