"""
Thornleigh Farm VPN Watchdog
Ping Batch Module
author: hugh@blinkybeach.com
"""

from th_watchdog.ping import Ping


class PingBatch:
    """
    Send a number of pings, defining success as a number of those pings
    succeeding
    """
    def __init__(self, host: str, number: int = 3, success: int = 1) -> None:

        assert isinstance(number, int)
        assert isinstance(success, int)
        if success > number:
            raise ValueError('success must be <= number')

        if not isinstance(host, str):
            raise TypeError('host must be of type `str`')

        self._host = host
        self._successful = False
        self._number = number
        self._success_count = 0

        pings = [Ping(host) for i in range(number)]

        for result in [p.succeeded for p in pings]:
            if result is True:
                self._success_count += 1

        if self._success_count >= success:
            self._successful = True
            return

    successful = property(lambda s: s._successful)
    number = property(lambda s: s._number)
    success_count = property(lambda s: s._success_count)
    report = property(lambda s: s._report())

    def _report(self) -> str:
        """
        Return a report on the success or failure of this PingBatch
        """
        if self.successful is False:
            return 'Ping batch failed, host: ' + self._host

        report = 'Ping batch to {host} succeeded, {success}/{number}'
        return report.format(
            host=self._host,
            success=str(self._success_count),
            number=str(self._number)
        )


if __name__ == '__main__':
    batch = PingBatch('google.com')
    print(batch.report)
