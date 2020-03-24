# ZIP Code Downloader/Parser

I wanted a list of all the valid ZIP codes in the US. I wanted it to be
up-to-date, based on authoritative US Postal Service data. This turned out to
be less straightforward than I'd originally expected. I published this
package so other people wouldn't have to figure this out for themselves.

## Install

This program has two Python package dependencies: Requests and Requests-HTML.

If you don't know what Pipenv is, run this to install them:

```shell
pip install requests requests-html
```

If, on the other hand, you're a Pipenv person, run this instead:

```shell
pipenv install
```

## Run

```shell
python usps_parser.py
```

## What you get

Three files will be created:

* `AREADIST.TXT`: A data file in an obscure format, downloaded from the USPS website
* `output.txt`: A text file with all the ZIP codes, one per line
* `valid_zips.json`: A JSON file with one item: a list of all the ZIP codes

That's it!
