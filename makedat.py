import re

import requests
from bs4 import BeautifulSoup

def daturl2cgiurl(daturl):
    r1 = "http:\/\/([a-z]{2,8}.\dch.net)/([a-z|0-9]*)/dat/(\d+).dat"
    match_result = re.match(r1, daturl)

    cgiurl = "http://" +  match_result.group(1) + "/test/read.cgi/" + match_result.group(2) + "/" + match_result.group(3)
    return cgiurl

def remove_image_href(elem):
    if elem.name == "a" and "class" in elem.attrs and elem.attrs["class"][0] == "image" :
        return elem.contents[0]
    else:
        return elem


def scraping(cgiurl):
    r = requests.get(cgiurl)
    soup = BeautifulSoup(r.content, "html.parser")
    print(soup.select(".title"))

    title = soup.select(".title")[0].text
    posts = soup.select(".post")

    dat = ""

    for i, post in enumerate(posts):
        number = post.select(".number")[0].text
        
        name = ''.join(map(str, post.select(".name")[0].contents))[3:-4]
        name = re.sub('</a>', '', name)
        name = re.sub('<a\shref=\"mailto:.*\">', '', name)

        email = ""
        if post.select(".name")[0].select("a", herf=True):
            email = post.select(".name")[0].select("a", herf=True)[0]["href"][7:]
        
        date = post.select(".date")[0].text
        
        uid = ""
        if post.select(".uid"):
            uid = post.select(".uid")[0].text
        
        message = ''.join(map(str, map(remove_image_href, post.select(".escaped")[0].contents)))
        
        if uid == "":
            post_dat = name + "<>" + email + "<>" + "" + date +  "<>" + message
        else:
            post_dat = name + "<>" + email + "<>" + "" + date + " " + uid + "<>" + message

        if i == 0:
            post_dat += "<>" + title
        post_dat += "\n"

        dat += post_dat
    
    return dat
        

