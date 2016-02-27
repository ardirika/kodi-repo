#!/usr/bin/python
# (c)AresU, October 8, 2015
# Greetz to: TioEuy & Bosen
# Version:
# 20160118: 1.5: Fix video server bug again
# 20151231: 1.4: Fix video server bug
# 20151209: 1.3: Fix video server link generator, add fanart
# 20151206: 1.2: Add Search function, add more video server & add uptobox resolver
# 20151017: 1.1: Improve Performance & Show FanArt
# 20151013: 1.0: First release

import xbmc,xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from os import path, system
import socket
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus
import xbmcaddon

try:
    import json
except:
    import simplejson as json

pass#print  "Here in default-py sys.argv =", sys.argv

mainURL="http://www.layanon9.pw"
thisPlugin = int(sys.argv[1])
addonId = "plugin.video.layanon9"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
addon = xbmcaddon.Addon()
path = addon.getAddonInfo('path')
progress = xbmcgui.DialogProgress()
#if not path.exists(dataPath):
#       cmd = "mkdir -p " + dataPath
#       system(cmd)

Host = "http://www.layanon9.net"

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def playVideo(url):
    player = xbmc.Player()
    player.play(url)

def gedebug(strTxt):
    print '##################################################################################################'
    print '### GEDEBUG: ' + str(strTxt)
    print '##################################################################################################'
    return
    
def addSearch():
    searchStr = ''
    keyboard = xbmc.Keyboard(searchStr, 'Search')
    keyboard.doModal()
    if (keyboard.isConfirmed()==False):
      return
    searchStr=keyboard.getText()
    if len(searchStr) == 0:
      return
    else:
      return searchStr 

def showSearch():
    pic = " "
    stext = addSearch()
    name = stext
    try:
      url="/search?q=" + stext.replace(' ','%20')
      # gedebug(url)
      ok = showMenu(url, '1')
    except:
      pass
    #addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
    #xbmcplugin.endOfDirectory(thisPlugin)

