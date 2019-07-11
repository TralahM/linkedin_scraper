from time import sleep
# from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from argparse import ArgumentParser
from parsel import Selector
from urllib.parse import unquote
import googlesearch

search_query = "site:linkedin.com/in/ AND {0}"


def findurls(searchquery):
    return [unquote(url) for url in googlesearch.search(searchquery, num=100, stop=100)]


def validate_field(field):
    if field is None:
        field = "None"
    return field


browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")

url = "https://www.linkedin.com/"


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-q", action='store', dest='query',
                        default="python developer", help="search query to find user profiles")
    parser.add_argument("-f", action="store", dest="fl",
                        default="linkedin_users.csv", help="filename csv to store the scraped profiles")
    parser.add_argument("-u --username", action='store',
                        dest='user', help='your linkedin email address')
    parser.add_argument("-p --password", action='store',
                        dest='password', help='your linkedin password')
    args = parser.parse_args()
    passwd = args.password
    email_addr = args.user
    searchq = search_query.format(args.query)
    writer = csv.writer(open(args.fl, "w"))
    writer.writerow(['Name', 'Job_Title', 'Company',
                     'College', 'Location', 'Connections', 'Image', 'URL'])
    browser.get(url)
    sleep(2)
    lgbtn = browser.find_element_by_css_selector(".nav__button-secondary")
    lgbtn.click()
    username = browser.find_element_by_css_selector('#username')
    username.send_keys(email_addr)
    sleep(.5)
    password = browser.find_element_by_css_selector('#password')
    password.send_keys(passwd)
    sleep(.5)
    login_button = browser.find_element_by_css_selector('.btn__primary--large')
    login_button.click()
    sleep(.5)
    linkedin_urls = findurls(searchq)
    for lurl in linkedin_urls:
        browser.get(lurl)
        sleep(1.3)
        job_title = ''
        company = ''
        college = ''
        connections = ''
        name = ''
        location = ''
        profile_pic = ''
        linkedin_url = lurl
        try:
            profile_pic = browser.find_element_by_css_selector(
                ".pv-top-card-section__photo").get_attribute("src")
            name = browser.find_element_by_xpath(
                "/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[1]/li[1]").text.strip()
            job_title = browser.find_element_by_xpath(
                "/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/h2").text.strip()
            location = browser.find_element_by_xpath(
                "/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[2]/li[1]").text.strip()
            company = browser.find_element_by_xpath(
                "/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[2]/ul/li/span/span[1]").text.strip()
            college = browser.find_element_by_xpath(
                '/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[2]/ul/li[2]').text.strip()
            connections = browser.find_element_by_xpath(
                "/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[2]/li[2]/span").text.strip()
            linkedin_url = lurl
        except:
            pass
        print("Name: "+name, ",Job Title: "+job_title, ",Company: "+company,
              ",College: "+college, ",Location: "+location, ",Connections: "+connections, ",URL: "+linkedin_url, "\n")
        writer.writerow([name.encode('utf-8'), job_title.encode('utf-8'), company.encode("utf-8"),
                         college.encode("utf-8"), location.encode("utf-8"), connections.encode("utf-8"), profile_pic, linkedin_url.encode("utf-8")])

    browser.close()
