#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from lxml import etree


MyHelp = "Usage:\n	IP\n	User\n	Password\n	ShowAllPort , ShowPortState , SetPortState\n	PortNumber(1,2,3,....)\n	State(0,1)"


def Fun_GetItem(IP, User, Password, i):
    try:
        htmldata = requests.get('http://' + IP + '/port.cgi', auth=(User, Password))
    except:
        print ("Error: \"requests.get\" Line:", sys._getframe().f_lineno)
        exit()
    html = etree.HTML(htmldata.text)

    for row in html.xpath('//table[1]')[0].xpath('//tr')[4:]:
        td = row.xpath('.//td/text()')
        if len(td):
            if td[0] == "Port %d" % i:
                return td

def Fun_GetValue(Obj, SelectName, Text):
    select = Obj.xpath('//select[@name=\'' + SelectName  + '\']//option')
    for row in select:
        if row.text.find(Text) != -1:
            return int(row.get('value'))

def Fun_NameConvert_speed_duplex(name):
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

def Fun_NameConvert_flow(name):
    if (name == "启动"):
        return "开启"
    else:
        return name

def Fun_SetPort(IP, User, Password, i, iState):
    r = Fun_GetItem(IP, User, Password, i)
    if r is not None:
        try:
            htmldata = requests.get('http://' + IP + '/port.cgi', auth=(User, Password))
        except:
            print ("Error: \"requests.get\" Line:", sys._getframe().f_lineno)
            exit()
        html = etree.HTML(htmldata.text)
        table = html.xpath('//table')

        portid = Fun_GetValue(table[0], 'portid', r[0])
        speed_duplex = Fun_GetValue(table[0], 'speed_duplex', Fun_NameConvert_speed_duplex(r[2]))
        flow = Fun_GetValue(table[0], 'flow', Fun_NameConvert_flow(r[4]))

        data = {'portid':portid, 'state':iState, 'speed_duplex':speed_duplex, 'flow':flow, 'submit':'+++%D3%A6%D3%C3+++', 'cmd':'port'}
        try:
            htmldata = requests.post('http://' + IP + '/port.cgi', data, auth=(User, Password))
        except:
            print ("Error: \"requests.get\" Line:", sys._getframe().f_lineno)
            exit()
        html = etree.HTML(htmldata.text)

        for row in html.xpath('//table[1]')[0].xpath('//tr')[4:]:
            td = row.xpath('.//td/text()')
            if len(td):
                if td[0] == "Port %d" % i:
                    return td[1]

def Fun_GetPortState(IP, User, Password, i):
    r = Fun_GetItem(IP, User, Password, i)
    if r is not None:
        return r[1]

def Fun_ListPortState(IP, User, Password):
    try:
        htmldata = requests.get('http://' + IP + '/port.cgi', auth=(User, Password))
    except:
        print ("Error: \"requests.get\" Line:", sys._getframe().f_lineno)
        exit()
    html = etree.HTML(htmldata.text)

    for row in html.xpath('//table[1]')[0].xpath('//tr')[4:]:
        td = row.xpath('.//td/text()')
        if len(td):
            print ("端口：", td[0], "状态: ", td[1])


if __name__ == '__main__':
    if (len(sys.argv) < 5):
        print (MyHelp)
        exit()

    if (sys.argv[4] == "ShowAllPort"):
        Fun_ListPortState(sys.argv[1], sys.argv[2], sys.argv[3])
    elif (sys.argv[4] == "ShowPortState" and len(sys.argv) >= 6):
        print (Fun_GetPortState(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[5])))
    elif (sys.argv[4] == "SetPortState" and len(sys.argv) >= 7):
        print (Fun_SetPort(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[5]), int(sys.argv[6])))
    else:
        print (MyHelp)

