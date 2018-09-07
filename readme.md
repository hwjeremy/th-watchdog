# OpenVPN connection monitor

Thornleigh Farm Watchdog (TFW) is a python program designed to monitor a critical OpenVPN connection. The objectives of TFW are:

* Alert an administrator when an OpenVPN connection is lost
* Attempt corrective action
* Notify an administrator if the connection is restored

TFW was born out of frustration with OpenVPN's esoteric functionality for the detection and resumption of failed connections. TFW's operating environment features high rates of connection failure: UPS-overwhelming power failures and satellite connection interuptions are common on [Thornleigh Farm](https://thornleighfarm.com).

TFW is publicly released as Open Source Software under the MIT license. I don't think it is necessarily good software of software anyone else might want to use. Instead, I've open-sourced as a source of inspiration and ideas for others dealing with general connection monitoring problems.

The biggest problems with TFW are:

* Requires root permissions to run. Yuck. This is due to dependence on raw sockets for ICMP.
* Was bashed out in a couple of hours on a Friday evening, so it is a bit of a mess, with no tests or documentation.
