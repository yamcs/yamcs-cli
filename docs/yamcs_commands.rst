yamcs commands
==============

.. program:: yamcs commands

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs commands** list
    | **yamcs commands** describe <*COMMAND*>
    | **yamcs commands** run [--processor <*PROCESSOR*>] [--dry-run]
       [--sequence-number <*SEQNO*>] [--arg-file <*FILE*>]
       [--arg <*KEY=VALUE*> [<*KEY=VALUE*> ...]]
       <*COMMAND*>

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
