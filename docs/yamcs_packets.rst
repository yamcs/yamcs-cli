yamcs packets
=============

.. program:: yamcs packets

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs packets** log [-p <*PACKET*>, --packet <*PACKET*>]
       [-n <*LINES*>, --lines <*LINES*>] [-s <*DATE*>, --since <*DATE*>]
       [-u <*DATE*>, --until <*DATE*>]

Description
-----------

Read packets.


Commands
--------

.. describe:: log [-p <PACKET> --packet <PACKET>] [-n <LINES>, --lines <LINES>] [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>]

    Read packet log


Options
-------

.. option:: -p <PACKET>, --packet <PACKETS>

    With ``log``, filter by packet name.

.. option:: -n <LINES>, --lines <LINES>

    With ``log``, specify the number of packets to show, or ``all`` to show all.

    Default: 10, but only when ``--since`` and ``--until`` are unset.

.. option:: -s <DATE>, --since <DATE>

    With ``log``, include packets not older than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    With ``log``, include packets not newer than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.
