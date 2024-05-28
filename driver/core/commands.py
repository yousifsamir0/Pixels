from .parser import WebSocketParser as wsP


def plant_command(plantCount,seed_name:str):
    realCount=min(len(wsP.ent_soil),plantCount)
    soil_ids=wsP.ent_soil[:realCount]
    plant_C= b'\r\xa2ui\x84\xa2id\xb1itm_'+seed_name.encode()+b'\xa4type\xa6entity\xa4slot\x01\xa3mid\xb8'
    commands_list = [list(plant_C+soil_id.encode()) for soil_id in soil_ids[:]]
    return commands_list
def water_command():
    soil_ids=wsP.ent_crops
    print("water wsP.ent_crops:\n",soil_ids)
    waterC=b'\r\xa2ui\xde\x00\x03\xa2id\xb4itm_rustyWateringCan\xa4type\xa6entity\xa3mid\xb8'
    commands_list = [list(waterC+soil_id.encode()) for soil_id in soil_ids[:]]
    return commands_list

def shear_command():
    soil_ids=wsP.ent_crops
    print("shearing wsP.ent_crops:\n",soil_ids)
    shearC = b'\r\xa2ui\x84\xa2id\xaaitm_shears\xa4type\xa6entity\xa4slot\x01\xa3mid\xb8'
    commands_list = [list(shearC+soil_id.encode()) for soil_id in soil_ids[:]]
    return commands_list

def collect_wood_command():
    wood_ids=wsP.ent_woods
    print("collecting woods:\n",wood_ids)
    precollectC = b'\r\xabclickEntity\x84\xa3mid\xb8'
    postcollectC = b'\xa6entity\xa8ent_wood\xa6impact\xa5click\xa6inputs\x92\xcd\n\xd8\xcb@\xafW\x00\x00\x00\x00\x00'
    commands_list = [list(precollectC+wood_id.encode()+postcollectC) for wood_id in wood_ids[:]]
    return commands_list
def cut_trees_command():
    trees_ids=wsP.ent_trees
    print("cutting trees:\n",trees_ids)
    cutC = b'\r\xa2ui\x84\xa2id\xa7itm_axe\xa4type\xa6entity\xa4slot\x03\xa3mid\xb8'
    commands_list = [list(cutC+trees_ids.encode()) for trees_ids in trees_ids[:]]
    
    return (commands_list*6)

def buy_from_hazel_command(itemName:str,quantity:int):
    quantity_binary = b'\xcc'+quantity.to_bytes() if (quantity<256 )  else b'\xcd'+quantity.to_bytes(2)
    itemName_binary = (0xa4 +len(itemName)).to_bytes() + b'itm_' +itemName.encode()
    buyC = b'\r\xacbuyStoreItem\x83\xa7storeId\xafstr_bucksGalore\xa6itemId'+itemName_binary+b'\xa8quantity'+quantity_binary
    return [list(buyC)]

def sell_items_command(itemName:str,quantity:int,pricePerOne:int):
    quantity_binary = b'\xcc'+quantity.to_bytes() if (quantity<256 )  else b'\xcd'+quantity.to_bytes(2)
    price_binary =    b'\xcc'+pricePerOne.to_bytes() if (pricePerOne<256 )  else b'\xcd'+pricePerOne.to_bytes(2)
    itemName_binary = (0xa4 +len(itemName)).to_bytes() + b'itm_' +itemName.encode()
    sellC=b'\r\xabmarketplace\x85\xaasubcommand\xa6create\xa6itemId'+itemName_binary+b'\xa8quantity'+quantity_binary+b'\xa5price'+price_binary+b'\xa8currency\xa9cur_coins'
    return [list(sellC)]
def use_item_on_self_command(itemName:str,count:int=1):
    itemName_binary = (0xa4 +len(itemName)).to_bytes() + b'itm_' +itemName.encode()
    command = b'\r\xa2ui\x83\xa2id' + itemName_binary + b'\xa4type\xa4self\xa4slot\x00'
    return [list(command)]*count