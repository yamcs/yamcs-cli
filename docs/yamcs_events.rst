yamcs events
============

.. program:: yamcs events

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs events** create [-m <*MESSAGE*>, --message <*MESSAGE*>] [--date <*DATE*>]
    |   [--sequence-number <*SEQNO*>] [--severity <*LEVEL*>] [--source <*SOURCE*>]
    |   [--type <*TYPE*>] [--extra <*KEY=VALUE*> [<*KEY=VALUE*> ...]]
    | **yamcs events** log [-n <*LINES*>, --lines <*LINES*>]
    |   [-s <*DATE*>, --since <*DATE*>] [-u <*DATE*>, --until <*DATE*>]

Description
-----------

Add events to the Yamcs event log.


Commands
--------

.. describe:: create

    Create an event. This command shows an editor where you can enter the event message. Alternatively you can specify the message using the ``--message`` option.

.. describe:: log [-n <LINES>, --lines <LINES>] [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>]

    Read event log


Options
-------

.. option:: -m <MESSAGE>, --message <MESSAGE>

    Event message. 

.. option:: --date <DATE>

    Event time. If unspecified, defaults to mission time.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: --sequence-number <SEQNO>

    Sequence number of this event. This is used to determine unicity of events
    at the same time and coming from the same source. If not set Yamcs will
    automatically assign a sequential number as if every submitted event is unique.

.. option:: --severity <LEVEL>

    The severity level of the event. One of ``info``, ``watch``, ``warning``, ``distress``, ``critical`` or ``severe``.
    Default is ``info``.

.. option:: --source <SOURCE>

    Source of the event. Defaults to ``User`` if unset.

.. option:: --type <TYPE>

    Type of the event.

.. option:: --extra <KEY=VALUE> [KEY=VALUE ...]

    Set additional event properties.

.. option:: -n <LINES>, --lines <LINES>

    With ``log``, specify the number of events to show, or ``all`` to show all.

    Default: 10, but only when ``--since`` and ``--until`` are unset.

.. option:: -s <DATE>, --since <DATE>

    With ``log``, include events not older than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    With ``log``, include events not newer than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

.. include:: _includes/timestamps.rst
