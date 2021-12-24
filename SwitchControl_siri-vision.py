#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
from lxml import etree


g_URL = 'http://192.168.1.3/'
g_User = "admin"
g_Password = "*******************"


MyHelp = "Usage: [ ShowAllPort | ShowPortState, PortNumber(1,2,3,....) | SetPortState, PortNumber(1,2,3,....), State(0,1) ]"


def SetPort(i, iState):
    data = {'portid':(i-1), 'state':iState, 'speed_duplex':'0', 'flow':'0', 'submit':'+++%D3%A6%D3%C3+++', 'cmd':'port'}
    requests.post(g_URL + 'port.cgi', data, auth=(g_User,g_Password))

def Fun_GetPortState(i):
    htmldata = requests.get(g_URL + 'port.cgi', auth=(g_User,g_Password))
#    print (htmldata.text)
    html = etree.HTML(htmldata.text)
    result = html.xpath('//table')
    tabledata = etree.tostring(result[1], encoding='utf-8').decode()

    tree = etree.fromstring(tabledata)
    for row in tree.xpath('//tr')[2:]:
        r = row.xpath('.//td/text()')
        strPort = "Port %d" % i
        if r[0] == strPort:
            return r[1]

def Fun_ListPortState():
    htmldata = requests.get(g_URL + 'port.cgi', auth=(g_User,g_Password))
    html = etree.HTML(htmldata.text)
    result = html.xpath('//table')
    tabledata = etree.tostring(result[1], encoding='utf-8').decode()

    tree = etree.fromstring(tabledata)
    for row in tree.xpath('//tr')[2:]:
        r = row.xpath('.//td/text()')
        print ("端口：", r[0], "状态: ", r[1])


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print (MyHelp)
        exit()

    if (sys.argv[1] == "ShowAllPort"):
        Fun_ListPortState()
    elif (sys.argv[1] == "ShowPortState"):
        print (Fun_GetPortState(int(sys.argv[2])))
    elif (sys.argv[1] == "SetPortState"):
        SetPort(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print (MyHelp)
