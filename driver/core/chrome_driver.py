import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .playwright import PlayWrite
# from .pyputeer import pyppeteer_sync

# from seleniumwire import webdriver , undetected_chromedriver,request



class Driver():
    _instance = None
    _init = False
    def __init__(self) -> None:
        if not self.__class__._init:
            c_options = Options()
            c_options.add_experimental_option("debuggerAddress", "localhost:8989")
            self.driver = webdriver.Chrome(options=c_options)
            # self.driver = webdriver.Chrome(options=c_options,seleniumwire_options={'port':8080})
            self.actions = ActionChains(self.driver)
            self.pw = PlayWrite()
            print('created Driver Instance')
            self.__class__._init = True
    def __new__(cls,*args, **kwargs) :
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def intercept_init(self):

        def interceptor(request):
            if '/v1/map/' in request.url or '/game/findroom/' in request.url:
                print(request)


            # if 'pixels-server.pixels.xyz'in request.url:
        self.driver.request_interceptor=interceptor

    def find_element_by_xpath(self,xpath:str,element:WebElement=None,timeout:float=0.1,interval:float=0.01):
        d = self.driver if not element else element
        t=time.time()
        while(time.time()-t <= timeout):
            try:
                if not len(xpath): print('[driver_FEBC]: Empty xpath given');return None
                ret_element = d.find_element(By.XPATH,xpath)
                return ret_element
            except Exception as e:
                if time.time()-t > timeout:
                    print('[driver_FEBX]: No elements found !\n',e)
                    return None
            time.sleep(interval)
    
    def find_elements_by_xpath(self,xpath:str,element:WebElement=None,timeout:float=0.1,interval:float=0.01):
        d = self.driver if not element else element
        t = time.time()
        while (time.time()-t <= timeout):
            if not len(xpath): print('[driver_FEBCs]: Empty xpath given');return None
            elements = d.find_elements(By.XPATH,xpath)
            if len(elements):
                return elements
            time.sleep(interval)
        print('[[driver_FEBCs]: timeout no elements found !]')
        return []
                


    def wait_till_element_clickable(self,xpath,timeout=30):
        try:
            if not len(xpath): print('[driver_WEC]: Empty xpath given');return None
            element= WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH,xpath)))
            return element
        except:
            print(f'[driver_WEC]: Timeout waiting {xpath}')
            return None
        
    def scroll_to_element(self, scrollable_element, target_element):
        """Scroll to a target element inside a scrollable element."""
        # Move to the scrollable element
        target_y = target_element.location['y'] - scrollable_element.location['y']
        self.driver.execute_script("arguments[0].scrollTop = arguments[1];", scrollable_element, target_y)

    def send_keys(self,*keys_to_send: str):
        self.actions.send_keys(*keys_to_send).perform()
        
    def force_click_element(self,element):
        self.driver.execute_script("arguments[0].click();", element)
        return
    def evaluate_handle(self,pageFunction:str):
        obj= self.driver.execute_cdp_cmd('Runtime.evaluate', {
                    'expression': pageFunction,
                    'returnByValue': False,
                    'awaitPromise': True,
                    'userGesture': True,
                })
        if obj.get('result'):
            return obj.get('result').get('objectId')
        else:
            print('Runtime.Exception in evaluate_handle')
    def queryObjects(self,objectPrototypeId):
        try:
            obj = self.driver.execute_cdp_cmd('Runtime.queryObjects', {
                'prototypeObjectId': objectPrototypeId,
            }).get('objects').get('objectId')
            return obj
        except Exception as e:
            print(e)
    def execute_func_on(self,pageFunctionImp:str,*args):
        self.driver.execute_cdp_cmd('Runtime.callFunctionOn', {
            'functionDeclaration': f'{pageFunctionImp}\n',
            'objectId':args[0],
            'arguments':[{'objectId':arg} for arg in args ],
            'returnByValue': False,
            'awaitPromise': True,
            'userGesture': True,
        })
    def sendWS(self,data,interval=0.12):
        data_js=f"JSON.parse('{json.dumps(data)}')"
        data = self.evaluate_handle(data_js)
        wsProto=self.evaluate_handle('WebSocket.prototype')
        instances = self.queryObjects(wsProto)
        fn = f'''async (instances,data) => {{
        instance = instances.find((sock)=>sock.readyState===1)
        for (let i =0; i< data.length;++i)
        {{
            instance.send(new Uint8Array(data[i]).buffer)
            await new Promise((resolve) => setTimeout(resolve, {interval} * 1000));
        }}
        }}'''
        self.execute_func_on(fn,instances,data)

    
