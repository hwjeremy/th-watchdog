"""
Thornleigh Farm - VPN Watchdog
Email Module
author: hugh@blinkybeach.com
"""
from th_watchdog.emailstate import EmailState
import boto3
from watchdog_config import AWS_SECRET_KEY
from watchdog_config import AWS_ACCESS_KEY
from watchdog_config import ADMIN_ADDRESS

SES_CLIENT = boto3.client(
    service_name='ses',
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_access_key_id=AWS_ACCESS_KEY,
    region_name='us-west-2'
)


class Email:
    """
    An email notifying the administrator of a VPN state
    """
    def __init__(self, subject: str, body: str) -> None:
        self._state = EmailState.UNSENT
        if not isinstance(subject, str):
            raise TypeError('subject must be of type `str`')
        if not isinstance(body, str):
            raise TypeError('body must be of type `str`')
        self._send(subject, body)
        return

    state = property(lambda s: s._state)

    def _send(self, subject: str, content: str) -> None:
        """
        Transmit the email message. If successful, set state to sent.
        """
        SES_CLIENT.send_email(
            Source='Thornleigh Farm System <system@thornleighfarm.com>',
            Destination={
                'ToAddresses': [
                    ADMIN_ADDRESS
                ],
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': content
                    }
                }
            }
        )
        self._state = EmailState.SENT
        return
