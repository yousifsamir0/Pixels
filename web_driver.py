import asyncio.log
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import compare_blob_image_with_disk


# c_options = Options()
# c_options.add_experimental_option("debuggerAddress", "localhost:8989")
# # Initialize the WebDriver with the existing Chrome instance
#self.driver = webdriver.Chrome(options=c_options)
# market_input =self.driver.find_element(By.XPATH,"//*[contains(@id, '__next')]")


class Chrome():
    _instance = None
    def __init__(self) -> None:
        c_options = Options()
        c_options.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(options=c_options)
        self.driver.bidi_connection()
        self.actions = ActionChains(self.driver)
    def __new__(cls,*args, **kwargs) :
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def force_click_element(self,element):
        self.driver.execute_script("arguments[0].click();", element)
         

    def get_energy(self):
            try:              
                energyEl =self.driver.find_element(By.XPATH,"//*[contains(@class, 'Hud_energytext')]")
                return float(energyEl.text.strip().replace(',',''))
            except:
                print('[log:get_energy]:: could not find energy')
                return -1
    def get_gold(self):
            try:              
                goldElement =self.driver.find_element(By.XPATH,'//*[contains(@class,"commons_coinBalance_")]')
                # print('from gold itself: ',float(goldElement.text.strip().replace(',', '')))
                return int(goldElement.text.strip().replace(',', ''))
            except:           
                print('[log:get_gold]:: could not find gold')
                return -1
    def open_land(self):
        try:
            openLand_btn =self.driver.find_element(By.XPATH,"//*[contains(@class, 'Hud_topLeftBackground')]//button[1]")
            openLand_btn.click()
            return True
        except:
            print('[log:open_land]:: could not find landbtn')
            return False
        
    def travel_bookmark(self):
        try:
            opened=self.open_land(self.driver)
            if not opened: return False
            bookmark_btn =self.driver.find_element(By.XPATH,"//*[contains(@class, 'LandAndTravel_tabs')]//button[3]")
            bookmark_btn.click()
            bookmarks =self.driver.find_element(By.XPATH,"//*[contains(@class, 'LandAndTravel_mapsSquare')]")
            print(bookmarks.text)
            return True
        except:
            print('[log:open_land]:: could not find landbtn')
            return False     
    def sell(self,itemName,price):
        try:
            create_btn =self.driver.find_element(By.XPATH,"//*[contains(@class, 'Infiniportal_tabButtonsContainer')]//button[2]")
            create_btn.click()
            listings =self.driver.find_elements(By.XPATH,"//*[contains(@class, 'MarketplaceListings_listing_')]")
            for item in listings:
                item_data = item.text.split('\n')
                item_name = item_data[0]
                item_quantity = item_data[1]
                if itemName.lower() == item_name.lower():
                    item.find_element(By.TAG_NAME,'button').click()
                    self.driver.find_elements(By.TAG_NAME,'input')[0].clear()
                    self.driver.find_elements(By.TAG_NAME,'input')[0].send_keys(int(price))
                    self.driver.find_elements(By.TAG_NAME,'input')[1].clear()
                    self.driver.find_elements(By.TAG_NAME,'input')[1].send_keys(int(item_quantity))
                    self.driver.find_element(By.XPATH,'//button[contains(@class,"MarketplaceAddListing_button")]').click()
                    return True
            return False
        except:
            print('[log:sell] could not sell')
            return False
    def buy(self,itemName,count,maxPrice):
        # try:
            localCount = count
            if localCount*maxPrice > self.get_gold():
                localCount = int(self.get_gold()/maxPrice)

            view_listing_btn=None
            input =self.driver.find_element(By.TAG_NAME,"input")
            input.clear()
            input.send_keys(itemName.lower())
            listings =self.driver.find_elements(By.XPATH,"//*[contains(@class, 'Marketplace_item_')]")
            for item in listings:
                # print(item.text)
                item_data = item.text.split('\n')
                print(item_data)
                item_name = item_data[0]
                if itemName.lower() == item_name.lower():
                    print('found')
                    view_listing_btn=item.find_element(By.TAG_NAME,'button')
            current_g = self.get_gold()
            buyCooldown=False
            while(localCount!=0):
                if buyCooldown:
                    time.sleep(2.5)
                    buyCooldown = False
                # for i in range(10):
                view_listing_btn.click()
                listing = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "MarketplaceItemListings_buyListing")]')))
                print(listing.text)
                listing_data = listing.text.split('@')
                listing_price = int(listing_data[-1].strip().replace(',',''))
                listing_count = int(listing_data[-2].split(':')[-1].strip().replace(',',''))
                print('price: is {} and count is {}'.format(listing_price,listing_count))
                if listing_price>maxPrice:
                    x_btn =self.driver.find_elements(By.XPATH,"//*[contains(@class, 'commons_modalBackdrop')]//button[contains(@class,'commons_closeBtn')]")[1]
                    x_btn.click()
                    continue
                buy_count = min(localCount,listing_count)
                listing.click()

                price_input =self.driver.find_element(By.XPATH,"//*[contains(@class, 'MarketplaceItemListings_amount')]//input")
                price_input.clear()
                price_input.send_keys(buy_count)

                buy_button =self.driver.find_element(By.XPATH,"//*[contains(@class, 'MarketplaceItemListings_buyListing')]")
                buy_button.click()
                notification = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "Notifications_text_")]')))
                # if self.get_gold() != current_g:
                print(notification.text)
                self.force_click_element(notification)
                if '+' in notification.text:
                    print(current_g)
                    print(self.get_gold())
                    current_g = self.get_gold()
                    localCount -= buy_count
                    buyCooldown = True
                    self.driver.find_element(By.XPATH,'//*[contains(@class, "Marketplace_buyContent")]//button[1]').click()
                    time.sleep(0.5)
                x_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class,"MarketplaceItemListings_container_")]//button[1]')))
                x_btn.click()
                
        # except:
        #     print('[log:Buy] could not Buy')
        #     return False
    def get_items(self):
        actions = ActionChains(self.driver)
        while(True):
            self.driver.implicitly_wait(2)
            items=self.driver.find_elements(By.XPATH,"//*[contains(@class, 'Hud_item_')]")
            # print(len(items))
            item_shortcut = int(items[0].get_attribute('textContent').split('x')[0])
            if item_shortcut == 1:
                return items
            actions.send_keys(Keys.TAB).perform()
        
    def get_item_count(self,item_blob):
        self.get_items()
        items=self.driver.find_elements(By.XPATH,"//*[contains(@src, 'blob:')]")
        count=0
        for item in items:
            if compare_blob_image_with_disk(self.driver,item.get_attribute('src'),item_blob):
                quatity = item.find_element(By.XPATH,'../..//div[contains(@class, "Hud_quantity_")]').get_attribute('textContent').split('x')[-1].strip()
                count += 1 if quatity=='' else int(quatity)
        return count
    def item_get_slot(self,item_blob)-> int:
        items=self.driver.find_elements(By.XPATH,"//*[contains(@src, 'blob:')]")
        for item in items:
            if compare_blob_image_with_disk(self.driver,item.get_attribute('src'),item_blob):
                slot_number = item.find_element(By.XPATH,'../..//div[contains(@class, "Hud_shortcut_")]').get_attribute('textContent').strip()
                return int(slot_number)
    def expand_items_if_not(self):
        if len(self.driver.find_elements(By.XPATH,"//*[contains(@class, 'Hud_expanded_')]")):
            return
        self.actions.send_keys('b').perform()
        time.sleep(1)
    def swap_slots(self,oldSlot,newSlot):
        self.expand_items_if_not()
        self.actions.send_keys(Keys.ESCAPE).perform()
        items = self.get_items()
        items[oldSlot-1].click()
        time.sleep(0.15)
        items[newSlot-1].click()
        self.actions.send_keys(Keys.ESCAPE).perform()
    def put_item_in_slot(self,item_blob,slotNumber):
        oldSlot = self.item_get_slot(item_blob)
        if oldSlot == slotNumber:return
        self.swap_slots(oldSlot,slotNumber)



    # Items.pw.startIntercept(1019)
    # print('started')
    # time.sleep(5)
    # Items.pw.stopIntercept()
