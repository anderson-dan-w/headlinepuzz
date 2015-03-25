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

def getHLP():
    text = get_webpage("thephoenixsociety.org", "/puzzles/puzzles.htm")
    match = re.search("address shown above.*?</p>", text)
    if match:
        headline_string, n = re.subn(r"\\\w", "", match.group())
        lines = re.split("<br>\d\.\s", headline_string)
        headlines = lines[1:]  ## first part is 'address shown...'
        headlines = [h.replace("</p>","").replace("\\","") for h in headlines]
        return headlines
    return

if __name__ == '__main__':
    headlines = getHLP()
    if headlines:
        print(headlines)
    else:
        print("Had trouble parsing...")
