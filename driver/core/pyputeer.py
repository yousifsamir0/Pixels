import asyncio
import json
from pyppeteer import connect
from pyppeteer.network_manager import Request



class pyppeteer_sync:
    def __init__(self,) -> None:
        self.page=None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.init())
        print('pyppteer instance created')

    def sync_send_ws_message(self,data,interval=0.12):
        self.loop.run_until_complete(self.send_ws_message(data,interval=interval))

    async def init(self) -> None:
        browser = await connect({'browserURL':'http://127.0.0.1:8989','defaultViewport':None})
        pages = await browser.pages()
        self.page = pages[0]
    async def send_ws_message(self,data,interval):
        data_js=f"JSON.parse('{json.dumps(data)}')"
        dataHandle = await self.page.evaluateHandle(data_js)
        prototype = await self.page.evaluateHandle("WebSocket.prototype")
        socketInstances_handle = await self.page.queryObjects(prototype)
        await self.page.evaluate(f'''async (instances,data) => {{
        instance = instances.find((sock)=>sock.readyState===1)
        for (let i =0; i< data.length;++i)
        {{
            instance.send(new Uint8Array(data[i]).buffer)
            await new Promise((resolve) => setTimeout(resolve, {interval} * 1000));
        }}
        }}''', socketInstances_handle,dataHandle)
        return



# import time
# p = pyppeteer_sync()
# p.sync_start_intercept()

# p.sync_send_ws_message(L1019_plant_commands)
# print('start waiting')
# time.sleep(200)
# time.sleep(1)
# p.sync_send_ws_message(L1019_water_commands)
# time.sleep(60)
# p.sync_send_ws_message(L1019_shear_commands)