if __name__=='__main__':

    # c = Chrome()
    # input()
    from driver.pixels_driver import Items,Market
    from driver.core.parser import WebSocketParser
    from driver.core.commands import cut_trees_command,collect_wood_command,use_item_on_self_command
    from Tasks import buy_from_hazel,go_sell_items
    Items.cookis_login(34,100)
    Items.travel_bookmark(1019)
    # Items.driver.sendWS(use_item_on_self_command('honey',4))
    # go_sell_items()
    # buy_from_hazel('butterberryseeds',1)
    
    # data = Items.driver.evaluate_handle(f"JSON.parse('{json.dumps([1,2,3,[4,5,6]])}')")
    # wsProto=Items.driver.evaluate_handle('WebSocket.prototype')
    # instances = Items.driver.queryObjects(wsProto)
    # fn = '''(instances,data)=>{{
    #     let instance = instances[0];
    #     console.log(data)
    #     console.log(instance)
    # }}'''
    # Items.driver.execute_func_on(fn,instances,data)


    # driver = Items.driver.driver

#     remoteObject = driver.execute_cdp_cmd('Runtime.evaluate', {
#                     'expression': 'WebSocket.prototype',
#                     'returnByValue': False,
#                     'awaitPromise': True,
#                     'userGesture': True,
#                 }).get('result')
#     wsArr = driver.execute_cdp_cmd('Runtime.queryObjects', {
#             'prototypeObjectId': remoteObject.get('objectId'),
#         }).get('objects')
#     print(wsArr)

