#!/usr/bin/env python3

# HOW TO CLEAN THE common.css FILE FROM "I DON T CARE ABOUT COOKIES"
# cat common-original.css | sed -e 's/{[^][]*}/,/g' | sed '/^$/d' | sed '/^\/\*/d' | sed '/^,$/d' | sed 's/,$//'  | awk '{printf("##%s\n", $0)}' > common-adb.txt

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import argparse
from urllib.parse import urlparse
from datetime import datetime
from selenium import webdriver
import os
import sys
import json
import time
import re

# Parse Vars
parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, default='https://www.repubblica.it')
parser.add_argument('--outfile', type=str, default='output.json')
parser.add_argument('--selectors', type=str, default="selectors.txt")
parser.add_argument('--accept_words', type=str, default="accept_words.txt")
parser.add_argument('--chrome_driver', type=str, default="./chromedriver")
parser.add_argument('--screenshot_dir', type=str, default=None)
parser.add_argument('--lang', type=str, default=None)
parser.add_argument('--timeout', type=int, default=5)
parser.add_argument('--clear_cache', action='store_true')
parser.add_argument('--try_scroll', action='store_true')
globals().update(vars(parser.parse_args()))

log_entries = []

def main():

    global driver
    global url

    # Fix Url
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    # Enable browser logging and start driver
    log("Starting Driver")
    d = DesiredCapabilities.CHROME
    #d['loggingPrefs'] = { 'performance':'ALL' }
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = Options()
    if lang is not None:
        options.add_experimental_option('prefs', {'intl.accept_languages': lang})
    driver = webdriver.Chrome(executable_path=chrome_driver, desired_capabilities=d, options=options)

    #  Go to the page, first visit
    log("Making First Visit")
    start_time=time.time()
    driver.get(url)
    end_time=time.time()
    log("First Visit PLT [s]: {}".format(end_time-start_time))
    time.sleep(timeout)
    before_data = get_data(driver)
    make_screenshot("{}/all-first.png".format(screenshot_dir))

    # Click Banner
    log("Clicking Banner")
    banner_data = click_banner(driver)
    if banner_data["matched_containers"] == [] and try_scroll:
        log("Trying with scroll")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(timeout)
    click_data = get_data(driver)
    make_screenshot("{}/all-click.png".format(screenshot_dir))

    #  Go to the page, second visit
    log("Making the Second Visit")
    if clear_cache:
        driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    start_time=time.time()
    driver.get(url)
    end_time=time.time()
    log("Second Visit PLT [s]: {}".format(end_time-start_time))
    time.sleep(timeout)
    after_data = get_data(driver)
    make_screenshot("{}/all-second.png".format(screenshot_dir))

    # Save
    data = {"first": before_data, "click": click_data, "second": after_data, "banner_data": banner_data,
            "log": log_entries}
    json.dump(data, open(outfile, "w"), indent=4)

    # Quit
    driver.quit()
    log("All Done")

def get_data(driver):

    #data = {"urls": [],"cookies": driver.get_cookies()}  # Worse than next line
    data = { "urls": [],
            "cookies": driver.execute_cdp_cmd('Network.getAllCookies', {})}

    log = driver.get_log('performance')

    for entry in log:
        message = json.loads(entry["message"])
        if message["message"]["method"] == "Network.responseReceived":
            url = message["message"]["params"]["response"]["url"]
            data["urls"].append(url)

    return data

def make_screenshot(path):

    if screenshot_dir is not None:
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        try:
            driver.save_screenshot(path)
        except Exception as e:
            log("Exception in making screenshot: {}".format(e))

def click_banner(driver):

    selectors_css = parse_rules(selectors, urlparse(driver.current_url).netloc)

    accept_words_list = open(accept_words, "r").read().splitlines()

    banner_data = {"matched_containers": [], "candidate_elements": []}
    contents = driver.find_elements_by_css_selector(selectors_css)
    screenshots = []

    for i, c in enumerate(contents):
        banner_data["matched_containers"].append({  "id": c.id,
                                                    "tag_name": c.tag_name,
                                                    "text": c.text,
                                                    "size": c.size,
                                                    "selected": True if i==0 else False,
                                                    })

        if screenshot_dir is not None:
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            try:
                c.screenshot("{}/matched-containers-{}.png".format(screenshot_dir,i))
            except Exception as e:
                log("Exception in making screenshot: {}".format(e))

    if len(contents) == 0:
        log("Warning, no banner found")
        return banner_data

    if len(contents) > 1:
        log("Warning, more than a cookie banner detected. Using the first.")

    candidate = None

    # Try Links, add the element itself in case
    links = contents[0].find_elements_by_tag_name("a")
    if contents[0].tag_name  == "a":
        links.append(contents[0])

    for c in links:
        if c.text.lower() in accept_words_list:
            candidate = c
            banner_data["candidate_elements"].append({  "id": c.id,
                                                        "tag_name": c.tag_name,
                                                        "text": c.text,
                                                        "size": c.size,
                                                        })

    # Try buttons, add the element itself in case
    btns = contents[0].find_elements_by_tag_name("button")
    if contents[0].tag_name  == "button":
        btns.append(contents[0])

    for c in btns:
        if c.text.lower() in accept_words_list:
            candidate  = c
            banner_data["candidate_elements"].append({  "id": c.id,
                                                        "tag_name": c.tag_name,
                                                        "text": c.text,
                                                        "size": c.size,
                                                        })
    # Click the candidate
    if candidate is not None:
        candidate.click()
        banner_data["clicked_element"] = candidate.id
    else:
        log("Warning, no matching candidate")

    return banner_data


def match_domains(domain, match):
    labels_domains = domain.strip(".").split(".")
    labels_match   = match.strip(".").split(".")
    return labels_match == labels_domains[-len(labels_match):]

def parse_rules(file_name, target_domain=""):
    
    selectors = []
    for line in open(file_name, "r").read().splitlines():

        if not line.startswith("!") and "##" in line:

            selector = re.search("(?<=##).+$",  line).group(0)

            domain_rules = re.search("^[a-zA-Z0-9-\\.~,]+(?=##)",  line)
                        
            if domain_rules is not None:
                domains = domain_rules.group(0).split(",")
                found_positive=False
                found_negative=False

                for domain in domains:
                    if domain.startswith("~") and match_domains(target_domain, domain[1:] ):
                        found_negative = True
                    elif match_domains(target_domain, domain):
                        found_positive = True
                        
                if found_positive and not found_negative:
                    selectors.append(selector)

            else:
                selectors.append(selector)

    return ", ".join(selectors)

def log(str):
    print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), str)
    log_entries.append( (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str) )

if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log("Exception at line {}: {}".format(exc_tb.tb_lineno, e))
        log("Quitting")
        driver.quit()


