from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from django.db import transaction
from .serializers import ShopInfoSerializer,ShopPicSerializer,ShopMenuSerializer
import time
import asyncio

# Create your views here.
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)

class CrawlingView (APIView):
    def post (self, request):
        webdriver_options = webdriver.ChromeOptions()
        webdriver_options.add_argument('headless')
        driver = webdriver.Chrome("/Users/choeuilim/Downloads/chromedriver")
        shops = request.data["data"]
        result = []


        def crwaling(target):
            
            for urls in target:
                driver.execute_script("window.open('"+urls["place_url"]+"')")

            # 모든 브라우져 열기

            driver.switch_to.window(driver.window_handles[1])

            time.sleep(3)
            browser = driver.window_handles

            for i in range(1,len(browser)):
                shopinfo = {"shopName" : target[0-i]["place_name"],
                            "shopId" : target[0-i]["id"],
                            "location" : target[0-i]["road_address_name"],
                            "phoneNumber" : target[0-i]["phone"],
                            "shoppic" :[],
                            "menu": []
                            }

                driver.switch_to.window(driver.window_handles[i])
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    pic = soup.find('ul',{'class':'list_photo photo_type5'})
                    pics = pic.find_all('a')
                    for p in pics :
                        pp = p.get_attribute_list('style')
                        picURL = pp[0][24:55] + "C320x320/" + pp[0][64:-1]
                        shopinfo["shoppic"].append(picURL)
                            
                        try:
                            menu = soup.find('ul',{'class':'list_menu'})
                            menus = menu.find_all('li')
                            print(menus)

                            for m in menus:
                                menu = m.find("span",{"class":"loss_word"}).get_text()
                                price = m.find("em",{"class":"price_menu"}).get_text()
                                menuSet = [menu, price[4:]]
    
                                shopinfo["menu"].append(menuSet)
                        except:
                            shopinfo["menu"].append(["메뉴 정보 없음","가격 정보 없음"])

                except:
                    print("로딩 에러 인듯")    

                # dbsaveLogic(shopinfo)
                result.append(shopinfo)

        def dbsaveLogic(shopinfo):
            print(shopinfo)
            shopinfos = {"shopName" : shopinfo["shopName"],
                        "shopId" : shopinfo["shopId"],
                        "location" : shopinfo["location"],
                        "phoneNumber" : shopinfo["phoneNumber"]}

            shopinfoserializer = ShopInfoSerializer(data = shopinfos)

            if shopinfoserializer.is_valid():
                shopinfoserializer.save()
            else :
                print("Not saved!!!!!!!!")
            
            for i in shopinfo["shoppic"]:
                shoppicserializer=ShopPicSerializer(data = {"shopId" : shopinfo["shopId"],"URL":i})
                if shoppicserializer.is_valid():
                    shoppicserializer.save()

            for i in shopinfo["menu"]:
                shopmenuserializer=ShopMenuSerializer(data = {"shopId" : shopinfo["shopId"],"menu":i[0],"price":i[1]})
                if shopmenuserializer.is_valid():
                    shopmenuserializer.save()

            print(shopinfo["shoppic"])





        crwaling(shops)
        driver.close()

        return Response(result)