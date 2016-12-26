import datetime
from collections import Mapping

import peewee as pw
from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.csv_utils import dump_csv
import pandas as pd
import gzip
from secrets import DB_NAME, DB_PASSWORD, DB_USER

db = pw.SqliteDatabase('tweets.db')
psql_db = pw.PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD)
import models

class BaseModel(pw.Model):
    class Meta:
        database = db


class Place(BaseModel):
    """Twitter API json "place" key"""
    id_str = pw.CharField()
    place_type = pw.CharField(null=True)
    country_code = pw.CharField(null=True)
    country = pw.CharField(null=True)
    name = pw.CharField(null=True)
    full_name = pw.CharField(null=True)
    url = pw.CharField(null=True)  # URL to json polygon of place boundary
    bounding_box_coordinates = pw.CharField(null=True)  # json list of 4 [lat, lon] pairs


class User(BaseModel):
    id_str = pw.CharField(null=True)  # v4
    screen_name = pw.CharField(null=True)
    verified = pw.BooleanField(null=True)  # v4
    time_zone = pw.CharField(null=True)  # v4
    utc_offset = pw.IntegerField(null=True)  # -28800 (v4)
    protected = pw.BooleanField(null=True)  # v4
    location = pw.CharField(null=True)  # Houston, TX  (v4)
    lang = pw.CharField(null=True)  # en  (v4)
    followers_count = pw.IntegerField(null=True)
    created_date = pw.DateTimeField(default=datetime.datetime.now)
    statuses_count = pw.IntegerField(null=True)
    friends_count = pw.IntegerField(null=True)
    favourites_count = pw.IntegerField(default=0)


class Tweet(BaseModel):
    id_str = pw.CharField(null=True)
    in_reply_to_id_str = pw.CharField(null=True, default=None)
    in_reply_to = pw.ForeignKeyField('self', null=True, related_name='replies')
    user = pw.ForeignKeyField(User, null=True, related_name='tweets')
    source = pw.CharField(null=True)  # e.g. "Twitter for iPhone"
    text = pw.CharField(null=True)
    tags = pw.CharField(null=True)  # e.g. "#sarcasm #angry #trumped"
    created_date = pw.DateTimeField(default=datetime.datetime.now)
    location = pw.CharField(null=True)
    place = pw.ForeignKeyField(Place, null=True)
    favorite_count = pw.IntegerField(default=0)


def tweets_to_df():
    tweets = []
    for t in Tweet.select():
        try:
            tweets += [(t.user.screen_name, t.text, t.tags, t.favorite_count, t.user.followers_count, t.user.friends_count, t.user.statuses_count)]
        except:
            tweets += [(None, t.text, t.tags, t.favorite_count, None, None, None)]
    return pd.DataFrame(tweets)


def dump_tweets(name='twitterbot'):
    with gzip.open(name + '-tweets-2016-12-11.csv.gz', 'w') as fout:
        query = Tweet.select()
        dump_csv(query, fout)
    with gzip.open(name + '-tweets-2016-12-11.csv.gz', 'w') as fout:
        query = User.select()
        dump_csv(query, fout)


def create_tables():
    db.connect()
    db.create_tables([Place, User, Tweet])


def pw2dj(tables=((User, models.User), (Place, models.Place), (Tweet, models.Tweet)):
    for from_cls, to_cls in tables:

        print('=' * 100)
        print('Copying {} -> {}'.format(from_cls, to_cls))

        query = from_cls.select()
        N = query.count()
        for i, obj in enumerate(query):
            if not i % 1000:
                N = FromTable.select.count()
            print('Saving {:08d}/{08d} {}: {}'.format(i, N, round(i * 100. / N, 1), obj))
            ToTable(obj).save()


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
