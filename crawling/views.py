from tkinter import Menu
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from django.db import transaction
from .serializers import ShopInfoSerializer,ShopPicSerializer,ShopMenuSerializer
from .models import Shopinfo, Shopmenu, Shoppic
import time
import asyncio

# Create your views here.
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)

class CrawlingView (APIView):
    def post (self, request):
        webdriver_options = webdriver.ChromeOptions()
        webdriver_options.add_argument('headless')
        driver = webdriver.Chrome("/Users/choeuilim/Downloads/chromedriver",options=webdriver_options)
        shops = request.data["data"]
        crawling = []
        result = []


        def crwaling(target):
            print("크롤링 시작!!!!!!!!!")
            for urls in target:
                driver.execute_script("window.open('"+urls["place_url"]+"')")

            # 모든 브라우져 열기

            driver.switch_to.window(driver.window_handles[1])

            time.sleep(3)
            browser = driver.window_handles

            for i in range(1,len(browser)):
                shopinfo = {"shopName" : target[0-i]["place_name"],
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

                        for m in menus:
                            menu = m.find("span",{"class":"loss_word"}).get_text()
                            price = m.find("em",{"class":"price_menu"}).get_text()
                            menuSet = [menu, price[4:]]

                            shopinfo["menu"].append(menuSet)
                    except:
                        shopinfo["menu"].append(["메뉴 정보 없음","가격 정보 없음"])
                except:
                    print("로딩 에러 인듯")    

                with transaction.atomic():
                    dbsaveLogic(shopinfo)
                    result.append(shopinfo)


        def dbsaveLogic(shopinfo):
            shopinfos = {"shopName" : shopinfo["shopName"],
                        "location" : shopinfo["location"],
                        "phoneNumber" : shopinfo["phoneNumber"]}

            shopinfoserializer = ShopInfoSerializer(data = shopinfos)

            if shopinfoserializer.is_valid():
                shopinfoserializer.save()
            else :
                print("Not saved!!!!!!!!")
            
            shopid = Shopinfo.objects.get(shopName=shopinfo["shopName"],location = shopinfo["location"],phoneNumber = shopinfo["phoneNumber"])
            for i in shopinfo["shoppic"]:
                shoppicserializer=ShopPicSerializer(data = {"shopId_id":int(shopid.id),"URL":i})
                if shoppicserializer.is_valid():
                    shoppicserializer.save()
                else:
                    print("사진 저장 오류")

            for i in shopinfo["menu"]:
                shopmenuserializer=ShopMenuSerializer(data = {"shopId_id" :int(shopid.id),"menu":i[0],"price":i[1]})
                if shopmenuserializer.is_valid():
                    shopmenuserializer.save()
                else:
                    print("메뉴 저장 오류")



        def cheakShopInDB(shopinfo):
            try:
                shoppic = []
                menu = []
                shopinfoInDB = Shopinfo.objects.get(shopName=shopinfo["place_name"],location = shopinfo["road_address_name"],phoneNumber = shopinfo["phone"])
                if shopinfoInDB:
                    print("디비에 있음")
                    id = shopinfoInDB.id
                    shopinfomation = Shopinfo.objects.filter(id=id).values()
                    pics = Shoppic.objects.filter(shopId_id=id).values()
                    menus = Shopmenu.objects.filter(shopId_id=id).values()

                    for pic in pics :
                        shoppic.append(pic["URL"])

                    for m in menus:
                        menu.append([m["menu"],m["price"]])
                        
                    
                    making = {"shopName" : shopinfomation[0]["shopName"],
                                "location" : shopinfomation[0]["location"],
                                "phoneNumber" : shopinfomation[0]["phoneNumber"],
                                "shoppic" : shoppic,
                                "menu": menu
                                }
                    result.append(making)
            except:
                crawling.append(shopinfo)


        def main(shoplist):
            print("main!!")
            for shop in shoplist:
                cheakShopInDB(shop)
            
            if len(crawling) > 0 :
                crwaling(crawling)


        main(shops)
        driver.close()


        return Response(result)