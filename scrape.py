# project: p3
# submitter: rrgeorge
# partner: none


import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from collections import deque
from graphviz import Digraph
from IPython.core.display import Image
import html5lib
import lxml
import heapq
import time

class Scraper:
    def __init__(self, driver, home_url):
        self.driver = driver
        self.home_url = home_url
        self.bfspwd = []
        self.dfspwd = []
        self.bfstodo = deque([self.home_url])
        self.dfstodo = [self.home_url]
        self.bfsvisited = set(self.bfstodo)
        self.dfsvisited = set(self.dfstodo)
        self.buttonThere = False

    # you can do these three with your group
    def easter_egg(self):
        self.driver.get(self.home_url)
        span = self.driver.find_elements_by_tag_name("span")
        l = []
        cat = ""
        for line in span:
            l.append(line.text)
        return cat.join(l)
    
    def page_urls(self, url):
        self.driver.get(url)
        links = self.driver.find_elements_by_tag_name("a")
        return [a.get_attribute("href") for a in links]
    
   
    def bfs_btn(self, url):
        self.driver.get(url)
        btn = self.driver.find_element_by_id("BFS")
        btn.click()
        return str(btn.get_attribute("innerHTML"))
    
    def dfs_btn(self, url):
        self.driver.get(url)
        btn = self.driver.find_element_by_id("DFS")
        btn.click()
        return str(btn.get_attribute("innerHTML"))
    
    def bfs_pass(self):
        # do the first thing on the list
        while len(self.bfstodo) > 0:
            cur_url = self.bfstodo.popleft()
            #print(cur_url)
            #gv.node(node_name(cur_url))
    
            children_urls = self.page_urls(cur_url)
    
            # add new things to the end of the list
            for child_url in children_urls:
                if not child_url in self.bfsvisited:
                    self.bfstodo.append(child_url)
                    self.bfsvisited.add(child_url)
                    self.bfspwd.append(self.bfs_btn(child_url))
                
        return "".join(self.bfspwd)
    
    def dfs_pass(self):
        cur_url = heapq.heappop(self.dfstodo)
        kids = self.page_urls(cur_url)
        for kid in kids:
            if kid not in self.dfsvisited:
                self.dfspwd.append(self.dfs_btn(kid))
                heapq.heappush(self.dfstodo, kid)
                self.dfsvisited.add(kid)
                self.dfs_pass()
        return "".join(self.dfspwd)

    # write the code for this one individually
    def protected_df(self, pwd):
        self.driver.get(self.home_url)
        pwd_entry = self.driver.find_element_by_id("password-input")
        pwd_entry.clear()
        btn = self.driver.find_element_by_id("attempt-button")
        pwd_entry.send_keys(pwd)
        btn.click()
        time.sleep(1)
        try:
            moreBtn = self.driver.find_element_by_id("more-locations-button")
            self.buttonThere = True
        except NoSuchElementException:
            pass
        if self.buttonThere == True:
            diff = 1
            while diff>0:
                table = self.driver.find_element_by_tag_name("table")
                df = pd.read_html(table.get_attribute("outerHTML"))[0]
                len1 = len(df)
                moreBtn.click()
                time.sleep(1)
                table = self.driver.find_element_by_tag_name("table")
                df = pd.read_html(table.get_attribute("outerHTML"))[0]
                len2 = len(df)
                diff = len2-len1
            table = self.driver.find_element_by_tag_name("table")
            df = pd.read_html(table.get_attribute("outerHTML"))[0]
        else:
            diff = 1
            while diff>0:
                table = self.driver.find_element_by_tag_name("table")
                df = pd.read_html(table.get_attribute("outerHTML"))[0]
                len1 = len(df)
                time.sleep(1)
                table = self.driver.find_element_by_tag_name("table")
                df = pd.read_html(table.get_attribute("outerHTML"))[0]
                len2 = len(df)
                diff = len2-len1
            table = self.driver.find_element_by_tag_name("table")
            df = pd.read_html(table.get_attribute("outerHTML"))[0]
        return df