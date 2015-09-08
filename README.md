# phishGaps
Scrape Phish.net for all setlists, then sort show dates by highest average song gap

Uses Python 2.7

Requred Packages:

Beautiful Soup 4 - http://www.crummy.com/software/BeautifulSoup/
  pip install beautifulsoup4

lxml - http://lxml.de/
  pip install lxml

Notes:
  The script is divided up into three blocks:
    Download year html
    Download individiual show html
    Find gaps
    
  If you plan to extend this, there is no need to download the html repeatedly.  Thus, each block has a run flag.
  
  
