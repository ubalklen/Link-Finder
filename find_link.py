print(
    "Link Finder\n"
    "This script scans a web page of a given URL and searches for a target link \n"
    "If the scanned page has a link to the same hostname as the URL given by the user, its destination page also scanned\n"
    "So potentially the whole site will be scanned (this may take hours!)\n"
    "All pages with the target link are saved on target-link-[date]-[time]-[random-ID].txt"
)

import os
import validators
import colorama
import queue
import datetime
from random import randint
from selenium import webdriver
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Colorama setup
colorama.init()

# URL setup
start_url = input("Site to scan: ")

while not validators.url(start_url):
    print("Invalid URL")
    start_url = input("Site to scan: ")

parsed_uri = urlparse(start_url)
hostname = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)

target_url = input("Link to be found on the site: ")
target_url = target_url.rstrip("/")

while not validators.url(target_url):
    print("Invalid URL")
    target_url = input("Link to be found on the site: ")


# Timer setup
start_time = datetime.datetime.now()

# Output file setup
datetime_string = start_time.strftime("%Y-%m-%d-%H-%M-%S")
script_path = os.path.dirname(os.path.abspath(__file__))
file_id = "".join(["%s" % randint(0, 9) for digit in range(0, 6)])
output_file_path = os.path.join(
    script_path, "target-link-" + datetime_string + "-" + file_id + ".txt"
)
output_file = open(output_file_path, "w", encoding="utf-8")

# We don't want to scan files (only web pages)
do_not_scan = (
    "#",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".doc",
    ".docx",
    ".odt",
    ".ods",
    ".jpg",
    ".png",
    ".zip",
    ".rar",
)

# Set used to flag visited pages and avoid multiple scans
scanned_pages = {start_url}

# Webdriver setup
options = webdriver.chrome.options.Options()
options.add_argument("--log-level=3")  # minimal logging
options.add_argument("--headless")
driver_path = os.path.join(script_path, "drivers", "chromedriver.exe")
driver = webdriver.Chrome(driver_path, options=options)
driver.implicitly_wait = 1

# Search for target link
output_file.write("Pages with the link " + target_url + " from " + start_url + "\n")
no_target = True
page_counter = 1
page_total = 1
page_queue = queue.Queue()
page_queue.put(start_url)

while not page_queue.empty():
    page = page_queue.get()
    print("Scanning " + page + " (" + str(page_counter) + "/" + str(page_total) + ")")
    page_counter = page_counter + 1
    target_link_found = False

    try:
        driver.get(page)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        link_list = soup.findAll("a")

        for link in link_list:
            link_url = urljoin(hostname, link["href"])
            link_text = link.text.strip()

            if target_url in link_url:
                if not target_link_found:
                    target_link_found = True
                    no_target = False
                    output_file.write("\n" + page + "\n")

                print(
                    colorama.Fore.GREEN
                    + "\t"
                    + str(link_url)
                    + " ("
                    + link_text
                    + ")"
                    + colorama.Style.RESET_ALL
                )
                output_file.write("\t" + str(link_url) + " (" + link_text + ")\n")

            link_parsed_uri = urlparse(link_url)
            link_hostname = "{uri.scheme}://{uri.netloc}/".format(uri=link_parsed_uri)

            if (
                link_hostname == hostname
                and link_url not in scanned_pages
                and not link_url.endswith(do_not_scan)
            ):
                page_queue.put(link_url)
                scanned_pages.add(link_url)
                page_total = page_total + 1
                print(
                    colorama.Fore.YELLOW
                    + "\t"
                    + link_url
                    + " added to scan queue"
                    + colorama.Style.RESET_ALL
                )

    except Exception as err:
        print(colorama.Fore.RED + "Could not scan " + page + colorama.Style.RESET_ALL)
        print(str(err))

driver.quit()

if no_target:
    output_file.seek(0)
    output_file.truncate()
    output_file.write(
        "Link to " + target_url + "have not been found from " + start_url + "\n"
    )

running_time = datetime.datetime.now() - start_time
farewell_msg = "\n" + str(page_total) + " pages scanned in " + str(running_time)
print("Scan completed!" + farewell_msg)
output_file.write(farewell_msg)
output_file.close()
