#!/usr/bin/python
# -*- coding: latin-1 -*-
import urllib2
import urllib
import sys
import os

#Open a file containing a list of the Parc Id, Names
#Those could be extracted directly from the url if needed.
parcInfoFile= 'ParcRequestInfo.txt'
f = open(parcInfoFile)
lines = f.readlines()
codeToProcess = len(lines)

#Remove tags around title and Data...
def GetData(line):
    start = line.find("<strong>")
    title = line[start+len("<strong>"):line.find("</strong>")]
    data = hline[line.find("</strong>")+len("</strong>"):line.find("<br")]
    return title, data

print "Parc,Piste de ski tracee a 12h,Pistes de marche denivellees a 12h, Piste de Ski, Piste de Marche, Glissade, Qualite d'enneigement, Precipitation dernieres 24h, Mise a Jour"
csv = []
for line in lines:
    #Remove end of lines
    line = line.strip()
    #Erase info after # on a line
    if line.find('#') != -1:
        line = line[1:line.find('#')]
    #Separate Elements
    elements = line.split(',')
    if len(elements) != 2:
        continue

    masterId = elements[0] #"81893832"
    parcName = elements[1] #"Bois-de-Liesse"

    pageBaseURL = "http://ville.montreal.qc.ca/portal/page?_pageid=174,13107595&_dad=portal&_schema=PORTAL"
    pageBaseURL += "&masterid=" + masterId
    pageBaseURL += "&nom_du_parc=" + parcName

    req = urllib2.Request(pageBaseURL)
    
    #Request page from Website
    try:
        pageBase = urllib2.urlopen(req)
    except URLError, e:
        print e.code
        print e.read()
        
    html = pageBase.read()
    HLS = html.split("\n")
   
    #Set Title
    
    #Print the name of the parc and conditions of ski
    print parcName + ",",

    conditionsItems = False

    for hline in HLS:
        hline = hline.strip()
        
        if conditionsItems:
            if hline.find("Ski") != -1:
                title,data = GetData(hline)
                #print title + " " + data            
                print data + ",",
            elif hline.find("Marche") != -1:
                title,data = GetData(hline)
                print data + ",",
                #print title + " " + data            
            elif hline.find("Glissade") != -1:
                title,data = GetData(hline)
                data = data[0:data.find("<")]
                print data + ",",
                #print title + " " + data            

                conditionsItems = False
            continue

        if hline.find("12 h") != -1:
            title,data = GetData(hline)
            print data + ",",
            #print title + " " + data
        elif hline.find("État général") != -1:
            conditionsItems = True
            #print hline
        elif hline.find("Qualité d'enneigement") != -1:
            title,data = GetData(hline)
            print data + ",",
            #print title + " " + data
        elif hline.find("Précipitations dans les dernières 24 h") != -1:
            title,data = GetData(hline)
            print data + ",",
            #print title + " " + data            
        elif hline.find("Mise à jour") != -1:
            title = "Mise à jour"
            data = hline[hline.find(title) + len(title):len(hline)]
            data = data[0:data.find("<")]
            print data,            
#print title + " " + data            



    print "\n",
            
#end

