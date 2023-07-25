# UFCAnalysis

A web scraping script used to scrape UFC data from http://ufcstats.com/. 

## Project Description

The scrapeUFC.py script will use BeautifulSoup to parse HTML from [UFCStats](http://ufcstats.com/statistics/events/completed?page=all).
It will then begin to gather fight stats from each individual fight found in each fight card 
from the very first ufc event. 
Once the data has been parsed, the script will begin to clean and append to a list and continue to do so until it is done with each fight.
When it is done it will upload all of the data to Microsoft SQL Server ready for data validation and exploration.

## Getting Started

Best if ran with Python version 3.9.15 or higher 

### Prerequisites

You will need to install the BeautifulSoup, Pandas, re, workbook, and the sqlalchemy library.

```
npm install BeautifullSoup
npm install Pandas
npm install re
npm install workbook
npm install sqlalchemy
```

## Authors

* **Axel Diaz** - [adiaz50](https://github.com/adiaz50)

## Acknowledgments

* Inspiration from UFC fighters and the entertainment they give us.
* Would also like to thank [Andrew Couch](https://github.com/andrew-couch) for the explanations found in his videos.
