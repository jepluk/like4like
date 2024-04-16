import requests as r
import re, random, os, json, time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError

password = 'akun123'
account = ['jamalud', 'azzamxyz', 'tukimins', 'tukimans', 'animexyz']
credits = 'Meizug'
host    = 'https://www.like4like.org/'
feature = list()

def user_login():
    account_data = list()
    print('Sedang menyiapkan sesi. Silahkan tunggu sebentar.')
    print('Coded by (Meizug)')

    for username in account:
        ses = r.session()
        ses.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Encoding': 'gzip, deflate','Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','sec-ch-ua': '"Google Chrome";v="118", "Chromium";v="118", "Not=A?Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': UserAgent().random,'X-Requested-With': 'XMLHttpRequest'})
    
        source = ses.get(host +'login').text
        response = ses.post(host +'api/login.php', data={'time':re.search(r'time=(.*?)\&', source).group(1), 'token':re.search(r'token=(.*?)";', source).group(1), 'username':username, 'password':password, 'recaptcha':''}).json()
        
        print()
        if response['success']:
            print('>> LOGIN BERHASIL')
            account_data.append((ses, username))
        else:
            print('>> LOGIN GAGAL')

        print('>> Username  : '+ username)
        print('>> Credits   : '+ str(uinfo(ses)[0]))
        print('>> Refound   : '+ str(refound(ses)))
        print('>> Useragent : '+ ses.headers.get('User-Agent'))
        
        if len(feature) == 0: scraping_feature(ses)
        # exit(feature)

    account.clear()
    account.extend(account_data)

def uinfo(ses):
    response = ses.get(host +'api/get-user-info.php').json()
    if response['success']: return (response['data']['credits'], response['data']['weeklyPosition'], response['data']['weeklyReferralPosition'])
    else: return (response['error'], response['error'], response['error'])

def refound(ses):
    response = ses.get(host +'api/get-notifications.php').json()
    if response['success']: return response['data']['refundedCredits']
    else: return response['error']

def scraping_feature(ses):
    source = BeautifulSoup(ses.get(host +'earn-credits.php').text, 'html.parser')
    feature.extend([(option['value'], option.text) for option in source.find_all('option')])

def main():
    os.system('clear')
    print('Mining koin web like4like.org.')
    print('Coded by (Meizug)')
    print('Account: '+ str(len(account)))
    print()

    while True:
        try:
            with ThreadPoolExecutor(max_workers=30) as thread:
                for i in range(100):
                    thread.submit(mining)
        except KeyboardInterrupt:
            break

def mining():
    try:
        for ses, uname in account:
            ft = random.choice(feature)
            feature_set = ft[0]
            ses.get(host +'earn-credits.php?feature='+ feature_set) #refresh
            response = ses.get(host +'api/get-tasks.php?feature='+ feature_set).json()
            
            if response['success']:
                try: core = response['data']['tasks'][0]
                except:
                    # print(f'Log({uname}) >> get task error!')
                    continue
                
                rewards = core['value']
                patch = {'idzad': core['idlink'],'vrsta': core['featureType'],'idcod': core['taskId'],'feature': feature_set, '_': int(time.time() * 1000)}
                response = ses.get(host +'api/start-task.php?' + '&'.join('%s=%s' % (key, value) for key, value in patch.items())).json()
                
                if response['success']:
                    data = {'url': core['url'], 'idzad': patch['idcod'], 'idlinka': patch['idzad'],'idclana': response['data']['codedTask'] + '=true', 'vrsta': patch['vrsta'], 'feature': feature_set, 'addon': 'false', 'version': ''}
                    response = ses.post(host +'api/validate-task.php', data=data).json()
                    # print(response)
                    
                    if response['success']:
                        my_credits = response['data']['credits']
                        if my_credits == 0:
                            # print(f'Log({uname}) >> 0 validate task error!')
                            continue

                        print('>> BERHASIL MENGERJAKAN MISI')
                        print('>> Username : '+ uname)
                        print('>> Rewards  : '+ str(rewards) +' Coins')
                        print('>> Credits  : '+ str(my_credits) +' Coins')
                        print('>> Task Name: '+ ft[1])
                        print()
                        
                    else:
                        # print(f'Log({uname}) >> validate task error!')
                        continue
                else:
                    # print(f'Log({uname}) >> start task error!')
                    continue
            else:
                # print(f'Log({uname}) >> get task error!')
                continue
    except ConnectionError:
        print('Koneksi error.')
        time.sleep(10)

    

if __name__ == "__main__":
    os.system('clear')
    user_login()
    main()

