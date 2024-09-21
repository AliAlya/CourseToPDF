import scrapetube
import os
from pyytdata import get_vid_info_from_url
import re


api_key = os.getenv('<YOUR API KEY HERE>')

def convert_subscribers(subscriber_str):
    if 'K' in subscriber_str:
        return int(float(subscriber_str.replace('K subscribers', '')) * 1000)
    elif 'M' in subscriber_str:
        return int(float(subscriber_str.replace('M subscribers', '')) * 1000000)
    elif subscriber_str == "1 subscriber":
        return 1
    else:
        return int(subscriber_str.replace(' subscribers', ''))

def get_channel_info(name, chan_id=None):
    channel_info = scrapetube.get_channel(channel_id=chan_id)
    video_urls = []
    for item in channel_info:
        base_url = "https://www.youtube.com/watch?v="
        video_id = item['videoId']
        video_urls.append(base_url + video_id)

    socials = []
    count = 0 
    for video in video_urls:
        video_info = get_vid_info_from_url(video)
        description = video_info.description
        if description == "":
            continue
        url_pattern = re.compile(r'https?://\S+')
        socials_urls = url_pattern.findall(description)
        if socials_urls == []:
            continue
        cleaned = []
        for item in socials_urls:
            if 'facebook' in item or 'instagram' in item or 'twitter' in item or 'linkedin' in item:
                cleaned.append(item)
        socials.append(cleaned)
        count += 1
        if count == 1:
            break

    if socials == [[]]:
        socials = ["No socials found"]
    return socials       

# def find_keys_with_subscriber_count(d, parent_key=''):
#     results = {}
#     if isinstance(d, dict):
#         for k, v in d.items():
#             if 'subscriber' in k.lower():
#                 results[parent_key + k] = v
#             if isinstance(v, (dict, list)):
#                 nested_results = find_keys_with_subscriber_count(v, parent_key + k + '.')
#                 results.update(nested_results)
#     elif isinstance(d, list):
#         for i, v in enumerate(d):
#             if isinstance(v, (dict, list)):
#                 nested_results = find_keys_with_subscriber_count(v, parent_key + f'[{i}].')
#                 results.update(nested_results)

#     for key, value in results.items():
#         return d[key]

def get_channels(catagory, limit):
    main_db = []
    channels = scrapetube.get_search(catagory,  results_type='channel', limit=limit)
    for channel in channels:
        try:
            channel_profile = []
            channel_profile.append(channel['title']['simpleText'])
            # Subs = channel['videoCountText']['simpleText'] 
            Subs = find_keys_with_subscriber_count(channel)
            channelId = channel['channelId']
            Subs = convert_subscribers(Subs)
            if Subs < 1000 or Subs > 100000:
                continue 
            channel_profile.append(Subs)
            channel_profile.append(channelId)
            main_db.append(channel_profile)
        except KeyError as e:
            print(f"key error here: {e}")
            continue

    return main_db


search = input("Enter a catagory: ")
list_channels = get_channels(search, 100)
count = 0
for item in list_channels:
    count += 1
    print("\n" + f"Number: {count}")
    print(item)
    # channel_info = get_channel_info(item[0], item[2])
    # print(channel_info)
    

