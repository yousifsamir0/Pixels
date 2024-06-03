import re





class WebSocketParser():
    ent_soil=[]
    ent_crops=[]
    ent_woods=[]
    ent_trees=[]
    @classmethod
    def parseFrame(cls,payload):
        if  (payload[0]==0x0e):  #mapData
            cls.parse_map_data(payload)
            pass
        elif (payload[0]==0x11): #updatePlayer frame
            cls.parse_updatePlayer_frame(payload)
            pass

        elif (payload[2:10] == b'joinRoom'): #joinRoom frame
            cls.parse_joinRoom_frame(payload)
            pass

    @classmethod
    def parse_map_data(cls,payload:bytes):
        pattern = b'([0-9a-f]{24}).{1,10}?[0-9a-f]{24}\x84\xa8ent_soil'
        regex = re.compile(pattern,re.DOTALL)
        # Find all matches
        matches:list[bytes] = regex.findall(payload)
        # Extract IDs from matches
        # print([match  for match in matches])
        # print(payload)
        # print(matches)
        # print(len(matches))
        cls.ent_soil= [match.decode() for match in matches]
        # print(cls.ent_soil)

    @classmethod
    def parse_updatePlayer_frame(cls,payload:bytes):
        pattern = b'\xb8[^\xb8]*\xb8[^\xb8]*' + b'ent_crop'
        regex = re.compile(pattern)
        # Find all matches
        matches:list[bytes] = regex.findall(payload)
        # Extract IDs from matches
        for match in matches:
            if match[1:25].decode() not in cls.ent_crops:
                cls.ent_crops.append(match[1:25].decode())
        #----------wood
        pattern = b'\xb8[0-9a-fA-F]{24}[^\xb8]*' + b'ent_wood\x86'
        regex = re.compile(pattern)
        # Find all matches
        matches:list[bytes] = regex.findall(payload)
        # Extract IDs from matches
        for match in matches:
            if match[1:25].decode() not in cls.ent_woods:
                cls.ent_woods.append(match[1:25].decode())
        
    @classmethod
    def parse_joinRoom_frame(cls,payload:bytes):
        pattern = b'\xb8[^\xb8]*\xb8[^\xb8]*' + b'ent_crop'
        regex = re.compile(pattern)
        # Find all matches
        matches:list[bytes] = regex.findall(payload)
        # Extract IDs from matches
        ids = [match[1:25].decode() for match in matches]
        cls.ent_crops=ids
        #--------------woods
        pattern = b'\xb8[^\xb8]*' + b'ent_wood\xcc'
        regex = re.compile(pattern)
        # Find all matches
        matches:list[bytes] = regex.findall(payload)
        # Extract IDs from matches
        ids = [match[1:25].decode() for match in matches]
        cls.ent_woods=ids
        #--------------trees
        pattern = b'\xb8[^\xb8]*\xb8[^\xb8]*' + b'ent_playerTree'
        regex = re.compile(pattern)
        # Find all matches
        matches:list[bytes] = regex.findall(payload)
        # Extract IDs from matches
        ids = [match[1:25].decode() for match in matches]
        cls.ent_trees=ids
        #---------------Items
        # pattern = b'\xff[^\xb8]*itm_[^\xb8]*\xff'
        # regex = re.compile(pattern)
        # # Find all matches
        # matches:list[bytes] = regex.findall(payload)
        

    @classmethod
    def reset(cls):
        cls.ent_soil=[]
        cls.ent_crops=[]
        cls.ent_woods=[]
        cls.ent_trees=[]
    # b'\x86\xb86624a8af54c3ca9674cf9134\x87\xb2pixelsNFTFarm-1019\x88I\xff%\x81\xb866462e7ce0db88c393cf48ea\x82\xb865fbde07b09ef5a41193f934\x83\x00\x84\xb0ent_cropPopberry'
    # b'\x86\xb86624a8af54c3ca9674cf9134\x87\xb2pixelsNFTFarm-1019\x88H\xff$\x81\xb866462e4be0db88c393cf35ee\x82\xb865fbde06b09ef5a41193f909\x83\x00\x84\xb0ent_cropPopberry'
    # b'\x86\xb86624a8af54c3ca9674cf9134\x87\xb2pixelsNFTFarm-1019\x88G\xff#\x81\xb866462911e0db88c393cd09ed\x82\xb865fbde01b09ef5a41193f812\x83\x00\x84\xb0ent_cropPopberry'
    # b'\x86\xb86624a8af54c3ca9674cf9134\x87\xb2pixelsNFTFarm-1019\x88F\xff"\x81\xb866462837e0db88c393ccb43d\x82\xb865fbde01b09ef5a41193f7db\x83\x00\x84\xb0ent_cropPopberry'
    # b'\x86\xb86624a8af54c3ca9674cf9134\x87\xb2pixelsNFTFarm-1019\x88E\xff!\x81\xb866462803e0db88c393cc9e6c\x82\xb865fbddf7b09ef5a41193f5d2\x83\x00\x84\xb0ent_cropPopberry'
    # b'\x86\xb86624a8af54c3ca9674cf9134\x87\xb2pixelsNFTFarm-1019\x8bD\xff \x81\xb866462686e0db88c393cc0a20\x82\xb865fbddf4b09ef5a41193f550\x83\x00\x84\xb0ent_cropPopberry'