"""
Scrapes current ZIP code data from USPS website, and builds a list of all valid ZIP codes.

Copyright 2020 Syntexys Inc.
License: MIT
"""

import json

import requests
from requests_html import HTMLSession

# Scraping info
ZIP5_INTERSTITIAL_URL = "https://postalpro.usps.com/ais-viewer/areadist"
ZIP5_INTERSTITIAL_CSS = ".mt-1"

# Files
AREADIST_FN = "AREADIST.TXT"
OUTPUT_TXT_FN = "output.txt"
OUTPUT_JSON_FN = "valid_zips.json"

#  FILE LAYOUT FOR AREADIST.TXT
#
#  FIELD                                         RELATIVE
#  REFERENCE  FIELD                   LOGICAL    POSITION
#  NUMBER     DESCRIPTION             LENGTH     FROM/THRU   CONTENT NOTES
#  ---------  -----------             -------    ---------   -------------
#    01       AREA                      02         01 02
#    02       DISTRICT                  03         03 05
#    03       ZIP5                      05         06 10
AREA_PARAMS = (0, 2)
DISTRICT_PARAMS = (2, 3)
ZIP5_PARAMS = (5, 5)

def get_slice(data, slice):
    first = slice[0]
    last = first + slice[1]
    return data[first:last]

def parse():
    """
    Parse the data file once it's downloaded.
    """
    results = {}
    with open(AREADIST_FN) as areadist_f:
        areadist_lines = areadist_f.readlines()
        print(f"Lines in {AREADIST_FN}: {len(areadist_lines)}")

        for line in areadist_lines:
            area = get_slice(line, AREA_PARAMS)
            district = get_slice(line, DISTRICT_PARAMS)
            zip5 = get_slice(line, ZIP5_PARAMS)
            assert zip5 not in results
            results[zip5] = (area, district)
    
    print(f"Items in results: {len(results.keys())}")
    with open(OUTPUT_TXT_FN, "w") as output_f:
        output_f.write("\n".join(results.keys()))
    print(f"Wrote ZIP codes to {OUTPUT_TXT_FN}")

    with open(OUTPUT_JSON_FN, "w") as json_f:
        json.dump(list(results.keys()), json_f)
    print(f"Wrote JSON file {OUTPUT_JSON_FN}")

def download():
    """
    Download the data file from the USPS site.
    """
    # Scrape the interstitial page, which links to the actual data file.
    # We need to do this because it looks like the name of the data file fluctuates.
    session = HTMLSession()
    resp = session.get(ZIP5_INTERSTITIAL_URL)
    link = resp.html.find(ZIP5_INTERSTITIAL_CSS, first=True)

    # Download the data file.
    url_base = resp.request.url.replace(resp.request.path_url, "")
    new_url = url_base + link.attrs['href']
    resp2 = requests.get(new_url)

    # Save the data file.
    with open(AREADIST_FN, "wb") as saved_f:
        saved_f.write(resp2.content)
    print(f"Saved and wrote {AREADIST_FN}")

if __name__ == "__main__":
    download()
    parse()
