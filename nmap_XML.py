# coding=utf-8

from bs4 import BeautifulSoup

def get_html_text(text):
    result=[]
    text=BeautifulSoup(text,'html.parser')
    hosts=text.find_all('host')
    if len(hosts) ==0:
        return None
    for host in hosts:
        addr=host.address['addr']
        ports=host.find_all('port')
        # print('ports=',len(ports))
        for port in ports:
            portid=port['portid']
            portocol=port['protocol']
            state=port.state['state']
            reason=port.state['reason']
            reason_ttl=port.state['reason_ttl']
            # try:
            service=port.service['name']
            # except TypeError as e:
            #     service='UNKnown Service'

            print(addr,portid,portocol,state,reason,reason_ttl,service)
            # result.append([addr,portid,portocol,state,reason,reason_ttl,service])
    return result

# get_html_text(open('z:\\十堰.xml',encoding='utf-8').read())
get_html_text(open('z:\\port\\yc.xml',encoding='utf-8').read())