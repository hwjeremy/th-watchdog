"""
Thornleigh Farm - VPN Watchdog
VPNState Module
author: hugh@blinkybeach.com
"""

from enum import Enum


class VPNState(Enum):
    """
    Potential states of the VPN connection
    """
    UP = 'up'
    DOWN = 'down'
