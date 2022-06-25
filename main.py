from json import load
from shutil import ExecError
import string
import requests
import os
import threading
from colorama import Fore, init
import random

init()
xlist = ["NfZQSsxxihI1aL_F5KSX-Q","Gi2ISuIbk8nHEYsIRZyriw","SYzlCnM9oe4exSX0RJuVVQ","5imbweonSha2UHjPuu2_rA","4L3PTPoPr0hXBBRKp59WlQ","eRJqOkcjww_N48CMUnCxPg","lIXpsdGqKNrOxacsZDtDMQ","BOk3wvBuVrKG-3vVScS_Mg","JxHQs1iIuQQPAEnXMjFBwA","uHDVmdsmxNxVXV6NwRDb2Q","9mN3Cjy0Sf-IHCt3qj1EKg","3MpY7xtPO6c7Zim42W36LQ","f0PMXAnw1LrEcYzvkJ1QXQ","FsGJwjbFSi9jqXIegbhU5A","qB4eCY1-w68BhQSu5XNFwg"]

__lock__ = threading.Lock()
fcl = False
ol = False
tc = 0
lc = 0
hits = 0
takens = 0
fails = 0
tries = 0
proxies = []

def loadproxies():
    r = requests.get("https://api.proxyscrape.com?request=getproxies&proxytype=http")
    rformat = r.text.strip()
    rformat = rformat.replace("\r","")
    rlist = list(rformat.split("\n"))
    with open("proxies.txt", "w") as x:
        for proxy in rlist:
            proxies.append(proxy)

def safeprint(str):
    __lock__.acquire()
    print(str)
    __lock__.release()

def check(user):
    xsrf_token = random.choice(xlist)
    global proxies
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Cookie": f"xsrf_token={xsrf_token}"
    }
    proxie = {
        'http': random.choice(proxies)
    }
    resp = requests.post(f'https://accounts.snapchat.com/accounts/get_username_suggestions?requested_username={user}&xsrf_token={xsrf_token}', headers=headers, proxies=proxie)
    try:
        if resp.json()['reference']['status_code'] == 'OK':
            return False
        elif resp.json()['reference']['status_code'] == 'TAKEN':
            return True
        else:
            pass
    except:
        return resp.text


banner = """

                    .▄▄ ·  ▐ ▄  ▄▄▄·  ▄▄▄· ▄▄·  ▄ .▄ ▄▄▄· ▄▄▄▄▄     ▄▄·  ▄ .▄▄▄▄ . ▄▄· ▄ •▄ ▄▄▄ .▄▄▄  
                    ▐█ ▀. •█▌▐█▐█ ▀█ ▐█ ▄█▐█ ▌▪██▪▐█▐█ ▀█ •██      ▐█ ▌▪██▪▐█▀▄.▀·▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·
                    ▄▀▀▀█▄▐█▐▐▌▄█▀▀█  ██▀·██ ▄▄██▀▐█▄█▀▀█  ▐█.▪    ██ ▄▄██▀▐█▐▀▀▪▄██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄ 
                    ▐█▄▪▐███▐█▌▐█ ▪▐▌▐█▪·•▐███▌██▌▐▀▐█ ▪▐▌ ▐█▌·    ▐███▌██▌▐▀▐█▄▄▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌
                    ▀▀▀▀ ▀▀ █▪ ▀  ▀ .▀   ·▀▀▀ ▀▀▀ · ▀  ▀  ▀▀▀     ·▀▀▀ ▀▀▀ · ▀▀▀ ·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀

                                                     yuxontop
                """.replace('.', Fore.RED+'.'+Fore.YELLOW).replace('▪', Fore.RED+'▪'+Fore.YELLOW).replace('·', Fore.RED+'·'+Fore.YELLOW)

def get_random_string(lenght):
    if ol == True:
        return ''.join(random.choice(string.ascii_lowercase) for i in range(lenght))
    else:
        return ''.join(random.choice(string.ascii_lowercase+str(string.digits)) for i in range(lenght))
                    

def update():
    global fails, hits, takens, tries, tc
    while True:
        os.system(f'title SnapchatUsernameChecker ^| github.com/yuxontop ^| Fails: {fails} ^| Hits: {hits} ^| Taken: {takens} ^| Tries: {tries} ^| Threads: {tc}')


def main():
    global tc, fbl, ol, lc, fip
    os.system('cls')
    print(Fore.YELLOW + banner)
    print('\n'*4)
    tc = int(input('     [>] How Much Threads You Want ? '))
    fbl = str(input('     [>] From Username List ? (Y/n) ? ')).lower()
    if fbl == 'y':
        fbl = True
        fip = str(input('     [>] Username File Name (leave blank for default) ? '))
        if fip == '':
            fip = 'usernames.txt'
    else:
        fbl = False
        lc = int(input('     [>] Usernames Length ? '))
        ol = str(input('     [>] Do You Want Only Letters In Usernames (Y/n) ? ')).lower()
        if ol == 'y':
            ol = True
        else:
            ol = False
    ut = threading.Thread(target=update)
    ut.start()
    print('\n'*3)
    for thread in range(tc):
        t = threading.Thread(target=Checker)
        t.start()
        

def Checker():
    global tc, fbl, ol, lc, shit, hits, takens, fails, tries, fip
    if fbl:
        with open(fip, 'r+') as f:
            f = f.read().splitlines()
            for username in f:
                try:
                    ia = check(username)
                    tries += 1
                    if ia == False:
                        safeprint(Fore.GREEN + f'     [+] {username} Is Available !')
                        hits += 1
                    elif ia == True:
                        takens += 1
                        safeprint(Fore.RED + f'     [-] {username} Is Taken !')
                except Exception as e:
                    fails += 1
                    pass

    else:
        while True:
            username = get_random_string(lc)
            ia = check(username)
            tries += 1
            try:
                if ia == False:
                    safeprint(Fore.GREEN + f'     [+] {username} Is Available !')
                    hits += 1
                elif ia == True:
                    takens += 1
                    safeprint(Fore.RED + f'     [-] {username} Is Taken !')
            except Exception as e:
                fails += 1
                pass




    




if __name__ == __name__:
    loadproxies()
    main()
