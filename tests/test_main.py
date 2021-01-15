
import os
import datetime
# import pytest
from pathlib import Path
# import urllib.parse
# import urllib.request
from pydantic import HttpUrl
# from pydantic import BaseModel


from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


def connect_twitter_api_v2():
    endpoint: HttpUrl = "https://api.twitter.com/2/users/{id}/tweets".format(
        id=os.environ['TWITTER_USER_ID'])
    return endpoint


def test_connect_twitter_api_v2():
    """endpointがただしいか検証する"""
    assert connect_twitter_api_v2() == "https://api.twitter.com/2/users/707346268821913600/tweets"


def data_date():
    return "{today}T{UTC_PLUS_0900}".format(today=datetime.date.today(), UTC_PLUS_0900="09:00:00Z")


def test_data_date():
    assert data_date() == "{today}T09:00:00Z".format(today=datetime.date.today())


def data_expansion():
    expansion_list = [
        "attachments.poll_ids",
        "attachments.media_keys",
        "author_id",
        "entities.mentions.username",
        "geo.place_id",
        "in_reply_to_user_id",
        "referenced_tweets.id",
        "referenced_tweets.id.author_id"
    ]

    return ",".join(expansion_list)


def test_data_expansion():

    assert data_expansion() == "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username," \
        "geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id"


def data_tweetField():
    tweetField_list = [
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
    return ",".join(tweetField_list)


def test_data_tweetField():

    assert data_tweetField() == "attachments,author_id,context_annotations,conversation_id,created_at," \
        "entities,id,in_reply_to_user_id,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text"


def data_userField():
    userField_list = [
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
    return ",".join(userField_list)


def test_data_userField():

    assert data_userField() == "created_at,description,entities,id,location,name," \
        "pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified"


def data_mediaField():
    mediaField_list = [
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
    return ",".join(mediaField_list)


def test_data_mediaField():
    assert data_mediaField() == "duration_ms,height,media_key,preview_image_url,type," \
        "url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics"


def data_pollField():
    pollField_list = [
        "duration_minutes",
        "end_datetime",
        "id",
        "options",
        "voting_status"
    ]
    return ",".join(pollField_list)


def test_data_pollField():

    assert data_pollField() == "duration_minutes,end_datetime,id,options,voting_status"


def get_bearer_token():
    return os.environ['bearer_token']


def test_get_bearer_token():
    assert isinstance(get_bearer_token(), str)


def test_root_dir():
    location = Path(__file__)
    parent_dir = location.parent
    root_dir = parent_dir.parent
    assert location.name == 'test_main.py'
    assert parent_dir.name == 'tests'
    assert root_dir.name == 'tweetArchives'


def test_yesterday():
    os.environ['DATE_END'] = '2021-01-01'
    today = datetime.date.today()
    date = today + datetime.timedelta(days=-1) if os.environ.get('DATE_END') is None else os.environ['DATE_END']
    yesterday = datetime.date.fromisoformat(str(date))

    assert yesterday.strftime('%b') == 'Jan'
    assert yesterday.strftime('%Y') == '2021'
    assert yesterday.strftime('%B') == 'January'
    assert yesterday.strftime('%U').isnumeric() is True  # week number 0 - 53