def showMainMenu():
    pic = " "
    addDirectoryItem("Drama TV", {"name":"Drama TV", "url":Host, "mode":1, 'episode':1}, pic)
    addDirectoryItem("TV Show", {"name":"TV Show", "url":Host, "mode":2, 'episode':1}, pic)
    addDirectoryItem("Telemovie", {"name":"Telemovie", "url":Host, "mode":3, 'episode':0}, pic)
    addDirectoryItem("Filem", {"name":"Filem", "url":Host, "mode":4, 'episode':0}, pic)
    addDirectoryItem("Anugerah", {"name":"Anugerah", "url":Host, "mode":5, 'episode':0}, pic)
    addDirectoryItem("Sukan", {"name":"Sukan", "url":Host, "mode":6, 'episode':0}, pic)
    addDirectoryItem("Istimewa", {"name":"Istimewa", "url":Host, "mode":7, 'episode':0}, pic)
    # addDirectoryItem("Browse", {"name":"Browse", "url":Host, "mode":2}, pic)
    addDirectoryItem("Search", {"name":"Search", "url":Host, "mode":99}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showLetterList():
    huruf='abcdefghijklmnopqrstuvwxyz'
    pic = ""
    #addDirectoryItem('#', {"name":'#', "url":"/drama-list/char-start-other.html", "mode":21}, pic)
    for i in range(len(huruf)):
        url="/drama-list/char-start-%s.html" % huruf[i]
        addDirectoryItem(huruf[i].upper(), {"name":huruf[i].upper(), "url":url, "mode":21}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showMenu(url, episode):
    # gedebug(url+episode)
    # url=url.replace(Host,'')
    url=mainURL+url
    pass#print "GEDEBUG: ",url
    # gedebug(url)
    content = getUrl(url)
    pass#print  "content B =", content
    regTxt ='<div class=\'post-thumbnail\'>\s*<a href=\'(.+?)\'><script type=\'text/javascript\'>\s*document.write\(bp_thumbnail_resize\(\"(.+?)\",\"(.+?)\"\)\);'
    match = re.split(regTxt,content)
    # gedebug(match)
    pic = " "
    picNext = path+'/next.jpg'
    for i in range(1,len(match),4):
      url=match[i]
      name=match[i+2]
      name=name.replace('&#8236;','').replace('&#8217;','\'')
      pic=match[i+1].replace(' ','%20').replace('s72-c','w250-h200-c')
      # gedebug('url: %s, name: %s, pic: %s' % (url,name,pic))
      if episode == str(1):
        addDirectoryItem(name, {"name":name, "url":url, "mode":11}, pic)
      elif episode == str(0):
        addDirectoryItem(name, {"name":name, "url":url, "mode":12, 'thumbnail':pic}, pic)
    
    try:
      regNext = '<a .*?class=\'blog-pager-older-link\' .*?href=\'http:\/\/.*?\/(.+?)\''
      match = re.compile(regNext).findall(content)[0]
      linkNext = '/'+match.replace('&amp;','&')
      addDirectoryItem("[I]Next[/I]", {"name":"Next", "url":linkNext, "mode":111, 'episode':episode}, picNext)
    except:
      pass
    
    # gedebug(linkNext)
    # addDirectoryItem("Next", {"name":"Next", "url":linkNext, "mode":111, 'episode':episode}, picNext)
    xbmcplugin.endOfDirectory(thisPlugin)

def showEpisodes(name1, url):
    # print 'GEDEBUG: Name: %s URL: %s' % (name1,url)
    content = getUrl(url)
    try:
      regPic='<a imageanchor="1" .*? src="(.+?)"'
      pic = re.compile(regPic).findall(content)[0]
    except:
      pic = ''
    # gedebug(pic)
    try:
      regTxt0='<table .*?>\n*\s*(.*?)</table>'
      match0 = re.compile(regTxt0,re.DOTALL).findall(content)[0]
      # gedebug(match0)
      regTxt='<td>\n*\s*<a href="(.+?)" target="_blank">\n*\s*<span style="color: orange;">(.+?)</span>\n*\s*</a>\n*\s*</td>' #Episodes
      match = re.split(regTxt,match0)
      # print(match)
      
      for i in range(1,len(match),3):
        #gedebug('url: %s, episode: %s' % (url,name))
        urlTarget=match[i]
        name=match[i+1]
        addDirectoryItem(name, {"name":name, "url":urlTarget, "mode":12, 'thumbnail':pic}, pic)
    except:
      # gedebug(pic)
      findServer(name1, url, pic)

    xbmcplugin.endOfDirectory(thisPlugin)

def findServer(name1, url, pic=''):
    # gedebug(str(name1)+str(url))
    content = getUrl(url)
    pic = pic.replace('%3a',':').replace('%2f','/')
    # gedebug(url)
    i = 0
    url = ''
    nameSource = ''
    # search external server in available
    regEx = '<a href="(.+?)" target="_blank">SERVER .*?'
    match = re.compile(regEx).findall(content)
    # gedebug(match)
    if len(match) > 0: #if external server found
      for link in match:
        try:
          urls = showQuality(name1, link)
          # data = url.split('-2uk3y-')
          i = i+1
          # gedebug(urls)
          data = generateLink(urls, i)
          # gedebug(data)
          url = data[0]
          nameSource = data[1]
          addDirectoryItem(nameSource, {"name":nameSource, "url":url, "mode":13}, pic)
        except:
          pass

    # search internal server
    try:
      # htmldecode = getLinkDecode(content)
      # # gedebug(htmldecode)
      # if htmldecode:
      #   content = htmldecode

      # gedebug(content)
      regEx = '<(IFRAME|iframe)(.+?)>'
      match = re.compile(regEx,re.DOTALL).findall(content)
      # gedebug(match)
      linkData = []
      for f, string in match:
        # gedebug(string)
        if 'facebook' in string:
          # gedebug('facebook')
          pass
        else:
          regTxt='(SRC|src)=(.+?)\s'
          match = re.compile(regTxt,re.DOTALL).findall(string)
          linkData += match
          # gedebug('not facebook')

      if not linkData:
        htmldecode = getLinkDecode(content)
        # gedebug(htmldecode)
        if htmldecode:
          regTxt='(SRC|src)=(.+?)\s'
          match = re.compile(regTxt).findall(htmldecode)[0][1]
          linkData = [('s',match)]       

      match = linkData
      gedebug(match)
      for s, urlTarget in match:
        urls = showQuality(name1, urlTarget, '1')
        # gedebug(urls)
        i = i+1
        # gedebug(urls)
        data = generateLink(urls, i)
        # gedebug(data)
        url = data[0]
        nameSource = data[1]
        addDirectoryItem(nameSource, {"name":nameSource, "url":url, "mode":13}, pic)
        
    except:
      pass

    try:
      regEx = 'document.write\(unescape\(\'(.+?)\'\)'
      match = re.compile(regEx,re.DOTALL).findall(content)
      for encodeHTML in match:
        decodeHTML = urllib.unquote(encodeHTML)
        
        try:
          regEx = '<iframe.*?src=[\"\'](.+?)[\"\']'
          links = re.compile(regEx,re.DOTALL).findall(decodeHTML)
          for link in links:
            urls = showQuality(name1, link, '1')
            i = i+1
            data = generateLink(urls, i)
            # gedebug(link)
            url = data[0]
            nameSource = data[1]
            addDirectoryItem(nameSource, {"name":nameSource, "url":url, "mode":13}, pic)
        except:
          pass
      # gedebug(match)
    except:
      pass

    # addDirectoryItem(nameSource, {"name":nameSource, "url":url, "mode":13}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def generateLink(urls, i):
    # gedebug(urls)
    try:
      for j in range(0,len(urls),2):
        url = urls[j]['url']
        # gedebug('SERVER RANGE '+url)
        quality = "  [B]|[/B]  [I]" + urls[j]['quality'] + "[/I]"
        nameSource = 'Server '+ str(i) + quality # + '  [B]|[/B]  [I]' + url['quality'] + '[/I]'
        return [url, nameSource]
    except:
      try:
        url = urls
        # gedebug('NOT SERVER RANGE '+url)
        quality = "  [B]|[/B]  [I]Unknown[/I]"
        # gedebug('VIDEO LINK : '+urls)
        nameSource = 'Server '+ str(i) + quality#  [B]|[/B]  [I]'+url+'[/I][/UPPERCASE]'
        return [url, nameSource]
      except:
        pass


def getLinkDecode(content):
    htmldecode = ''
    try:
      regTxt='document.write\(unescape\(\'(.+?)\'\)\)'
      htmlencode = re.compile(regTxt).findall(content)[0]
      # gedebug(htmlencode)
      htmldecode = urllib.unquote(htmlencode)
      # gedebug(htmldecode)
      return htmldecode
    except:
      pass

    try:
      regTxt='eval\(unescape\(\'(.+?)\'\)\)'
      htmlencode_part1 = re.compile(regTxt).findall(content)[2]
      htmlencode_part2 = re.compile(regTxt).findall(content)[3]
      htmlencode_part2 = re.compile('\)\s\+\s\'(.+?)\'').findall(htmlencode_part2)[0]
      # gedebug(htmlencode_part1)
      htmldecode_1 = urllib.unquote(htmlencode_part1)
      htmldecode_2= urllib.unquote(htmlencode_part2)
      # gedebug(htmldecode_2)
      r = ''
      num_1 = re.compile('split\(\"(\d{8}?)\"\)').findall(htmldecode_1)[0]
      num_2 = re.compile('tmp\[1\]\s\+\s\"(.+?)\"\);').findall(htmldecode_1)[0]
      num_3 = re.compile('charCodeAt\(\i\)\)\+(.+?)\);').findall(htmldecode_1)[0]
      tmp_0 = htmldecode_2[:-15]
      tmp_1 = htmldecode_2[-15:]
      tmp_1 = tmp_1.replace(num_1,'')
      s = tmp_0
      k = str(tmp_1) + str(num_2)
      for i in xrange(0,len(s)):
        r += chr( (int(k[int(i)%len(k)]) ^ int(ord(s[i]))) + int(num_3) )
      # gedebug(r)
      htmldecode = r
      return htmldecode
    except:
      pass

def showQuality(name1, url, htmldecode=''):
    # gedebug(url)
    if not htmldecode:
      # gedebug(url)
      content = getUrl(url)
      # gedebug(content)
      try:
        regTxt='<div itemprop=[\'"]description articleBody[\'"]>\n\s*<[Ii][Ff][Rr][Aa][Mm][Ee].*?[Ss][Rr][Cc]=(.+?) .*?>'
        match = re.compile(regTxt).findall(content)[0]
      except:
        htmldecode = getLinkDecode(content)
        # gedebug(htmldecode)
        regTxt='<iframe.*?src=(.+?) .*?>'
        match = re.compile(regTxt,re.DOTALL).findall(htmldecode)[0]

      name = name1.replace('%20',' ')
      url = match.replace('"','').replace('\'','')

      # gedebug(match)
      try:
        regEx='https*:\/\/(.+?)\/.*?'
        linkSource = re.compile(regEx).findall(match)[0]
      except:
        linkSource = url
      # gedebug(url)
      site = re.sub('(www.|docs.)','',linkSource)
      site = site.split('.')[0]
      if site == 'google': site = 'googledocs'
      elif site == 'uptostream': 
        site = 'uptobox'
        url = url.replace('http://uptostream.com/iframe/','http://uptobox.com/')
      elif site == '//dailymotion':
        site = 'dailymotion'
      # gedebug('URL 1 '+site+' -------- '+url)
      urls = __import__(site).resolve(url)
      # gedebug(urls)
      # urls = urls.replace('\'','')
      return urls

    else:
      # gedebug(url)

      name = name1.replace('%20',' ')
      url = url.replace('"','').replace('\'','').replace('&amp;', '&')
      try:
        regEx='https*:\/\/(.+?)\/.*?'
        linkSource = re.compile(regEx).findall(url)[0]
      except:
        linkSource = url
      # gedebug(linkSource)

      site = re.sub('(www.|docs.)','',linkSource)
      site = site.split('.')[0]
      if site == 'google': site = 'googledocs'
      elif site == 'uptostream': 
        site = 'uptobox'
        url = url.replace('http://uptostream.com/iframe/','http://uptobox.com/')
      elif site == '//dailymotion':
        site = 'dailymotion'
      # gedebug('URL 2 '+site+' -------- '+url)
      urls = __import__(site).resolve(url)
      # gedebug(urls)
      return urls
        # gedebug(urls)

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}  

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    li.setInfo( "video", { "Title" : name, "FileName" : name} )
    if pic == " " or pic == path+"/next.jpg": pic = path+"/fanart.jpg"
    li.setProperty('Fanart_Image', pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
name =  str(params.get("name", ""))
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))
episode = str(params.get("episode", ""))
repeat = str(params.get("repeat", ""))
thumbnail = str(params.get("thumbnail", ""))

