import csv
import os
import re
import unittest
from xml.sax import parseString

from bs4 import BeautifulSoup


def get_listings_from_search_results(html_file):
    """
    Write a function that creates a BeautifulSoup object on html_file. Parse
    through the object and return a list of tuples containing:
     a string of the title of the listing,
     an int of the cost to rent for one night,
     and a string of the listing id number
    in the format given below. Make sure to turn costs into ints.

    The listing id is found in the url of a listing. For example, for
        https://www.airbnb.com/rooms/1944564
    the listing id is 1944564.
.

    [
        ('Title of Listing 1', 'Cost 1', 'Listing ID 1'),  # format
        ('Loft in Mission District', 210, '1944564'),  # example
    ]
    """

    listings = []
    pattern = "title"

    with open(html_file, 'r') as f:
        contents = f.read()
        s = BeautifulSoup(contents, 'html.parser')
        titles = s.find_all('div', id=re.compile('title_.+'))
        prices = s.find_all('span', class_=re.compile('_tyxjp1'))
        ids = s.find_all('meta',content=re.compile('www.airbnb.com/rooms/'))

    for i in range(len(titles)):
        id = re.search('(?<=\/rooms\/)[0-9]+', str(ids[i]))
        id_str = ''
        if id:
            id_str = id.group(0)
        else:
            id = re.search('(?<=\/rooms\/plus\/)[0-9]+', str(ids[i]))
            id_str = id.group(0)

        title = titles[i].text
        title = " ".join(title.split())
            
        listings.append((title, int(prices[i].text[1:]), id_str))

    return listings


def get_listing_information(listing_id):
    """
    Write a function to return relevant information in a tuple from an Airbnb listing id.
    NOTE: Use the static files in the html_files folder, do NOT send requests to the actual website.
    Information we're interested in:
        string - Policy number: either a string of the policy number, "Pending", or "Exempt"
            This field can be found in the section about the host.
            Note that this is a text field the lister enters, this could be a policy number, or the word
            "pending" or "exempt" or many others. Look at the raw data, decide how to categorize them into
            the three categories.
        string - Place type: either "Entire Room", "Private Room", or "Shared Room"
            Note that this data field is not explicitly given from this page. Use the
            following to categorize the data into these three fields.
                "Private Room": the listing subtitle has the word "private" in it
                "Shared Room": the listing subtitle has the word "shared" in it
                "Entire Room": the listing subtitle has neither the word "private" nor "shared" in it
        int - Number of bedrooms
.
    (
        policy number,
        place type,
        number of bedrooms
    )
    """