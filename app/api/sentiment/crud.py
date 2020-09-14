from bson import json_util
from flask import current_app
import numpy as np

from app import db
from app.api.sentiment.models import Sentiment
from app.api.users.crud import get_user_by_id


def get_all_sentiments():
    """
    Returns the list of all sentiments

    :returns:
        List of all sentiments
    """
    return Sentiment.query.all()


def get_sentiment_by_id(sentiment_id):
    """
    Returns the sentiment with given id

    :param: sentiment_id
        ID of the sentiment
    :returns:
        Sentiment with given ID
    """
    sentiments = []
    cursor = current_app.mongo.keywords.find({"request_id": sentiment_id})

    for record in list(cursor):
        temp = []
        for i in record["classifications"]:
            sign = 1 if i["tag_name"] == "Positive" else -1
            temp.append(sign * i["confidence"])
        sentiments.extend(temp)

    arr = np.array(sentiments, dtype=np.float64)
    result = np.mean(arr)
    return {"score": result, "sentiment_id": sentiment_id}


def remove_sentiment(sentiment):
    """
    Removes the given sentiment

    :param: sentiment
        Sentiment to be removed
    """
    db.session.delete(sentiment)
    db.session.commit()


def update_sentiment(sentiment, keyword):
    """
    Utility method to update a sentiment
    :param: sentiment
        Sentiment to be updated
    :param: keyword
        Keyword for the sentiment analysis
    :returns:
        Updated sentiment
    """
    sentiment.keyword = keyword
    db.session.commit()
    return sentiment


def is_user_sentiment_quota_exhausted(user_id):
    """
    Utility method to find if user has exhausted their
    sentiment quota for keyword analysis

    :param: user_id
        ID of the user
    :returns:
        Status of quota
    """
    user = get_user_by_id(user_id)

    return user.sentiment_quota < 0


def update_user_sentiment_quota(user_id):
    """
    Utility method to update sentiment quota for a user

    :param: user_id
    """
    user = get_user_by_id(user_id)

    user.sentiment_quota -= 1
    db.session.commit()


def add_sentiment(keyword, user_id, job_id):
    """
    Adds a sentiment with given details and returns an instance of it.

    :param: keyword
        keyword to find sentiment for
    :param: user_id
        Id of the user
    :returns:
        Sentiment with given details
    """
    sentiment = Sentiment(keyword=keyword, user_id=user_id, job_id=job_id)
    db.session.add(sentiment)
    db.session.commit()

    update_user_sentiment_quota(user_id)
