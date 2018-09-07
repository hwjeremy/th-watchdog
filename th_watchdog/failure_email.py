"""
Thornleigh Farm - VPN Watchdog
Failure Email Module
author: hugh@blinkybeach.com
"""
from th_watchdog.email import Email


class FailureEmail(Email):
    """
    An email notifying the administrator of a failed state
    """
    SUBJECT = 'Starport VPN connection lost'
    BODY = 'Starport has lost connection to the VPN'

    def __init__(self):
        super().__init__(self.SUBJECT, self.BODY)
        return
