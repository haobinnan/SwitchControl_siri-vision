#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
from lxml import etree


MyHelp = "Usage:\n	IP\n	User\n	Password\n	ShowAllPort , ShowPortState , SetPortState\n	PortNumber(1,2,3,....)\n	State(0,1)"


def Fun_GetItem(IP, User, Password, i):
    htmldata = requests.get('http://' + IP + '/port.cgi', auth=(User, Password))
    html = etree.HTML(htmldata.text)
    result = html.xpath('//table')
    tabledata = etree.tostring(result[1], encoding='utf-8').decode()

    tree = etree.fromstring(tabledata)
    for row in tree.xpath('//tr')[2:]:
        r = row.xpath('.//td/text()')
        strPort = "Port %d" % i
        if r[0] == strPort:
            return r

def GetValue(HtmlData, SelectName, Text):
    htmldata = etree.fromstring(HtmlData)
    select = htmldata.xpath('//select[@name=\'' + SelectName  + '\']//option')

    for row in select:
        if row.text.find(Text) != -1:
            return int(row.get('value'))

def NameConvert_speed_duplex(name):
    if (name == "10 Half"):
        return "10M/半双工"
    elif (name == "10 Full"):
        return "10M/全双工"
    elif (name == "100 Half"):
        return "100M/半双工"
    elif (name == "100 Full"):
        return "100M/全双工"
    else:
        return name

def NameConvert_flow(name):
    if (name == "启动"):
        return "开启"
    else:
        return name

def SetPort(IP, User, Password, i, iState):
    r = Fun_GetItem(IP, User, Password, i)
    if (r):
        htmldata = requests.get('http://' + IP + '/port.cgi', auth=(User, Password))
        html = etree.HTML(htmldata.text)
        result = html.xpath('//table')
        tabledata = etree.tostring(result[0], encoding='utf-8').decode()

        portid = GetValue(tabledata, 'portid', r[0])
        speed_duplex = GetValue(tabledata, 'speed_duplex', NameConvert_speed_duplex(r[2]))
        flow = GetValue(tabledata, 'flow', NameConvert_flow(r[4]))

        data = {'portid':portid, 'state':iState, 'speed_duplex':speed_duplex, 'flow':flow, 'submit':'+++%D3%A6%D3%C3+++', 'cmd':'port'}
        requests.post('http://' + IP + '/port.cgi', data, auth=(User, Password))

def Fun_GetPortState(IP, User, Password, i):
    r = Fun_GetItem(IP, User, Password, i)
    if (r):
        return r[1]

def Fun_ListPortState(IP, User, Password):
    htmldata = requests.get('http://' + IP + '/port.cgi', auth=(User, Password))
    html = etree.HTML(htmldata.text)
    result = html.xpath('//table')
    tabledata = etree.tostring(result[1], encoding='utf-8').decode()

    tree = etree.fromstring(tabledata)
    for row in tree.xpath('//tr')[2:]:
        r = row.xpath('.//td/text()')
        print ("端口：", r[0], "状态: ", r[1])


if __name__ == '__main__':
    if (len(sys.argv) < 5):
        print (MyHelp)
        exit()

    if (sys.argv[4] == "ShowAllPort"):
        Fun_ListPortState(sys.argv[1], sys.argv[2], sys.argv[3])
    elif (sys.argv[4] == "ShowPortState"):
        print (Fun_GetPortState(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[5])))
    elif (sys.argv[4] == "SetPortState"):
        SetPort(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[5]), int(sys.argv[6]))
    else:
        print (MyHelp)

