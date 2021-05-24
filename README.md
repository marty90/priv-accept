## Priv-Accept

Accept automatically the Privacy Policies to allow automated measurements of the web as real users experience.
Priv-Accept visits a URL and uses a heuristic to find and click the accept button on privacy policies.
It is based on a set of keywords to find the right button/link.

Given a website, the tool accomplishes these tasks:

* Visits the website with a fresh browser profile
* Clicks on the Accept button, if one is found
* Re-visits the URL after the consent is given
* Stores a rich log files containing metadata on the visits, including all URLs, installed cookies and performance metrics (e.g., OnLoad time)


### Prerequisites

You need Python 3 with the `selenium` library. You also need Google Chrome and [chromedriver](https://chromedriver.chromium.org/) to allow Selenium using it.

Priv-Accept can also be built in a Docker image to allow parallel and isolated experiment. You can build the Docker image using the `Dockerfile` provided in this repo. The images extends the [BrowserTime](https://www.sitespeed.io/documentation/browsertime/) image to profit from the ready-to-use setup.


### Usage

Priv-Accept runs via command line and accept the following arguments:

```
priv-accept.py    [-h] [--url URL] [--outfile OUTFILE]
                    [--accept_words ACCEPT_WORDS]
                    [--chrome_driver CHROME_DRIVER]
                    [--screenshot_dir SCREENSHOT_DIR] [--lang LANG]
                    [--timeout TIMEOUT] [--clear_cache] [--headless]
                    [--try_scroll] [--global_search] [--full_net_log]
                    [--pre_visit] [--rum_speed_index]
                    [--visit_internals] [--num_internal]
                    
```
* `-h`: print the help
* `--url URL`: the url to visit
* `--outfile OUTFILE`: the output file with the metadata in JSON
* `--accept_words ACCEPT_WORDS`: a file with the expressions that indicate cookie acceptance
* `--chrome_driver CHROME_DRIVER`: the path to chrome_driver in your machine. By default, is searches on the current directory
* `--screenshot_dir SCREENSHOT_DIR`: where to save the screenshots of the visits and clicked element
* `--lang LANG`: the language to set. It can affect the Cookie Banner content
* `--timeout TIMEOUT`: the timeout to wait for extra-traffic after the onLoad events
* `--clear_cache`: clear the cache after the first visit
* `--headless`: run Chrome in headless mode. Note: in headless mode, the `clear_cache` cannot clean the DNS and socket cache due to limitations of Chrome
* `--try_scroll`: try to scroll the page if no banner is found
* `--user_agent`: override Chrome User Agent
* `--full_net_log`: store in the output file the details of the requests/responses
* `--pre_visit`: make all visits as "second visits", so with warm cache and open sockets
* `--rum_speed_index`: compute the [RUM Speed Index](https://github.com/WPO-Foundation/RUM-SpeedIndex)
* `--visit_internals`: also visit internal pages, randomnly choosen
* `--num_internal`: number of internal pages to visit, if `--visit_internals`

### Output

The main output is a JSON file with various statistics, including all the HTTP requests fired at each stage, the cookies that are installed and some information about the found banners. You can can also find performance metrics such as OnLoad time and DOMLoaded time. It can compute the RUM Speed Index. Notice that performance metrics depend on whether you fisit the page with a fresh or non-fresh browser profile.

Moreover, it stores screenshots of the page and of the cookie banners found as well as the clicked element.




