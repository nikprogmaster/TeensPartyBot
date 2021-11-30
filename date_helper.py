import datetime

SPACE = " "


def get_time_interval(party_date):
    now = datetime.datetime.now()
    if party_date > now:
        interval_in_s = (party_date - now).total_seconds()
        days = interval_in_s // 86400
        hours = (interval_in_s % 86400) // 3600
        minutes = ((interval_in_s % 86400) % 3600) // 60
        result = ""
        if days != 0:
            result += str(int(days)) + SPACE + get_correct_day_ending(days)
        if hours != 0:
            result += SPACE + str(int(hours)) + SPACE + get_correct_hour_ending(hours)
        if minutes != 0:
            result += SPACE + str(int(minutes)) + SPACE + get_correct_minute_ending(minutes)
        return result


def get_correct_hour_ending(hours):
    o = hours % 10
    if o == 1:
        return 'час'
    elif o == 2 or o == 3 or o == 4:
        return 'часа'
    else:
        return 'часов'


def get_correct_minute_ending(minute):
    o = minute % 10
    if o == 1:
        return 'минута'
    elif o == 2 or o == 3 or o == 4:
        return 'минуты'
    else:
        return 'минут'


def get_correct_day_ending(days):
    o = days % 10
    if o == 1:
        return 'день'
    elif o == 2 or o == 3 or o == 4:
        return 'дня'
    else:
        return 'дней'