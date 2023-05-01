yamcs alarms
============

.. program:: yamcs alarms

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs alarms** list [--processor <*PROCESSOR*>]
    | **yamcs alarms** acknowledge [--processor <*PROCESSOR*>]
    |    [-c <*COMMENT*>, --comment <*COMMENT*>] <*ALARM*> <*SEQNO*>
    | **yamcs alarms** shelve [--processor <*PROCESSOR*>]
    |   [-c <*COMMENT*>, --comment <*COMMENT*>] <*ALARM*> <*SEQNO*>
    | **yamcs alarms** unshelve [--processor <*PROCESSOR*>]
    |   [-c <*COMMENT*>, --comment <*COMMENT*>] <*ALARM*> <*SEQNO*>
    | **yamcs alarms** clear [--processor <*PROCESSOR*>]
    |   [-c <*COMMENT*>, --comment <*COMMENT*>] <*ALARM*> <*SEQNO*>
    | **yamcs alarms** log [-n <*LINES*>, --lines <*LINES*>]
    |   [-s <*DATE*>, --since <*DATE*>] [-u <*DATE*>, --until <*DATE*>]


Description
-----------

Manage alarms.


Commands
--------

.. describe:: list [--processor <PROCESSOR>]

    Show active alarms

.. describe:: acknowledge [--processor <PROCESSOR>] [-c <COMMENT>, --comment <COMMENT>] <ALARM> <SEQNO>

    Acknowledge an alarm

.. describe:: shelve [--processor <PROCESSOR>] [-c <COMMENT>, --comment <COMMENT>] <ALARM> <SEQNO>

    Shelve an alarm

.. describe:: unshelve [--processor <PROCESSOR>] [-c <COMMENT>, --comment <COMMENT>] <ALARM> <SEQNO>

    Unshelve an alarm

.. describe:: clear [--processor <PROCESSOR>] [-c <COMMENT>, --comment <COMMENT>] <ALARM> <SEQNO>

    Clear an alarm

.. describe:: log [-n <LINES>, --lines <LINES>] [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>]

    Read alarm log


Options
-------

.. option:: --processor <PROCESSOR>

    With ``list``, ``acknowledge``, ``shelve``, ``unshelve`` or ``clear``, specify the processor.

    Default: realtime

.. option:: -c <COMMENT>, --comment <COMMENT>

    With ``list``, ``acknowledge``, ``shelve``, ``unshelve`` or ``clear``, attach a comment to the alarm change.

.. option:: <ALARM>

    With ``acknowledge``, ``shelve``, ``unshelve`` or ``clear``, specify the alarm name.

.. option:: <SEQNO>

    With ``acknowledge``, ``shelve``, ``unshelve`` or ``clear``, specify the alarm instance.

.. option:: -n <LINES>, --lines <LINES>

    With ``log``, specify the number of alarms to show, or ``all`` to show all.

    Default: 10, but only when ``--since`` and ``--until`` are unset.

.. option:: -s <DATE>, --since <DATE>

    With ``log``, include alarms not older than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    With ``log``, include alarms not newer than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

.. include:: _includes/timestamps.rst
