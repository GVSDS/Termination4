"""import requests
import re
import json

def get_douyin_video_no_watermark(url):
    try:
        # 获取重定向后的真实URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        response = requests.get(url, headers=headers, allow_redirects=False)
        real_url = response.headers['Location']
        
        # 从真实URL中提取视频ID
        video_id = re.findall(r'/video/(\d+)', real_url)[0]
        print(real_url)
        
        # 构造API请求URL
        api_url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
        
        # 获取视频信息
        response = requests.get(api_url, headers=headers)
        print(response.text)
        data = json.loads(response.text)
        
        # 提取无水印视频URL
        video_url = data['item_list'][0]['video']['play_addr']['url_list'][0]
        video_url = video_url.replace('playwm', 'play')  # 去除水印关键步骤
        
        return video_url
    except Exception as e:
        print(f"发生错误: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    share_url = input("请输入抖音分享链接: ")
    video_url = get_douyin_video_no_watermark(share_url)
    
    if video_url:
        print("无水印视频URL:", video_url)
        # 下载视频
        print("正在下载视频...")
        video_data = requests.get(video_url, headers={'User-Agent': 'Mozilla/5.0'}).content
        with open('douyin_video.mp4', 'wb') as f:
            f.write(video_data)
        print("视频已保存为 douyin_video.mp4")
    else:
        print("获取视频失败，请检查链接是否正确")

"""
