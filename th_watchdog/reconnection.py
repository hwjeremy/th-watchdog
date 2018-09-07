"""
Thornleigh Farm VPN Watchdog
Reconnection Module
author: hugh@blinkybeach.com
"""
from th_watchdog.state import State
from th_watchdog.ping_batch import PingBatch
from watchdog_config import VPN_SERVER_IP
from watchdog_config import VPN_START_COMMAND
from watchdog_config import VPN_STOP_COMMAND
from subprocess import call
from time import sleep


class Reconnection:
    """
    An attempt to reconnect to the VPN
    """
    STOP_COMMAND = VPN_STOP_COMMAND
    START_COMMAND = VPN_START_COMMAND
    RECONNECT_WAIT_TIME = 16

    def __init__(self, state: State) -> None:

        if not isinstance(state, State):
            raise TypeError('state must be of type `state`')

        self._succeeded = False
        self._state = state

        self._attempt()

        return

    succeeded = property(lambda s: s._succeeded)

    def _attempt(self) -> None:
        """
        Attempt reconnection
        """
        call(self.STOP_COMMAND, shell=True)
        call(self.START_COMMAND, shell=True)
        sleep(self.RECONNECT_WAIT_TIME)
        pings = PingBatch(VPN_SERVER_IP)
        if pings.successful:
            self._succeeded = True
            self._state.record_nominal()
            return

        self._state.record_disconnection()
        return
