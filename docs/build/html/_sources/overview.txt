
Overview
========

SwfConduit is an AMF3 socket server written in Python using Twisted and PyAMF.
The client side uses Flash's Socket class, so it is bidirectional, not
service-oriented. This makes it ideal for interactive applications like games
and chat.

This document is for API and usage. Install instructions and tutorials can be
found on `the SwfConduit wiki
<http://github.com/doublecluepon/SwfConduit/wiki>`_.

----------
The Server
----------

The server is a Twisted factory with a custom Protocol to handle the AMF3
protocol and dispatching Events. SwfConduit maintains only a thin wrapper
around the most necessary parts, so that it can be bypassed if necessary.

The server is created using the :ref:`Loader <loader>` class, which accepts
configuration programmatically or through a config file and sets up the
appropriate Twisted listeners and factories.

The :ref:`Server <server>` and :ref:`Session <session>` classes are the
Twisted Factory and Protocol classes, respectively. You can extend these to
add your own functionality. The Loader then gets told where to find the Server
class, which knows what Session class to use.

:ref:`Events <event>` are the basic messages that pass between client and
server. Each Event encapsulates data to be acted upon. Each Event has a fire()
function that gets called when it is recieved by the server. The fire()
function is where most of the behavior will be.

----------
The Client
----------

The client API is described in the `SwfConduit client API docs
<http://doublecluepon.github.com/SwfConduit/flex/docs/>`_. For information on
using the client and server together, see `the SwfConduit wiki
<http://github.com/doublecluepon/SwfConduit/wiki>`_ for tutorials.
