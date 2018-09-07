"""
Thornleigh Farm VPN Watchdog
Ping Module
author: hugh@blinkybeach.com
"""

from ping3 import ping
from typing import Optional


class Ping:
    """
    An attempt to ICMP ping a host.
    """
    UNIT = 'ms'
    TIMEOUT = 2.2

    def __init__(self, host: str) -> None:

        assert isinstance(host, str)
        self._host = host
        self._result: Optional[int] = None

        result = ping(
            self._host,
            timeout=self.TIMEOUT,
            unit=self.UNIT
        )

        if result is None:
            return

        assert isinstance(result, float)
        self._result = int(result)

        return

    succeeded = property(lambda s: s._successful())
    result = property(lambda s: s._result)
    report = property(lambda s: s._report())

    def _successful(self) -> bool:
        """
        Return true if this Ping was successful
        """
        if self._result is None:
            return False
        return True

    def _report(self) -> str:
        """
        Return a string describing the result of the ping attempt
        """
        if self._result is None:
            report = 'Attempt to ping {host} failed'
            return report.format(host=self._host)
        report = 'Successfully pinged {host} in {time}{unit}'
        return report.format(
            host=self._host,
            time=str(self._result),
            unit=self.UNIT
        )


if __name__ == '__main__':
    google_ping = Ping('google.com')
    print(google_ping.report)
