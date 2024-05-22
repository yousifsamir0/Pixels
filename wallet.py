import vision as v
import Player
import time


def read_lines_from_file(filepath,print=False):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            # Remove newline characters from each line
            lines = [line.strip() for line in lines]
            if print:
                for i in lines:
                    print(i)
            return lines
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    


IMPORT_PK = 'images/import_pk.png'

def load_wallets_form_file(filePath):
    vo = v.Vision()
    addresses = read_lines_from_file(filePath,True)
    
    ronin_wallet,found=vo.wait_till_object_found(v.RONIN_WALLET,0.9)
    vo.click_on(ronin_wallet)

    ronin_accounts,found=vo.wait_till_object_found(v.RONIN_ACCOUNTS,0.8,True)
    vo.click_on(ronin_accounts)
    time.sleep(0.1)

    for w_address in addresses:
        import_pk,found=vo.wait_till_object_found(IMPORT_PK,0.8,True)
        vo.click_on(import_pk)
        time.sleep(0.1)
        vo.press('tab')
        time.sleep(0.1)
        vo.write(w_address,0.01)
        time.sleep(0.1)
        vo.press('tab')
        time.sleep(0.1)
        vo.press('tab')
        time.sleep(0.1)
        vo.press('enter')
        time.sleep(0.2)




if __name__=='__main__':
    load_wallets_form_file('privates.txt')


    

