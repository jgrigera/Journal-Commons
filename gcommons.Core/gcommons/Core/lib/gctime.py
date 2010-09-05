
import logging
from datetime import datetime
from DateTime import DateTime

logger = logging.getLogger("gcommons.Core.lib.gctime")

def gcommons_userfriendly_date(a_datetime):
    """
    a_datetime can be a string or DateTime object
    
    returns a string
    """
    now = datetime.now()
    if type(a_datetime) is str:
        a_datetime = DateTime(a_datetime)

    diff = now - datetime.fromtimestamp(a_datetime.timeTime())
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"
