import requests
import pandas as pd

url = "https://tasty.co/api/proxy/tasty/feed-page?from=0&size=5&slug=healthy&type=topic"

payload = {}
headers = {
  'authority': 'tasty.co',
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': 'bf-geo-country=GB; gdpr=true; _amp_pd=amp-3c5d9d38-b331-4443-8ea4-c42eb5f51848; euconsent-v2=CPtJWIAPtJWIAAKAuAENDFCsAP_AAH_AAAwIJbtX_H__bW9r8f5_aft0eY1P99j77uQzDhfNk-4F3L_W_JwX52E7NF36tq4KmR4Eu3LBIUNlHNHUTVmwaokVryHsak2cpTNKJ6BEkHMRO2dYGF5umxtjeQKY5_p_d3fx2D-t_dv-3dz3z81Xn3dZf-_0-PCdU5_9Dfn9fRfb-9IL9_78v8v8_9_rk2_eX_3_79_7_H9-f_84JcAEmGrcQBdmUODNoGEUCIEYVhARQKACCgGFogIAFBwU7IwCfWESAFAKAIwIgQ4AoyIBAAAJAEhEAEgRYIAAABAIAAQAIBEIAGBgEFABYCAQAAgOgYohQACBIQJEREQpgQFQJBAS2VCCUF0hphAFWWAFAIjYKABEEgIrAAEBYOAYIkBKxYIEmINogAGAFAKJUK1FJ6aAhYzMAAAA.d5gACGAAAAAA; addtl_consent=1~39.4.3.9.6.9.13.6.4.15.9.5.2.11.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.20.5.20.6.5.1.4.11.29.4.14.4.5.3.10.6.2.9.6.6.9.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.146.8.42.15.1.14.3.1.18.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.7.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.1.4.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.10.15.2.5.6.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.2.2.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.14.1.3.3.4.5.4.3.2.2.5.4.1.1.2.9.1.6.9.1.5.2.1.7.10.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.4.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.6.2.1.6.2.3.2.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.4.1.5.1.2.4.3.8.2.2.9.7.2.2.1.2.1.4.6.1.1.6.1.1.2.6.3.1.2.201.300.100; bf_visit=u%3D.qya7YRvaP%26uuid%3Dc226b3e3-b169-4930-bc11-6c012da0f0fc%26v%3D2; bf-xdomain-session-uuid=3455a73a-ba47-4ae1-9449-daa17e61adc0; ccpa=true',
  'referer': 'https://tasty.co/topic/healthy',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

d = response.json()
for item in d['items']:
    print(item['id'])
    print(item['name'])