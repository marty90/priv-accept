## Cookie Accept

Accept automatically the Cookie Warnings to allow automated measurements on web tracking.
It visits a URL and uses a heuristic to find the Cookie Banner and allow cookies.
It is based on the [I DON'T CARE ABOUT COOKIES 3.2.4](https://www.i-dont-care-about-cookies.eu/) CSS selectors and a set of keywords to find the right button/link.

Given a website, the tool accomplishes these tasks:

* Visits the website with a clean browser profile
* Clicks on the Cookie Accept bar, if one is found
* Re-visit the URL after the consent is given


### Prerequisites

You need Python 3 with the `selenium` library.

You also need Google Chrome and [chromedriver](https://chromedriver.chromium.org/) to allow Selenium using it.


### Usage

On a console

```
cookie-accept.py    [-h] [--url URL] [--outfile OUTFILE]
                    [--selectors SELECTORS] [--accept_words ACCEPT_WORDS]
                    [--chrome_driver CHROME_DRIVER]
                    [--screenshot_dir SCREENSHOT_DIR] [--lang LANG]
                    [--timeout TIMEOUT] [--clear_cache] [--headless]
                    [--try_scroll] [--global_search] [--full_net_log]
                    [--pre_visit]
```

* `url`: the url to visit
* `outfile`: the output file with the stats in JSON
* `selectors`: the list of selectors, in the [Adblock list format](https://help.eyeo.com/adblockplus/how-to-write-filters). By default, is uses the provided file
* `accept_words`: a file with the expressions that indicate cookie acceptance
* `chrome_driver`: the path to chrome_driver in your machine. By default, is searches on the local dir
* `screenshot_dir`: where to save some useful screenshot
* `lang`: the language to set. It can affect the Cookie Banner content
* `timeout`: the timeout to wait for extra-traffic after the onLoad events
* `clear_cache`: clear the cache after the first visit
* `headless`: run Chrome in headless mode. Note: in headless mode, the `clear_cache` cannot clean the DNS and socket cache due to limitations of Chrome
* `try_scroll`: try to scroll the page if no banner is found
* `global_search`: search accept words in the whole document
* `full_net_log`: store in the output file the details of the requests/responses
* `pre_visit`: make all visits as "second visits", so with cache e open sockets


### Output

The main output is a JSON file with various statistics, including all the HTTP requests fired at each stage, the cookies that are installed and some information about the found banners.

Moreover, it stores screenshots of the page and of the cookie banners found as well as the clicked element.