#     jsFunction = f'''(instances,data)=>{{
#         console.log(instances)
        
#     }}
# '''
#     driver.execute_cdp_cmd('Runtime.callFunctionOn', {
#                 'functionDeclaration': f'{jsFunction}\n',
#                 # 'objectId':wsArr.get('objectId'),
#                 'executionContextId':wsArr.get('objectId'),
#                 'arguments':[{'objectId':wsArr.get('objectId')}],
#                 'returnByValue': False,
#                 'awaitPromise': True,
#                 'userGesture': True,
#             })



    time.sleep(1000)



    # Items.travel_bookmark(334)
    # Items.driver.sendWS(plant_command(WebSocketParser.ent_soil[:10],'popberrySeeds'))
    # time.sleep(1)
    # Items.driver.sendWS(water_command(WebSocketParser.ent_crops[:10]))
    # time.sleep(60)
    # Items.driver.sendWS(shear_command(WebSocketParser.ent_crops[:10]))


    # time.sleep(1000)
    # input('input')
    # Items.pw.startIntercept(1019)
    # # print(Items.get_gold())
    # print(Items.driver.driver.requests)
    # print('done,waiting to retravel ')
    # Market.driver.attach_sock()
    # time.sleep(10)
    # Market.driver.attach_sock()
    # from net.server import Server
    # server = Server('192.168.1.105', 12345)
    # server.wait_for_connections()
    # t = time.time()
    # # print(Items.get_item_count('shears.png'))
    # print(Items.is_slot_selected(3))
    # print(time.time()-t)
#     script = '''(ob)=>{
#     console.log(ob);
#     let instance = ob[0];
#     console.log(instance);
#     //instance.send(new Uint8Array([13, 162, 117, 105, 132, 162, 105, 100, 177, 105, 116, 109, 95, 112, 111, 112, 98, 101, 114, 114, 121, 83, 101, 101, 100, 115, 164, 116, 121, 112, 101, 166, 101, 110, 116, 105, 116, 121, 164, 115, 108, 111, 116, 1, 163, 109, 105, 100, 184, 54, 53, 102, 98, 100, 100, 102, 55, 98, 48, 57, 101, 102, 53, 97, 52, 49, 49, 57, 51, 102, 53, 100, 50]).buffer)
# }
# '''
#     c.driver.execute_cdp_cmd('Runtime.callFunctionOn',{'functionDeclaration':script,'objectId':oId})
#     # c.driver.execute_script(script,instances)






    # print(c.driver.execute_cdp_cmd("queryObjects(WebSocket)"))
    # time.sleep(5)
#     print(c.driver.execute_cdp_cmd("Runtime.evaluate",{
    # "expression": "queryObjects(WebSocket)",
    # "includeCommandLineAPI": True,
    # "silent": False,
    # "generatePreview": True,
    # "userGesture": False,
    # "awaitPromise": False,
    # "throwOnSideEffect": True,
    # "timeout": 500,
    # "disableBreaks": True,
    # "replMode": True,
# }))
    # cookies=c.driver.get_cookie('pixels-session')
    # c.driver.delete_all_cookies()
    # c.driver.refresh()
    # time.sleep(5)
    # c.driver.add_cookie(cookies)
    # c.driver.refresh()
    # start = WebDriverWait(c.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class,"Intro_startbutton_")]')))
    # print('done')
    # cookies=c.driver.get_cookie('pixels-session')
    # print(cookies)
    # for cook in cookies:
    #     print(cook['name'])
    pass

    # pd= PixelsDriver()
    # print(pd.HUD.get_energy())
    # print(pd.HUD.get_gold())

    # pd.Trade.add_gold(10)
    # print(pd.Trade.get_other_player_name())
    # print(pd.Trade.get_other_trade_value())
    # pd.Trade.agree_trade()
    # pd.Items.get_items()
    # pd.Trade.trade_item('energydrink.png',5)
    # pd.Items.travel_bookmark(1629)
    # chrome.buy('egg',10000,40)
    # print(chrome.get_item_count(POPBERRY_SEED))
    # print(chrome.get_item_count(BUTTERBERRY_SEED))
    # print(chrome.get_item_count('shears.png'))
    # get_items(driver)
    # energy = get_energy(driver)
    # # print(energy)
    # gold = get_gold(driver)
    # print(gold)
    # sell(driver,'seltsam egg',2)
    # buy(driver,'ironite',12,10)
    # travel_bookmark(driver)












