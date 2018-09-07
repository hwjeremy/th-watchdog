"""
Thornleigh Farm - VPN Watchdog
Nominal Email Module
author: hugh@blinkybeach.com
"""
from th_watchdog.email import Email


class NominalEmail(Email):
    """
    An email notifying the administrator of a nominal state
    """
    SUBJECT = 'Starport VPN connection restored'
    BODY = 'Starport has regained connection to the VPN'

    def __init__(self):
        super().__init__(self.SUBJECT, self.BODY)
        return
