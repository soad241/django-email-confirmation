from redisconnection.util import get_connection, format_minute, format_date


connection = get_connection()

def ses_sent_minute_key():
    return "ses_sent:min:{0}".format(format_minute())    


def ses_sent_today_key():
    return "ses_sent:day:{0}".format(format_date())    


def acquire_ses_sent_lock():
    key = ses_sent_minute_key()
    res = connection.setnx(key, 1)
    if res:
        connection.expire(key, 60*20)        
    return res    


def get_num_ses_sent_today():
    return int(connection.get(ses_sent_today_key())) or 0
    
        
def incr_num_ses_sent_today():
    key = ses_sent_today_key()
    res = connection.incr(key)
    connection.expire(key, 60*60*72)    
    return res
    