# market_input = driver.find_element(By.XPATH,"//input[contains(@class, 'Marketplace_filter')]")
# market_input.send_keys('pop')

# button = driver.find_element(By.XPATH,"//div[contains(@class, 'Marketplace_items')]").find_element(
#     By.CSS_SELECTOR,"div:nth-child(8)").find_element(By.TAG_NAME,'button')

# actions = ActionChains(driver)
# actions.send_keys(Keys.ESCAPE).perform()


    # land_1019_soils=[
    #     "65fbddf4b09ef5a41193f550","65fbddf9b09ef5a41193f63c","65fbddf7b09ef5a41193f5d2","65fbddfab09ef5a41193f65c",
    #     # "65fbddfcb09ef5a41193f6af","65fbde01b09ef5a41193f812","65fbde01b09ef5a41193f7db","65fbde02b09ef5a41193f82c",
    #     # "65fbde03b09ef5a41193f86c","65fbddfdb09ef5a41193f6e7","65fbde05b09ef5a41193f8ce","65fbde03b09ef5a41193f88c",
    #     # "65fbde07b09ef5a41193f934","65fbde06b09ef5a41193f909","65fbde08b09ef5a41193f9a7","65fbde08b09ef5a41193f966",
    #     # "65fbde0ab09ef5a41193f9e2","65fbde0eb09ef5a41193fa84","65fbde0fb09ef5a41193faa9","65fbde10b09ef5a41193fad2",
    #     # "65fbde0cb09ef5a41193fa24","65fbde0cb09ef5a41193fa3f","65fbde0db09ef5a41193fa5b","65fbde09b09ef5a41193f9bd",
    #     # "65fbde11b09ef5a41193fb0d","65fbde12b09ef5a41193fb3b","65fbde16b09ef5a41193fc7e","65fbde15b09ef5a41193fbf5",
    #     # "65fbde13b09ef5a41193fb7d","65fbde15b09ef5a41193fc26","65fbde1bb09ef5a41193fd46","65fbde1cb09ef5a41193fd8f",
    #     # "65fbde19b09ef5a41193fcf7","65fbde1cb09ef5a41193fdca","65fbde1ab09ef5a41193fd23","65fbde18b09ef5a41193fcd7",
    #     # "65fbde1fb09ef5a41193fe2d","65fbde21b09ef5a41193fe60","65fbde1eb09ef5a41193fe05","65fbde1fb09ef5a41193fe25",
    #     # "65fbde33b09ef5a4119402fe","65fbde24b09ef5a41193fee1","65fbde32b09ef5a4119402c2","65fbde23b09ef5a41193fe9b",
    #     # "65fbde31b09ef5a4119402a1","65fbde34b09ef5a411940322","65fbde35b09ef5a41194035a","65fbde35b09ef5a411940366",
    #     # "65fbde3bb09ef5a41194049f","65fbde3cb09ef5a4119404c2","65fbde3db09ef5a4119404f4","65fbde3db09ef5a4119404d3",
    #     # "65fbde40b09ef5a411940559","65fbde3eb09ef5a41194051a","65fbde3fb09ef5a41194053d", "65fbde41b09ef5a411940595",
    #     # "65fbde40b09ef5a411940573", "65fbde46b09ef5a41194068a","65fbde47b09ef5a4119406ad","65fbde47b09ef5a4119406be"
    # ]
    # shearC=[
    #     13, 162, 117, 105, 132, 162, 105, 100, 170, 105, 116, 109, 95, 115, 104, 101, 
    #     97, 114, 115, 164, 116, 121, 112, 101, 166, 101, 110, 116, 105, 116, 121, 164, 
    #     115, 108, 111, 116, 1, 163, 109, 105, 100, 184 ]
    # waterC=[
    #     13, 162, 117, 105, 222, 0, 3, 162, 105, 100, 180, 105, 116, 109, 95, 114, 117,
    #     115, 116, 121, 87, 97, 116, 101, 114, 105, 110, 103, 67, 97, 110, 164, 116,121,
    #     112, 101, 166, 101, 110, 116, 105, 116, 121, 163, 109, 105, 100, 184 ]
    # plant_C=[
    #     13, 162, 117, 105, 132, 162, 105, 100, 177, 105, 116, 109, 95, 112, 111, 112,
    #     98, 101, 114, 114, 121, 83, 101, 101, 100, 115, 164, 116, 121, 112, 101, 166,
    #     101, 110, 116, 105, 116, 121, 164, 115, 108, 111, 116, 1, 163, 109, 105, 100,
    #     184, ]