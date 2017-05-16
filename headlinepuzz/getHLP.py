#!/usr/bin/python3
from http.client import HTTPConnection
import re

def get_webpage(domain, url):
    if not domain.startswith("www."):
        domain = "www." + domain
    conn = HTTPConnection(domain)
    conn.request("GET", url)
    response = conn.getresponse()
    return str(response.read())

HLP_DOMAIN = "thephoenixsociety.org"
HLP_URL = "/puzzles/puzzles.htm"
HLP_DATE_URL = "/puzzles/{0}/{0}_{1:02d}_puzzlesolve.htm"

def getHLP(year_month=None):
    url = HLP_URL
    if year_month is not None:
        year, month = year_month
        url = HLP_DATE_URL.format(year, month)
    text = get_webpage(HLP_DOMAIN, url)
    match = re.search("above.*?</p>", text)
    if match:
        headline_string, n = re.subn(r"\\\w", "", match.group())
        lines = re.split("<br>\d\.\s", headline_string)
        headlines = lines[1:]  ## first part is 'above...'
        headlines = [h.replace("</p>","").replace("\\","").replace("&nbsp;","")
                     for h in headlines]
        return headlines
    return

if __name__ == '__main__':
    headlines = getHLP()
    if headlines:
        print(headlines)
    else:
        print("Had trouble parsing...")
