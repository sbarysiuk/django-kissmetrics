from base64 import encodestring, decodestring
from datetime import datetime
from simplejson import loads, dumps

from django.contrib.auth.models import User
from django.db import models


class KISSMETRICS_TYPE_CHOICES():

    ALIAS = u'alias'
    RECORD = u'record'
    SET = u'set'

    CHOICES = (
        (ALIAS, ALIAS),
        (RECORD, RECORD),
        (SET, SET),
    )

    KISS_TYPE = {
        'a': ALIAS,
        'e': RECORD,
        's': SET,
    }


class Events(models.Model):
    """
    This class it used to store kiss metric data.
    """
    action = models.CharField(
        max_length=64, blank=True,
        help_text="When event is record, break out the action for querying.")
    create_ts = models.DateTimeField(default=datetime.now)
    _data = models.TextField(db_column='data', blank=True)
    identity = models.CharField(
        max_length=64, db_index=True, help_text="The type of KISS identity.")
    type = models.CharField(
        max_length=12, choices=KISSMETRICS_TYPE_CHOICES.CHOICES,
        help_text="The type of KISS action.")
    user_id = models.IntegerField(
        User, db_index=True, null=True,
        help_text='If the user was determined for this identity, then set it')

    def set_data(self, data):
        self._data = encodestring(dumps(data))

    def get_data(self):
        return loads(decodestring(self._data))

    data = property(get_data, set_data)
