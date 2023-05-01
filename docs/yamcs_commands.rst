yamcs commands
==============

.. program:: yamcs commands

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs commands** list
    | **yamcs commands** describe <*COMMAND*>
    | **yamcs commands** run [--processor <*PROCESSOR*>] [--dry-run]
    |   [--sequence-number <*SEQNO*>] [--arg-file <*FILE*>]
    |   [--arg <*KEY=VALUE*> [<*KEY=VALUE*> ...]]
    |   <*COMMAND*>
    | **yamcs commands** log [-n <*LINES*>, --lines <*LINES*>]
    |   [-s <*DATE*>, --since <*DATE*>] [-u <*DATE*>, --until <*DATE*>]

Description
-----------

Manage commands.


Commands
--------

.. describe:: list

    List commands

.. describe:: describe <COMMAND>

    Describe a command

.. describe:: run <COMMAND>

    Run a command

.. describe:: log [-n <LINES>, --lines <LINES>] [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>]

    Read command log


Options
-------

.. option:: --processor <PROCESSOR>

    With ``run``, specifies the name of the target processor.

    Default is ``realtime``.

.. option:: --dry-run

    With ``run``, validate the command, but do not queue it.

.. option:: --arg-file <FILE>

    With ``run``, read command arguments from a file

.. option:: --arg <KEY=VALUE> [KEY=VALUE ...]

    With ``run``, set command arguments.

.. option:: --sequence-number <SEQNO>

    With ``run``, set the sequence number of this command. This is used to determine unicity of commands at the same time and coming from the same origin. If not set Yamcs will automatically assign a sequential number as if every submitted command is unique.

.. option:: -n <LINES>, --lines <LINES>

    With ``log``, specify the number of commands to show, or ``all`` to show all.

    Default: 10, but only when ``--since`` and ``--until`` are unset.

.. option:: -s <DATE>, --since <DATE>

    With ``log``, include commands not older than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    With ``log``, include commands not newer than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

.. include:: _includes/timestamps.rst
