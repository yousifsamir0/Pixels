import time
from .chrome_driver import Driver
from selenium.webdriver.common.keys import Keys
from .utils import save_cookies,load_cookies


class PixelsBase:
    _instance = None
    def __init__(self):
        self.driver = Driver()
        self.pw = self.driver.pw
    def __new__(cls,*args, **kwargs) :
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def get_energy(self):
        energyEl =self.driver.find_element_by_xpath("//*[contains(@class, 'Hud_energytext')]")
        if energyEl:
            return float(energyEl.text.strip().replace(',',''))
        else:
            print('[log:get_energy]:: could not find energy')
            return -1
        
    def get_gold(self):              
        goldElement =self.driver.find_element_by_xpath('//*[contains(@class,"commons_coinBalance_")]')
        if goldElement:
            return int(goldElement.text.strip().replace(',', ''))
        else:
            print('[log:get_gold]:: could not find gold')
            return -1
        
    def open_land(self):
        openLand_btn =self.driver.find_element_by_xpath("//*[contains(@class, 'Hud_topLeftBackground')]//button[1]")
        if openLand_btn:
            openLand_btn.click()
            return True
        else:
            print('[open_land]:: could not find landbtn')
            return False
    def wait_for_travel(self,timeout=30):
        def getopacity(): return self.driver.find_element_by_xpath("//*[contains(@class, 'gameCover')]").get_attribute('style')
        t = time.time()
        while('1' not in getopacity() ): 
            time.sleep(0.01)
            if((time.time()-t)>=timeout):break
        t = time.time()
        while('0' not in getopacity() ): 
            time.sleep(0.01)
            if((time.time()-t)>=timeout):break
        time.sleep(1)
        
    def set_travel_to_land(self):
        pass

    def travel_bookmark(self,landNumber:int|float|str='tv'):
        mapId=str(landNumber)
        if type(landNumber) == int or type(landNumber) == float:
            mapId = 'pixelsNFTFarm-'+ mapId
        opened=self.open_land()
        if not opened: return False
        travilla_btn =self.driver.wait_till_element_clickable("//*[contains(text(), 'Go to Terravilla')]")
        if not travilla_btn: print('[travel]: could not find travilla_btn'); return False
        if str(landNumber) != 'tv':
            self.pw.startIntercept(landNumber)
        travilla_btn.click()
        self.wait_for_travel()
        if str(landNumber) != 'tv':
            self.pw.stopIntercept()
        print(f'[travel] Travel to land {landNumber} complete')
        return True
           
    def remove_bookmarks(self,landsNumberList=[],removeAll=False):
        opened=self.open_land()
        if not opened: return False
        bookmark_btn =self.driver.find_element_by_xpath("//*[contains(@class, 'LandAndTravel_tabs')]//button[3]")
        if not bookmark_btn: print('[delete_bookmarks]: could not find bookmark_btn'); return False
        bookmark_btn.click()
        bookmarks =self.driver.find_elements_by_xpath("//*[contains(@class, 'LandAndTravel_mapSquare_')]")
        if not bookmarks: print('[travel]: could not find bookmarks'); return False
        for bookmark in bookmarks:
            number = int( bookmark.text.replace('✖','').replace('GO','').replace('#','').strip())
            if (number in landsNumberList) or removeAll:
                print('land found and deleted =',number)
                print(bookmark.text)
                remove_btn=self.driver.find_element_by_xpath(".//button[contains(@class,'removeBookmarkButton')]",bookmark)
                if not remove_btn: print('[travel]: could not find GO_btn'); return False
                remove_btn.click()
        self.driver.send_keys(Keys.ESCAPE)
    def cookis_login(self,accountNumber,worldNum):
        cookie = load_cookies(accountNumber)
        driver =self.driver.driver
        driver.delete_all_cookies()
        driver.add_cookie(cookie)
        driver.refresh()
        worldSelection = self.driver.wait_till_element_clickable('//*[contains(@class,"Intro_smalllink_")]',60)
        time.sleep(0.1)
        worldSelection.click()
        time.sleep(0.1)
        scroller= self.driver.wait_till_element_clickable('//*[contains(@class,"Intro_worldScroller")]',60)
        world= self.driver.wait_till_element_clickable(f'//div[contains(text(),"{worldNum}")]',60)
        print(world.text)
        self.driver.scroll_to_element(scroller,world)
        time.sleep(0.1)
        world.click()
    def cookies_logout(self):
        self.driver.driver.delete_all_cookies()
        self.driver.driver.refresh()
        time.sleep(1)
    def logout(self): 
        logout_btn=self.driver.find_element_by_xpath(".//div[contains(@class,'ud_topRightBackground_')]//button[6]")
        if (logout_btn):
            logout_btn.click()
            time.sleep(0.1)