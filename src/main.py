import os
import datetime
import json
from pathlib import Path

import requests
from dotenv import load_dotenv
from pydantic import HttpUrl
from typing import List

load_dotenv()  # take environment variables from .env.


endpoint: HttpUrl = "https://api.twitter.com/2/users/{id}/tweets".format(id=os.environ['TWITTER_USER_ID'])

today = datetime.date.today()

expansion_list: List[str] = [
    "attachments.poll_ids",
    "attachments.media_keys",
    "author_id",
    "entities.mentions.username",
    "geo.place_id",
    "in_reply_to_user_id",
    "referenced_tweets.id",
    "referenced_tweets.id.author_id"
]
tweetField_list: List[str] = [
    "attachments",
    "author_id",
    "context_annotations",
    "conversation_id",
    "created_at",
    "entities",
    "id",
    "in_reply_to_user_id",
    "public_metrics",
    "possibly_sensitive",
    "referenced_tweets",
    "reply_settings",
    "source",
    "text"
]
userField_list: List[str] = [
    "created_at",
    "description",
    "entities",
    "id",
    "location",
    "name",
    "pinned_tweet_id",
    "profile_image_url",
    "protected",
    "public_metrics",
    "url",
    "username",
    "verified"
]
mediaField_list: List[str] = [
    "duration_ms",
    "height",
    "media_key",
    "preview_image_url",
    "type",
    "url",
    "width",
    "public_metrics",
    "non_public_metrics",
    "organic_metrics",
    "promoted_metrics"
]
pollField_list: List[str] = [
    "duration_minutes",
    "end_datetime",
    "id",
    "options",
    "voting_status"
]

params: dict = {
    'max_results': 100,
    # 昨日から今日の0時まで，さらにそれをUTCに合わせるのでさらに9時間巻き戻ると，開始時刻は一昨日の15時になる
    'start_time': "{yesterday}T{UTC}".format(
        yesterday=today + datetime.timedelta(days=-2) if os.environ.get('DATE_START') is None else os.environ['DATE_START'],
        UTC="15:00:00Z"
    ),
    'end_time': "{today}T{UTC}".format(
        today=today + datetime.timedelta(days=-1) if os.environ.get('DATE_END') is None else os.environ['DATE_END'],
        UTC="15:00:00Z"
    ),
    "expansions": ",".join(expansion_list),
    "tweet.fields": ",".join(tweetField_list),
    "user.fields": ",".join(userField_list),
    "media.fields": ",".join(mediaField_list),
    "poll.fields": ",".join(pollField_list)
}

headers = {
    'Authorization': 'Bearer {bearer_token}'.format(bearer_token=os.environ['bearer_token']),
    'Content-Type': 'application/json; charset=utf-8'
}

res = requests.get(endpoint, params=params, headers=headers)
json_data = res.json()


date = today + datetime.timedelta(days=-1) if os.environ.get('DATE_END') is None else os.environ['DATE_END']
yesterday = datetime.date.fromisoformat(str(date))

root_dir = Path(__file__).parents[1]
data_dir = root_dir / 'data'
month_dir = data_dir / yesterday.strftime('%Y') / yesterday.strftime('%B')
Path.mkdir(month_dir, exist_ok=True, parents=True)
output_file = month_dir / 'get-users-id-tweets_{date}.json'.format(date=str(date))

with open(output_file, 'w') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)
