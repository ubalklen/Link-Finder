# Link Finder
A Python script that scans a given web page (haystack) and searches for a given link (needle) on it.

If the page has a link to the same hostname as the web page given by the user, its destination page also scanned. It works like a web crawler, so potentially the whole site will be scanned. Be aware that this may take hours.

All links found are saved on *target-link-[date]-[time]-[random-ID].txt*.

# Requisites
Chrome 75 (put the [proper driver](http://chromedriver.chromium.org/downloads) in [drivers](https://github.com/ubalklen/Link-Finder/tree/master/drivers) folder if you have another version)

Python 3 (it has been tested on Python 3.7)

Some additional Python modules (check the [script](https://github.com/ubalklen/Link-Finder/blob/master/find_link.py))

# Details
The script scans pages using [Selenium](https://selenium-python.readthedocs.io/) to account for links that may be injected via JavaScript.