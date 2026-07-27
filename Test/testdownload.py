import requests
import re
import json
url = 'https://www.bilibili.com/video/BV1jt421c7yN/'
cookie = "buvid3=2844B77E-F527-FB05-1DF5-9FDF834AE3E888277infoc; b_nut=1709986388; i-wanna-go-back=-1; b_ut=7; _uuid=6577D687-BED9-9AE2-106A10-551210627F5AC88087infoc; enable_web_push=DISABLE; buvid4=5ED5B3A0-A998-7D47-3815-9AD9A1B27A4989131-024030912-0Fw3r6dKwZLwPoWOl%2F8HuA%3D%3D; CURRENT_FNVAL=4048; rpdid=|(u|Jmkkuukk0J'u~u|ulR~)~; header_theme_version=CLOSE; fingerprint=c27c0b59dd10dcdc4c14701a58f49669; buvid_fp_plain=undefined; buvid_fp=c27c0b59dd10dcdc4c14701a58f49669; LIVE_BUVID=AUTO6217111182462626; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; bp_video_offset_691902317=925084214145056785; DedeUserID=691902317; DedeUserID__ckMd5=ead312019baad7ed; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTYwNDM3MDgsImlhdCI6MTcxNTc4NDQ0OCwicGx0IjotMX0.Rdjc9F5oiEXSn_GylRWm3s2L-Pn8GYfyQS5IZt_Y3-8; bili_ticket_expires=1716043648; SESSDATA=3d6f944f%2C1731336513%2C491d2%2A51CjD5jp6zedAz4nQallTN_akUjFzg2LzJhdKMiJbI1nnw2bs5sp8Y09F7Jj4PofjUyfsSVlktMkF0aDRLN196dVNTeWh0czllbFZTWDlidWRpcnFnaENSNVVNbGNFMGR5bFBqYkcwalhuVklyUGJLVHJtYXo3TVpaTENqQ21rS0RPbldWTDUzRFp3IIEC; bili_jct=2975523315e5bccfa606ac286df61f36; home_feed_column=4; browser_resolution=1396-639; sid=6gr3y4l0; PVID=4; bp_t_offset_691902317=932475264446758937; b_lsid=5E9C415B_18F86EC150D"
headers = {
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Cookie": cookie
}
response = requests.get(url=url, headers=headers)
html = response.text
print(html)
title = re.findall('title="(.*?)"', html)[0]
print(title)
info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
json_data = json.loads(info)
video_url = json_data['data']['dash']['video'][0]['baseUrl']
print(video_url)
audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
print(audio_url)
video_content = requests.get(url=video_url, headers=headers).content
audio_content = requests.get(url=audio_url, headers=headers).content
with open('video\\' + title + '.mp4', mode='wb') as v:
    v.write(video_content)
with open('video\\' + title + '.mp3', mode='wb') as a:
    a.write(audio_content)