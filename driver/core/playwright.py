import time
from playwright.sync_api import sync_playwright
import threading
from .parser import WebSocketParser 







class PlayWrite(threading.Thread):
    def __init__(self,):
        super().__init__(daemon=True)
        self.mapId:str=None
        self.intercepting:bool = False
        self.request_intercept:callable = None
        self.page=None
        self._isStarted=False
        self.start()
        while(not self._isStarted):time.sleep(0.1)
    def run(self):
        self.browser= sync_playwright().start().chromium.connect_over_cdp("http://127.0.0.1:8989")
        default_context = self.browser.contexts[0]
        self.page = default_context.pages[0]
        self.enableIntercept()
        self.enableWsMonitor()
        self._isStarted = True
        print('playwright instance created')
        while True:
            self.page.wait_for_timeout(1000)
     
    def enableWsMonitor(self):
        self.page.on("websocket", self.on_web_socket)
    def enableIntercept(self): 
        self.page.route("**/*",self.interceptor)
    def startIntercept(self,mapId:str):
        self.mapId = str(mapId)
        self.intercepting=True
    def stopIntercept(self):
        self.intercepting=False
        self.mapId=''
    def get_new_ids(self):
        ids= self.newSoilIds
        self.newSoilIds = []
        return ids


    def interceptor(self,route):
        if self.intercepting:
            url = route.request.url
            if ('pixels-server' in url):
                print(url)
                url=url.replace('terravilla',self.mapId)
                print(url)
            route.continue_(url=url)
        else:
            route.continue_()


    def on_web_socket(self,ws):
        def on_frame_received(payload:bytes):
            WebSocketParser.parseFrame(payload)
        print(f"WebSocket opened: {ws.url}")
        # ws.on("framesent", frame_sent)
        ws.on("framereceived", on_frame_received)
        ws.on("close", WebSocketParser.reset)


def frame_sent(payload:bytes):
    # if b'clickEntity' in payload:
    print(payload)




# class PlayWrite(threading.Thread):
#     def __init__(self,):
#         self.browser= sync_playwright().start().chromium.connect_over_cdp("http://127.0.0.1:8989")
#         default_context = self.browser.contexts[0]
#         self.page = default_context.pages[0]
#         self.mapId:str=None
#         self.intercepting:bool = False
#         self.request_intercept:callable = None
#         # self.page.route("", self.interceptor)
#         # self.page.wait_for_timeout(5000)


#     def enableIntercept(self,mapId:str):
#         self.mapId=mapId
#         self.page.route("**/*",self.interceptor)
        

#     def disableIntercept(self,url):
#         self.page.unroute("**/*")

#     def interceptor(self,route):
#             url = route.request.url
#             print(url)
#             if ('pixels-server' in url):
#                 url=url.replace('terravilla',self.mapId)
#             print(url)
#             route.continue_(url=url)            