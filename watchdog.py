"""
Thornleigh Farm VPN Watchdog
Core Module
author: hugh@blinkybeach.com
"""
from th_watchdog.ping_batch import PingBatch
from th_watchdog.state import State
from watchdog_config import VPN_SERVER_IP
from watchdog_config import INET_CHECK_IP
from watchdog_config import DNS_CHECK_HOST
from watchdog_config import RECORD_FILENAME
from th_watchdog.reconnection import Reconnection


def patrol() -> None:
    """
    Examine the state of the VPN connection. Record anomolies, and perform
    repair procedures where possible.
    """
    state = State(RECORD_FILENAME)
    vpn_check = PingBatch(VPN_SERVER_IP)
    if vpn_check.successful is True:
        state.record_nominal()
        return

    # If we can't connect to the internet, we should return. Nothing can
    # done.

    internet_check = PingBatch(INET_CHECK_IP)
    if internet_check.successful is False:
        return

    dns_check = PingBatch(DNS_CHECK_HOST)
    if dns_check.successful is False:
        return

    state.record_disconnection()
    Reconnection(state)
    return


if __name__ == '__main__':
    patrol()
