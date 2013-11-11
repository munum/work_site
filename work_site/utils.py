# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

import string
import random
import os

from datetime import datetime


# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

ALLOWED_AVATAR_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Form validation

USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25

REALNAME_LEN_MIN = 4
REALNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16

DOB_YEAR_MIN = 1900
DOB_YEAR_MAX = 2012

DEPOSIT_MIN = 0.00
DEPOSIT_MAX = 9999999999.99

# Sex type.
#MALE = 1
#FEMALE = 2
#SEX_TYPE = {
#    MALE: u'Male',
#    FEMALE: u'Female'
#}

# Model
STRING_LEN = 64

class Storage(dict):
    """
    A Storage object is like a dictionary but setattr can also
    be used.

    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

storage = Storage

class Enum(Storage):

    def __init__(self, *a):
        self.name = tuple(a)
        Storage.__init__(self, ((e, i) for i, e in enumerate(a)))

    def __contains__(self, item):
        if isinstance(item, int):
            return item in list(self.values())
        else:
            return Storage.__contains__(self, item)

SEX_TYPE = Enum('MALE', 'FEMALE')


def get_current_time():
    return datetime.utcnow()


def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_AVATAR_EXTENSIONS


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    #return base64.urlsafe_b64encode(os.urandom(size))
    return ''.join(random.choice(chars) for x in range(size))


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception, e:
        raise e
