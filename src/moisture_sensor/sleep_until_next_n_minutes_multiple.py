import time
import datetime


def sleep_until_next_n_minutes_multiple(n):
    """
    Sleeps until the next n minute multiple from the full hour.
    Best suited for time spans with 60 % n = 0 i.e. 1, 2, 3, 5, 10, 15, 20, 30, 60
    """
    now = datetime.datetime.now()

    # Calculate the number of minutes to add to reach the next n-minute mark
    minutes_to_add = n - (now.minute % n)

    # Calculate the seconds to sleep
    seconds_to_sleep = minutes_to_add * 60 - now.second
    time.sleep(seconds_to_sleep)
