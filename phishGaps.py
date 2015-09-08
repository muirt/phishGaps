import os
from bs4 import BeautifulSoup
import glob
import re
import operator


#set these to True to download the html.  No need to download multiple times
downloadYears = True
downloadShows = True

findGaps = True


#1983-2015
validYears = range(1983,2016)


#download html of a full year of setlists
if downloadYears:
    for year in validYears:
        yearURL = "http://phish.net/setlists/" +str(year) + ".html"
        os.system("curl " + yearURL + " > " + str(year) + ".html")


#parse individual show links out of year html, and download each show html
if downloadShows:
    for year in validYears:

        #make directory if it doesn't exist yet
        if(str(year) not in os.listdir(".")):
            os.system("mkdir " + str(year))

        #parse html
        soup = BeautifulSoup(open(str(year) + ".html"), "lxml")

        #each setlist is inside a <div class="setlist"> tag
        dateDivs = soup.find_all('div', attrs={'class' : 'setlist'})

        #get the link for each show
        for div in dateDivs:
            #the link is inside <div><h2><a> tags
            link = div.h2.a
            if link.has_attr('href'):
                #separate out the date, to use as a file name
                date = str(link['href']).split("=")[1]
                setlistLink = str(link['href'])
                #download an individual show's setlist
                os.system("curl " + setlistLink + " > ./" + str(year) + "/" + date + ".html")

#iterate through all setlists, extracting gap number
if findGaps:
    gapDict = {}

    #make an output file to store results
    out_file = open("gapList.txt", "w")


    for year in validYears:

        #get list of files in each year folder
        folder = "./" + str(year) + "/*"
        fileList = glob.glob(folder)

        for fileName in fileList:

            #parse html
            soup = BeautifulSoup(open(fileName), "lxml")

            #check for show not counting toward official stats
            does_not_count = soup.find_all(string = re.compile('stats purposes'))

            #check for only soundchecks
            setlist_excluded = soup.find_all('div', attrs={'class' : "setlist excluded"})

            #if this is an official show, and not just a sound check
            if len(does_not_count) == 0 and len(setlist_excluded) == 0:

                #find <p> tag that contains gap number
                song_gap_tag = soup.find_all('a', href=re.compile('^/setlists/gapchart'))

                #find all returns a list, but this list is always 1 element long
                for gap in song_gap_tag:
                    #old shows with no gaps have an empty string, omit those
                    if len(gap.contents) > 0:
                        #extract date from file name
                        showDate = fileName[7:17]
                        #make dictionary entry from date and gap
                        gapDict[showDate] = float(gap.contents[0])

    #sort all shows by average gap, in descending order
    sorted_gaps = sorted(gapDict.items(), key=operator.itemgetter(1), reverse=True)

    index = 1

    #write list to file
    for show in sorted_gaps:
        out_file.write(str(index) + ". " + str(show) + "\n")
        index += 1

    #close file
    out_file.close()