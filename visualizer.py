# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:46:13 2020
 
@author: e.peruch
""" 

import xml.etree.ElementTree as ET
import lxml.etree as LET 
import webbrowser
    
def text_to_xml(param):
    with open(param["xml_filename"], 'r', encoding="utf8") as f: 
        xml_file = f.read() 
        return xml_file


def xml_to_html(xml_encoding, param): #xsl transformation
    dom = LET.parse(param["xml_filename"])
    xslt = LET.parse(param["xsl_filename"])
    transform = LET.XSLT(xslt)
    newdom = transform(dom)
    with open (param["html_filename"], 'w', encoding="utf8") as h:
        print(newdom, file=h)
    url = param["html_filename"]
    return webbrowser.open(url, new=2)  # open in new tab