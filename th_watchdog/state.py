"""
Thornleigh Farm VPN Watchdog
State Module
author: hugh@blinkybeach.com
"""
import os
from th_watchdog.record import Record
from th_watchdog.nominal_email import NominalEmail
from th_watchdog.failure_email import FailureEmail
from th_watchdog.vpnstate import VPNState
from th_watchdog.emailstate import EmailState
from datetime import datetime


class State:
    """
    A record of the last observed state of the VPN connection
    """
    def __init__(self, filename: str) -> None:

        if not isinstance(filename, str):
            raise TypeError('statefile must be of type `str`')

        if '.state' not in filename:
            raise ValueError('filename must end in .state')

        if '/' in filename:
            raise ValueError('filename must reside in watchdog dir')

        self._filename = filename

        if not os.path.exists(filename):
            Record.write_null(filename)

        return

    was_previously_connected = property(lambda s: s._previously_connected())
    was_previously_disconnected = property(
        lambda s: not s._previously_connected()
    )
    email_sent = property(lambda s: s._email_sent())

    def record_nominal(self) -> None:
        """
        Record a nominal state
        """
        if self.was_previously_disconnected:
            NominalEmail()
        Record.nominal(self._filename)
        return None

    def record_disconnection(self) -> None:
        """
        Return a disconnected state
        """
        if self.was_previously_disconnected:
            if self.email_sent is True:
                return
        email = FailureEmail()
        Record(datetime.utcnow(), VPNState.DOWN, email.state).write(
            self._filename
        )
        return

    def _previously_connected(self) -> bool:
        """
        Return True if the VPN was previously observed to be disconnected
        """
        record = Record.from_file(self._filename)
        if record is None:
            return False
        if record.vpn == VPNState.DOWN:
            return False
        return True

    def _email_sent(self) -> bool:
        """
        Return True if a notification email was previously sent
        """
        record = Record.from_file(self._filename)
        if record is None:
            return False
        if record.email == EmailState.SENT:
            return True
        return False
