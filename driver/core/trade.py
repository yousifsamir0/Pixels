import math
import time
from .pixels_base import PixelsBase
from selenium.webdriver.common.keys import Keys
from .items import Items

class Trade(PixelsBase):
    it = Items() 
    def press_trade_btn(self):
        trade_btn =self.driver.find_element_by_xpath('//button[contains(text(),"Trade")]')
        trade_btn.click()
    def get_other_player_name(self):
        otherPlayerEl = self.driver.find_element_by_xpath('//*[contains(@class,"otherPlayerWrapper")]//div[contains(@class,"username")]')
        return otherPlayerEl.text.strip()
    def get_self_player_name(self):
        selfPlayerEl = self.driver.find_element_by_xpath('//*[contains(@class,"selfPlayerWrapper")]//div[contains(@class,"username")]')
        return selfPlayerEl.text.strip()
    def get_other_trade_value(self):
        otherPlayerEl = self.driver.find_element_by_xpath('//*[contains(@class,"otherPlayerWrapper")]//div[contains(@class,"tradevalue")]')
        return int(otherPlayerEl.text.split('\n')[-1].strip().replace(',',''))
    def get_self_trade_value(self):
        selfPlayerEl = self.driver.find_element_by_xpath('//*[contains(@class,"selfPlayerWrapper")]//div[contains(@class,"tradevalue")]')
        return int(selfPlayerEl.text.split('\n')[-1].strip().replace(',',''))
    def accept_trade(self,username):
        notificaion = self.driver.wait_till_element_clickable('//*[contains(@class,"Notifications_text_")]')
        if 'wants to trade. Accept?' in notificaion.text:
            _username = notificaion.text.split(' ')[0].strip()
            if _username == username:
                yes_btn = self.driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
                yes_btn.click()
                return True
            else: print('[AT]: username not match'); return False
        else:print('[AT]: no trade found'); return False
    def add_gold(self,gold_amount):
        gold_input = self.driver.find_element_by_xpath('//*[contains(@class,"selfPlayerWrapper")]//input')
        gold_input.clear()
        gold_input.send_keys(str(gold_amount))
        time.sleep(0.1)
        gold_input.send_keys(Keys.ENTER)

    def confirm_agree_trade(self):
        agree_btn = self.driver.wait_till_element_clickable('//button[text()="Yes"]')
        agree_btn.click()

    def agree_trade(self):
        agree_btn = self.driver.find_element_by_xpath('//button[text()="Agree"]')
        agree_btn.click()

    def get_trade_slot_element(self,slot_num):
        slots = self.driver.find_elements_by_xpath('//*[contains(@class,"selfPlayerWrapper")]//div[contains(@class,"tradeSlotWrapper_")]')
        return slots[slot_num-1]
    def trade_item(self,item_blob,amount):
        self.it.get_items() #for sort only
        item_slot = self.it.item_get_slot(item_blob)
        print(item_slot)
        switches_nr = math.ceil(item_slot/6)-1
        print(switches_nr)
        for i in range(switches_nr):
            self.driver.send_keys(Keys.TAB)
            time.sleep(0.4)
            
        shortcut_nr = item_slot-(switches_nr*6)
        self.driver.send_keys(str(shortcut_nr))
        trade_slotEL = self.get_trade_slot_element(1)
        trade_slotEL.click()
        time.sleep(0.2)
        # quantity_input = self.driver.find_element_by_xpath(,trade_slotEL)
        quantity_input = self.driver.wait_till_element_clickable('//*[contains(@class,"InventoryWindow_tradeQuantity")]')
        quantity_input.clear()
        quantity_input.send_keys(str(amount))
        time.sleep(0.1)
        quantity_input.send_keys(Keys.ENTER)
            

    


if __name__ == '__main__':
    o = Trade()
    o.add_gold(200)