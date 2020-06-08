
# coding: utf-8

# In[1]:


import urllib.request
import json
import sys
import os 

# 1) 먼저 이 기능을 사용하기에 앞서 유튜브 채널 ID 값은 필수다.
# 예) https://www.youtube.com/channel/UC4f2f5bta_PQMxZxidhNagg 사람의 채널 ID를 가져왔다. (구독자 166명, 영상 50개)
# channelID = 'UC2qZjbvP5fw1Dc7M7uXqNFA'
# channelId = sys.argv[1] # Java로 부터 가져온 값
# savepath = sys.argv[2]

channelId = 'UCAyT8qyXujD_HK-O1WCb1Zw'
savepath = '/home/dino/python/'


# 2) channelID값을 기반으로 해당 유튜버의 전체 videoID 값을 가져온다.

# 해당 메서드는 YouTube Data API를 사용합니다.
def get_all_video_in_channel(channel_id):
    api_key = 'AIzaSyAGoo0WEEVLjgcEvpdP0Y3xdKS5gs2qHGQ' # 개발자의 YouTube APIKEY를 삽입한다.
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)
    video_links = []
    url = first_url
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(i['id']['videoId'])
#                 video_links.append(base_video_url + i['id']['videoId']) #기존에는 base_url을 더했으나 우리는 videoID만 필요하다.
        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links

allChannelId = get_all_video_in_channel(channelId)
#이제 allChannelId에는 해당 유튜버의 모든 videoID값이 저장되어있다. 

# 3) 수집된 videoID값들을 통해 각각의 영상에 등록된 댓글들을 Youtube Comment Scraper(node.js)를 통해 크롤링한다.
#파일저장경로 >>>>>>>>>>>>>>>>>>>>>> PC별로 변경해야함!
save_dir = savepath + 'datas/comment/' + channelId + '/' 

#폴더가 없으면 생성하는 메서드
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)
    
for videoID in allChannelId:
    os.popen('youtube-comment-scraper -o '+ save_dir + videoID + '.json ' + videoID).read()
    
#업데이트할때의 로직이 추가로 필요하다.

print('[prototype_autoScraper.py] has run successfully!')

