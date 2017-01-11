import datetime
from collections import Mapping

import peewee as pw
from playhouse.shortcuts import model_to_dict, dict_to_model


db = pw.SqliteDatabase('tweets_v2.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Place(BaseModel):
    """Twitter API json "place" key"""
    place_type = pw.CharField()
    country_code = pw.CharField()
    country = pw.CharField()
    name = pw.CharField()
    full_name = pw.CharField()
    url = pw.CharField()  # URL to json polygon of place boundary
    bounding_box_coordinates = pw.CharField()  # json list of 4 [lat, lon] pairs


class User(BaseModel):
    # id = pw.BigIntegerField()
    screen_name = pw.CharField(unique=True)
    # location = pw.ForeignKey(Place)
    followers_count = pw.IntegerField(null=True)
    created_date = pw.DateTimeField(default=datetime.datetime.now)
    statuses_count = pw.IntegerField(null=True)
    friends_count = pw.IntegerField(null=True)
    favourites_count = pw.IntegerField(default=0)


class Tweet(BaseModel):
    id = pw.BigIntegerField(null=True)
    id_str = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, null=True, related_name='tweets')
    source = pw.CharField(null=True)  # e.g. "Twitter for iPhone"
    text = pw.CharField()
    tags = pw.CharField(null=True)  # e.g. "#sarcasm #angry #trumped"
    created_date = pw.DateTimeField(default=datetime.datetime.now)
    location = pw.CharField(null=True)
    place = pw.ForeignKeyField(Place, null=True)
    verified = pw.BooleanField(null=True)
    favorite_count = pw.IntegerField(default=0)
    # tweet_replied_to = pw.ForeignKeyField("Tweet", related_name='replies')


class Reply(BaseModel):
    # in_reply_to_status_id
    tweet_replied_to = pw.ForeignKeyField(Tweet, related_name='replies')
    tweet = pw.ForeignKeyField(Tweet, related_name='prompts')


def create_tables():
    db.connect()
    db.create_tables([Place, User, Tweet, Reply])


class Serializer(object):
    """Callable serializer. An instance of this class can be passed to the `default` arg in json.dump

    >>> json.dumps(model.Tweet(), default=Serializer(), indent=2)
    {...}
    """
    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    datetime_format = ' '.join([date_format, time_format])

    def convert_value(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime(self.datetime_format)
        elif isinstance(value, datetime.date):
            return value.strftime(self.date_format)
        elif isinstance(value, datetime.time):
            return value.strftime(self.time_format)
        elif isinstance(value, pw.Model):
            return value.get_id()
        else:
            return value

    def clean_data(self, data):
        # flask doesn't bother with this condition check, why?
        if isinstance(data, Mapping):
            for key, value in data.items():
                if isinstance(value, dict):
                    self.clean_data(value)
                elif isinstance(value, (list, tuple)):
                    data[key] = map(self.clean_data, value)
                else:
                    data[key] = self.convert_value(value)
        return data

    def serialize_object(self, obj, **kwargs):
        data = model_to_dict(obj, **kwargs)
        return self.clean_data(data)

    def __call__(self, obj, **kwargs):
        return self.serialize_object(obj, **kwargs)


class Deserializer(object):
    def deserialize_object(self, model, data, **kwargs):
        return dict_to_model(model, data, **kwargs)
