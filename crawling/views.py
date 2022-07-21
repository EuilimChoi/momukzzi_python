from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# Create your views here.


class CrawlingView (APIView):
    def post (self, request):
        driver = webdriver.Chrome("/Users/choeuilim/Downloads/chromedriver")
        target = request.data["data"][0]["place_url"]
        driver.get(target)
        driver.implicitly_wait(5)

        driver.execute_script('window.scrollTo(0, 200)')
        # tt = driver.find_element("xpath",'//*[@id="mArticle"]/div[3]/div[2]/div/a[1]')
        # ss = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/ul')
        driver.implicitly_wait(10)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # print(ss)

        return Response(str(soup))