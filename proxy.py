from selenium import webdriver
PROXY = "YOUR_PROXY_ADDRESS_HERE"
webdriver.DesiredCapabilities.FIREFOX['proxy']={
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "autodetect":False
}
driver = webdriver.Firefox()
driver.get('http://www.whatsmyip.org/')
