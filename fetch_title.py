from __future__ import print_function
import boto3
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
  # FIXME ensure event['url'] param is present and not blank
  page_title = title(event['url'])
  results = "url: " + event['url'] + " title: " + page_title

  # when event['queue'] is present then queue the results,
  # otherwise just return the results:
  aqueue = event.get('queue')
  print('SQS queue='+aqueue)
  if aqueue is None or len(aqueue) <= 0:
    # pass
    return results
  else:
    # FIXME use try except
    sqs_resource = boto3.resource('sqs')
    # this expects the queue's URL:
    # queue = sqs_resource.Queue(aqueue)
    # it's simpler to just use the queue name:
    queue = sqs_resource.get_queue_by_name(QueueName=aqueue)
    response = queue.send_message(MessageBody=results)

if __name__ == '__main__':
  event = {
    # 'url': 'http://cleesmith.github.io/health.html',
    'url': 'http://www.ghtctheatres.com/location/41139/Lewisburg-Cinema-8',
    # 'queue': 'https://sqs.us-east-1.amazonaws.com/410299363594/clsq'
    'queue': 'clsq'
  }

  pt = lambda_handler(event, 'pretend_context')
  print(pt)
