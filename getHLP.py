#!/usr/local/lib/python3
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
        hls_string, n = re.subn("\\\\\w", "", match.group()) ## fix formatting
        hls = hls_string.split("<br>")[2:]  ## get rid of address, and nbsp
        hls = [hl[3:] for hl in hls]  ## delete leading number: '1. ', etc
        hls[-1] = hls[-1].replace("&nbsp;</p>","")
        return hls
    print("no match...")
    return


