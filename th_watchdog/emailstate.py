"""
Thornleigh Farm - VPN Watchdog
EmailState Module
author: hugh@blinkybeach.com
"""

from enum import Enum


class EmailState(Enum):
    """
    Potential states of email sending
    """
    SENT = 'sent'
    UNSENT = 'unsent'
    NOT_APPLICABLE = 'na'
