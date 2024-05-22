from .pixels_base import PixelsBase
from selenium.webdriver.common.keys import Keys
from utils import compare_blob_image_with_disk
import time


class Items(PixelsBase):
    def get_item_element(self,slotNumber):
        itemEl = self.driver.wait_till_element_clickable(f"//*[contains(@class, 'itemList_')]/div[{slotNumber}]")
        return itemEl
    
    def is_slot_empty(self,slotNumber):
        itemEl = self.get_item_element(slotNumber)
        if self.driver.find_element_by_xpath("./div[contains(@class, 'clickable')]",itemEl):
            return False
        return True
    
    def get_items(self):
        # actions = ActionChains(self.driver)
        while(True):
            time.sleep(0.2)
            items=self.driver.find_elements_by_xpath("//div[contains(@class, 'Hud_item_')]")
            # print(len(items))
            item1 = self.driver.find_element_by_xpath("./div[contains(@class, 'Hud_shortcut_')]",items[0])
            item_shortcut = int(item1.get_attribute('textContent').strip())
            if item_shortcut == 1:
                return items
            self.driver.send_keys(Keys.TAB)
        
    def get_item_count(self,item_blob):
        items=self.driver.find_elements_by_xpath("//img[contains(@class,'Hud_itemImage')]")
        count=0
        for item in items:
            if compare_blob_image_with_disk(self.driver,item.get_attribute('src'),item_blob):
                quatity = self.driver.find_element_by_xpath('../..//div[contains(@class, "Hud_quantity_")]',item).get_attribute('textContent').split('x')[-1].strip()
                count += 1 if quatity=='' else int(quatity)
        return count
    def item_get_slot(self,item_blob)-> int:
        items=self.driver.find_elements_by_xpath("//div[contains(@class, 'Hud_item_')]//img")
        for item in items:
            if compare_blob_image_with_disk(self.driver,item.get_attribute('src'),item_blob):
                slot_number = self.driver.find_element_by_xpath('../..//div[contains(@class, "Hud_shortcut_")]',item).get_attribute('textContent').strip()
                return int(slot_number)
    def expand_items_if_not(self):
        itemGroup = self.driver.wait_till_element_clickable("//div[contains(@class, 'Hud_slidingGroup')]")
        if 'expanded' not in itemGroup.get_attribute('class'):  
            self.driver.send_keys('b')
            time.sleep(1)

    def shrink_items_if_not(self):
        itemGroup = self.driver.wait_till_element_clickable("//div[contains(@class, 'Hud_slidingGroup')]")
        if 'expanded' in itemGroup.get_attribute('class'):  
            self.driver.send_keys('b')
            time.sleep(1)

    def swap_slots(self,oldSlot,newSlot):
        self.expand_items_if_not()
        self.driver.send_keys(Keys.ESCAPE)
        items = self.get_items()
        items[oldSlot-1].click()
        time.sleep(0.15)
        items[newSlot-1].click()
        self.driver.send_keys(Keys.ESCAPE)

    def put_item_in_slot(self,item_blob,slotNumber):
        oldSlot = self.item_get_slot(item_blob)
        if oldSlot == slotNumber:return
        self.swap_slots(oldSlot,slotNumber)

    def is_slot_selected(self,slotNumber):
        # t =time.time()
        item = self.driver.wait_till_element_clickable(f"//div[text()='{slotNumber}']/..")
        # print(time.time()-t)
        # print(item.get_attribute("class"))
        if 'selected' in item.get_attribute('class'):
            return True
        return False
    
    def sort_items(self,items):
        self.get_items() # sorting purpose
        for i in range(len(items)):
            self.put_item_in_slot(items[i],i+1)
            time.sleep(0.1)
        self.shrink_items_if_not()
        # c.put_item_in_slot('water.png',2)
        # time.sleep(0.1)
        # c.put_item_in_slot(seed,3)
        # time.sleep(0.1)
        # c.put_item_in_slot('energydrink.png',4)
        # c.actions.send_keys('b').perform()
    
    