#### ACTIONS ####
if not sys.argv[2]:
    pass#print  "Here in default-py going in showContent"
    ok = showMainMenu()
else:
    if mode == str(1): #Click DramaTV
        ok = showMenu("/search/label/Drama%20TV", episode)
    elif mode == str(2):  #Click TVShow
        ok = showMenu("/search/label/TV%20Show", episode)
    elif mode == str(3):  #Click TVShow
        ok = showMenu("/search/label/Telemovie", episode)
    elif mode == str(4):  #Click TVShow
        ok = showMenu("/search/label/Filem", episode)
    elif mode == str(5):  #Click TVShow
        ok = showMenu("/search/label/Anugerah", episode)
    elif mode == str(6):  #Click TVShow
        ok = showMenu("/search/label/Sukan", episode) 
    elif mode == str(7):  #Click TVShow
        ok = showMenu("/search/label/Istimewa%20Raya%20Aidilfitri%202014", episode)                
    elif mode == str(99):  #Click Search
        ok = showSearch()
    elif mode == str(11):  #Click Episode
        ok = showEpisodes(name, url)
    elif mode == str(12):  #Click quality
        ok = findServer(name,url,thumbnail)
    elif mode == str(13): #Play video
        ok = playVideo(url)
    elif mode == str(21): #Show List by Letter
        ok = showMenu(url)
    elif mode == str(111): #Show Next Page
        ok = showMenu(url, episode)
