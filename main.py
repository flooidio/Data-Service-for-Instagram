import logging
from pymongo import MongoClient

from config import *
from instagram_private_api import Client
logger = logging.getLogger(__name__)

def getAttribute(obj):
    output = {}
    for key, value in obj.__dict__.items():
        if type(value) is list:
            output[key] = [getAttribute(item) for item in value]
        else:
            try:
                output[key] = getAttribute(value)
            except:
                output[key] = value

    return output

class Insgram_DataService():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client(username, password)
        self.user_id = self.client.username_info(username)['user']['pk']
        client = MongoClient(host, port)
        self.db = client.instagram

    def get_followers(self):
        follower_collection = self.db.followers

        max_id = ""
        while True:
            follower_response = self.client.user_followers(self.user_id, max_id=max_id)
            for follower in follower_response['users']:
                follower_collection.update({'pk': follower['pk']}, {"$set": follower}, upsert=True)

            max_id = follower_response.get('next_max_id')
            if max_id is None:
                break

    def get_followings(self):
        following_collection  = self.db.followings

        max_id = ""
        while True:
            following_response = self.client.user_following(self.user_id, max_id=max_id)
            for following in following_response['users']:
                following_collection.update({'pk': following['pk']}, {"$set": following}, upsert=True)

            max_id = following_response.get('next_max_id')
            if max_id is None:
                break

    def retrive_posts(self, user_id):
        print (user_id)
        post_collection = self.db.posts

        max_id = ""
        while True:
            post_response = self.client.user_feed(user_id, max_id=max_id)
            for post in post_response['items']:
                post_collection.update({'pk': post['pk']}, {"$set": post}, upsert=True)

            max_id = post_response.get('next_max_id')
            if max_id is None:
                break

    def retrive_comments(self, media_id):
        comment_collection = self.db.comments

        max_id = ""
        while True:
            comment_response = self.client.media_comments(media_id, max_id=max_id)
            for comment in comment_response['comments']:
                comment_collection.update({'pk': comment['pk']}, {"$set": comment}, upsert=True)

            max_id = comment_response.get('next_max_id')
            if max_id is None:
                break


if __name__ == "__main__":


    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    logger.info("started")


    username = username
    password = password

    service = Insgram_DataService(username, password)

    service.get_followers()
    service.get_followings()

    followerIds = [item['pk'] for item in list(service.db.followers.find({}, {'pk': 1}))]
    print (followerIds)
    for followerId in followerIds:
        print (followerId)
        service.retrive_posts(followerId)


    mediaIds = [item['pk'] for item in list(service.db.posts.find({}, {'pk':1}))]
    for mediaId in mediaIds:
        service.retrive_comments(mediaId)


