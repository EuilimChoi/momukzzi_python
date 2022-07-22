from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import asyncio

# Create your views here.


class CrawlingView (APIView):
    def post (self, request):
        driver = webdriver.Chrome("/Users/choeuilim/Downloads/chromedriver")
        result = []

        async def crwaling(target):
            shopinfo = {"shopName" : target["place_name"],
                    "shoppic" :[],
                    "menu": []
                    }

            driver.get(target["place_url"])
            await asyncio.sleep(3)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

        
            pic = soup.find('ul',{'class':'list_photo photo_type5'})
            pics = pic.find_all('a')
            for p in pics :
                pp = p.get_attribute_list('style')
                picURL = pp[0][24:55] + "C320x320/" + pp[0][64:-1]
                shopinfo["shoppic"].append(picURL)


            try:
                menu = soup.find('ul',{'class':'list_menu'})
                menus = menu.find_all('li')
                for m in menus:
                    menu = m.find("span",{"class":"loss_word"}).get_text()
                    price = m.find("em",{"class":"price_menu"}).get_text()
                    menuSet = [menu, price[4:]]
                    shopinfo["menu"].append(menuSet)
            except:
                shopinfo["menu"].append(["메뉴 정보 없음","가격 정보 없음"])

            print(shopinfo)
            result.append(shopinfo)

        shops = request.data["data"]


        for shop in shops:
            asyncio.run(crwaling(shop))

        return Response(result)