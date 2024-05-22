import time
from selenium.webdriver.common.keys import Keys
from .pixels_base import PixelsBase


class Market(PixelsBase):
    

    def sell(self,itemName,price):
        try:
            create_btn =self.driver.find_element_by_xpath("//*[contains(@class, 'Infiniportal_tabButtonsContainer')]//button[2]")
            create_btn.click()
            listings =self.driver.find_elements_by_xpath("//*[contains(@class, 'MarketplaceListings_listing_')]")
            for item in listings:
                item_data = item.text.split('\n')
                item_name = item_data[0]
                item_quantity = item_data[1]
                if itemName.lower() == item_name.lower():
                    self.driver.find_element_by_xpath('.//button',item).click()
                    self.driver.find_elements_by_xpath('//input[1]')[0].clear()
                    self.driver.find_elements_by_xpath('//input[1]')[0].send_keys(int(price))
                    self.driver.find_elements_by_xpath('//input[1]')[1].clear()
                    self.driver.find_elements_by_xpath('//input[1]')[1].send_keys(int(item_quantity))
                    self.driver.find_element_by_xpath('//button[contains(@class,"MarketplaceAddListing_button")]').click()
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
        print('amount to buy:',localCount)
        view_listing_btn=None
        input =self.driver.find_element_by_xpath("//input[1]")
        input.clear()
        input.send_keys(itemName.lower())
        time.sleep(1)
        listings =self.driver.find_elements_by_xpath("//*[contains(@class, 'Marketplace_item_')]")
        for item in listings:
            # print(item.text)
            item_data = item.text.split('\n')
            print(item_data)
            item_name = item_data[0]
            if itemName.lower() == item_name.lower():
                print('found')
                view_listing_btn=self.driver.find_element_by_xpath('.//button',item)
        current_g = self.get_gold()
        buyCooldown=False
        while(localCount!=0):
            if buyCooldown:
                time.sleep(2.5)
                buyCooldown = False
            # for i in range(10):
            view_listing_btn.click()
            listing = self.driver.wait_till_element_clickable('//*[contains(@class, "MarketplaceItemListings_buyListing")]',20)
            print(listing.text)
            listing_data = listing.text.split('@')
            listing_price = int(listing_data[-1].strip().replace(',',''))
            listing_count = int(listing_data[-2].split(':')[-1].strip().replace(',',''))
            print('price: is {} and count is {}'.format(listing_price,listing_count))
            if listing_price>maxPrice:
                x_btn =self.driver.find_elements_by_xpath("//*[contains(@class, 'commons_modalBackdrop')]//button[contains(@class,'commons_closeBtn')]")[1]
                x_btn.click()
                continue
            buy_count = min(localCount,listing_count)
            listing.click()

            price_input =self.driver.wait_till_element_clickable("//*[contains(@class, 'MarketplaceItemListings_amount')]//input")
            price_input.clear()
            price_input.send_keys(buy_count)

            buy_button =self.driver.wait_till_element_clickable("//*[contains(@class, 'MarketplaceItemListings_buyListing')]")
            buy_button.click()

            notification = self.driver.wait_till_element_clickable('//*[contains(@class, "Notifications_text_")]')
            print(notification.text)
            self.driver.force_click_element(notification)

            if '+' in notification.text:
                print(current_g)
                print(self.get_gold())
                current_g = self.get_gold()
                localCount -= buy_count
                buyCooldown = True
                closeBuy_btn=self.driver.wait_till_element_clickable('//*[contains(@class, "Marketplace_buyContent")]//button[1]')
                closeBuy_btn.click()
                time.sleep(0.5)
            x_btn = self.driver.wait_till_element_clickable('//*[contains(@class,"MarketplaceItemListings_container_")]//button[1]')
            x_btn.click()
    def buy_from_store(self,itemName,amount):
        try:
            search_input = self.driver.find_element_by_xpath('//input[contains(@class,"Store_filter_")]')
            search_input.clear()
            search_input.send_keys(itemName)
            time.sleep(0.2)
            item_card = self.driver.find_element_by_xpath('//div[contains(@class,"Store_card-content_")]')
            item_card.click()
            time.sleep(0.1)
            quantity_input = self.driver.find_element_by_xpath('//input[contains(@class,"Store_quantity-input_")]')
            quantity_input.clear()
            quantity_input.send_keys(str(amount))
            buy_btn = self.driver.find_element_by_xpath('//button[contains(@class,"Store_buy-btn_")]')
            buy_btn.click()
            time.sleep(0.3)
            self.driver.send_keys(Keys.ESCAPE)
            return True
        except Exception as e:
            print(f'[buy from Store]: {e}')
            return False
    def collect_mail_box(self):
        try:
            mail_badge = self.driver.find_elements_by_xpath('//button[contains(@class,"Hud_mailbox_")]/span')
            if mail_badge:
                # mail_box = self.driver.find_element_by_xpath('//div[contains(@class,"Hud_mailbox_")]')
                mail_badge[0].click()
                time.sleep(0.5)
                collect_all_btn = self.driver.find_element_by_xpath('//button[contains(@class,"MailBox_collectAllButton")]')
                collect_all_btn.click()
                time.sleep(0.2)
                close_btn = self.driver.find_element_by_xpath('//button[contains(@class,"closeBtn_")]')
                close_btn.click()
                return True
            print('[collectMail] no mails to collect !')
        except Exception as e:
            print(f'[mailBox] {e}')
            self.driver.send_keys(Keys.ESCAPE)
            return False
