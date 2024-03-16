yamcs packets
=============

.. program:: yamcs packets

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs packets** log [-p <*PACKET*>, --packet <*PACKET*>]
    |   [-n <*LINES*>, --lines <*LINES*>] [-s <*DATE*>, --since <*DATE*>]
    |   [-u <*DATE*>, --until <*DATE*>]
    | **yamcs packets** rebuild-histogram [-s <*DATE*>, --since <*DATE*>]
    |   [-u <*DATE*>, --until <*DATE*>]
    | **yamcs packets** rebuild-ccsds-index [-s <*DATE*>, --since <*DATE*>]
    |   [-u <*DATE*>, --until <*DATE*>]

Description
-----------

Read packets.


Commands
--------

.. describe:: log [-p <PACKET> --packet <PACKET>] [-n <LINES>, --lines <LINES>] [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>]

    Read packet log

.. describe:: rebuild-histogram [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>]

    Rebuilds the packet histogram. This may be necessary for example after bulk loading data.

.. describe:: rebuild-ccsds-index [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>]

    Rebuilds the CCSDS index. This may be necessary for example after bulk loading data.

    This method is only applicable when a ``CcsdsTmIndex`` service is used to calculate completeness.


Options
-------

.. option:: -p <PACKET>, --packet <PACKETS>

    With ``log``, filter by packet name.

.. option:: -n <LINES>, --lines <LINES>

    With ``log``, specify the number of packets to show, or ``all`` to show all.

    Default: 10, but only when ``--since`` and ``--until`` are unset.

.. option:: -s <DATE>, --since <DATE>

    Include packets not older than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    Include packets not newer than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

.. include:: _includes/timestamps.rst
