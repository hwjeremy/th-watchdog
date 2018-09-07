"""
Thornleigh Farm - VPN Watchdog
Record Module
author: hugh@blinkybeach.com
"""
from th_watchdog.vpnstate import VPNState
from th_watchdog.emailstate import EmailState
from typing import TypeVar
from datetime import datetime
from typing import Optional
from typing import Type
import os

T = TypeVar('T', bound='Record')


class Record:
    """
    A string record of VPN connection state
    """
    TIME_FORMAT = '[%Y-%m-%d_%H:%M:%S]'
    NULL_VALUE = 'null\n'

    def __init__(
        self,
        time: datetime,
        vpn: VPNState,
        email: EmailState
    ) -> None:

        # Example
        # [2018-12-01_12:51:12],down,unsent
        # time,vpnstate,emailsent

        if not isinstance(time, datetime):
            raise TypeError('time must be of type `datetime`')
        if not isinstance(vpn, VPNState):
            raise TypeError('vpn must be of type `VPNState`')
        if not isinstance(email, EmailState):
            raise TypeError('email must be of type `EmailState')

        self._time = time
        self._vpn = vpn
        self._email = email

        return

    serialised = property(lambda s: s._serialise())
    vpn = property(lambda s: s._vpn)
    time = property(lambda s: s._time)
    email = property(lambda s: s._email)

    def _serialise(self) -> str:
        """
        Return a string serialised record
        """
        record = self._time.strftime(self.TIME_FORMAT)
        record += ',' + self._vpn.value
        record += ',' + self._email.value
        record += '\n'
        return record

    @classmethod
    def from_string(cls: Type[T], raw_string) -> Optional[T]:
        """
        Return a new record
        """
        if not isinstance(raw_string, str):
            raise TypeError('raw_string must be of type `str`')

        if raw_string == Record.NULL_VALUE:
            return None

        if raw_string[-1] == '\n':
            raw_string = raw_string[:-1]

        pieces = raw_string.split(',')
        if len(pieces) != 3:
            raise ValueError('Unexpected record format')

        time = datetime.strptime(pieces[0], Record.TIME_FORMAT)
        vpn = VPNState(pieces[1])
        email = EmailState(pieces[2])
        record = cls(time, vpn, email)

        return record

    @classmethod
    def from_file(cls: Type[T], filename: str) -> Optional[T]:
        """
        Return a Record from a file
        """
        if not os.path.exists(filename):
            return None

        with open(filename, 'r') as rfile:
            return cls.from_string(rfile.read())

    @classmethod
    def nominal(cls, filename: str) -> None:
        """
        Write a nominal state
        """
        assert isinstance(filename, str)
        now = datetime.utcnow()
        record = cls(now, VPNState.UP, EmailState.NOT_APPLICABLE)
        record.write(filename)
        return

    @classmethod
    def write_null(cls, filename: str) -> None:
        """
        Write a null record to a file
        """
        assert isinstance(filename, str)
        with open(filename, 'w') as wfile:
            wfile.write(Record.NULL_VALUE)
        return

    def write(self, filename: str) -> None:
        """
        Write this record to a file
        """
        with open(filename, 'w') as wfile:
            wfile.write(self._serialise())
        return
