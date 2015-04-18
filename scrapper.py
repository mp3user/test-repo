import pdb
import time
import urllib
import urllib2
import re
import sys
import os
import shutil
import codecs
import unicodedata
from bs4 import BeautifulSoup

#debugger, just in case :S
#pdb.set_trace()
print("Some scrapper for ebay or aliexpress, 2014\n")
print("\n")

#Create Input.csv
file = open("input.csv", "w")
file.close()
#Set counter to 0
i=0

urlinn = raw_input('Number of search pages you want to enter:\n')
urlinnn=int(urlinn)
for i in range(0, urlinnn):
 print "Please copy & paste search page URL #",i+1,":"
 urlin = raw_input('')
 soup = BeautifulSoup(urllib2.urlopen(urlin).read())
 for link in soup.findAll('a',{'itemprop':'name'}):
     url = link.get('href')
     file = open("Input.csv", "a")
     file.write(url)
     file.write(",")
     file.close()
#Delete the last comma so it doesn't screw up the processing later
with open("input.csv", 'rb+') as filehandle:
    filehandle.seek(-1, os.SEEK_END)
    filehandle.truncate()    
print "Done."   

dlcheck = raw_input('Do you want to download the product pictures? (y/n)\n')
print("\n")
#if the images folder doesn't exist, create a new one
if dlcheck == "y":
 if not os.path.exists('images'):
  os.mkdir('images')


print("Reading input file...")
#open and read Input.csv, split at commas and create a list of URLs

try:
 with open('input.csv') as f:
     content = f.read().split(',')
 print("Input file read.")
 print("Creating output file...")
 #create the Output.csv file and write a header
 file = open("Output.csv", "w")
 file.write('Name,Price,icIMG URL\n')
 file.close()
#get list lenght
 llen=content.__len__()
 #throw an error if the list is invalid
 if llen==1:
  print "Hey! The Input file is empty!"
  print "Please put some URLs in there."
  wait = input("Press Enter to exit and try again.")
#state the number of detected valid URLs
 print "Detected",llen," valid URLs."
 print "\n"
 print "\n"

#fatal error... Hope this doesn't happen :(
except IOError:
   print "Oh dear\
   Something went horribly wrong.\n\
   Did you place the Input.csv file into the dist folder \nlike the readme told you to?\
   Do you have the Input file open in some program?\
   Did you give the Input file the correct name?\n"
   wait = input("Press Enter to exit and try again.")

#set counter "i" to 0 and error checker "checker" to None
i=0
errcheck = None

#The main loop. Go through the loop until every list item has been processed
try:
 for i in range(0, llen):
  print "Reading URL #",i+1,"/",llen
  url=content[i]
  doc = urllib2.urlopen(url).read()
  soup = BeautifulSoup(''.join(doc))
#Find the title and write it to the Output file
  try:
   s = soup.find('h1').text

   print s

   file = codecs.open('Output.csv','a','windows-1252')
   file.write('"')
   file.write(s)
   file.write('"')
   file.write(',')
   file.close()
  except:
   print "Product title not readable! Writing as UTF-8 instead... " 
   file = codecs.open('Output.csv','a','utf-8')
   file.write('"')
   file.write(s)
   file.write('"')
   file.write(',')
   file.close()
   errcheck = True
#Find the price and write it to the Output file   
  try:
   ppr = soup.find('span',{'class':'notranslate'}).text
   print "Found article price:"
   print ppr
   newpr = ppr.replace("EUR ", "")
   file = open("Output.csv", "a")
   file.write('"')
   file.write(newpr)
   file.write('"')
   file.write(",")
   file.close()
  except:
    print 'No product price found. Are you sure this URL leads to an eBay article?\n'
    file = open("Output.csv", "a")
    file.write('"')
    file.write(' ')
    file.write('"')
    file.write(",")
    file.close()
    errcheck = True
#Find the icIMG URL and write it to the Output file     
  try:
   imgurl = soup.find('img',id="icImg")['src']
   print "Found picture URL:"
   print imgurl
   file = open("Output.csv", "a")
   file.write('"')
   file.write(imgurl)
   file.write('"')
   file.write(",\n")
   file.close()
   i+=1
   if dlcheck == "y":
    print "Downloading image"

    urllib.urlretrieve(imgurl, os.path.join("images", str(i)+".jpg"))
   print "\n"
  except:
    print 'No icImg ID found. Are you sure this URL leads to an eBay article?\n'
    errcheck = True
#Fatal error again :(
except:   
   print 'Oh dear.\n'
   print 'Something went horribly wrong.\n'
   print 'The Input file is corrupt!'
   print 'Did you check the Input.csv file for mistakes?'
   print 'Pay attention to double commas!'
   file = open("Output.csv", "w")
   file.write('')
   file.close()
   wait = input("Press Enter to exit and try again.")  


#Done :D
print "\n"
print "\n"
print "Done! \n"
print "The data has been saved to Output.csv \n"
#If the program saved images, point the user to their direction
if dlcheck == "y":
 print "The images have been saved to the /images/ folder. \n"
#Warn the user if there have been errors.
if errcheck == True:
 print "WARNING:"
 print "There were encoding errors during processing."
 print "That means that some product titles may not be written correctly\n into the .csv file."
 print "I recommend checking the Output.csv file for mistakes\n and fixing them manually."
#The end!
wait = input("Press Enter to continue.")