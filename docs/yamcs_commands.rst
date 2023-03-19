yamcs commands
==============

.. program:: yamcs commands

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs commands** list
    | **yamcs commands** describe <*COMMAND*>
    | **yamcs commands** run [--processor <*PROCESSOR*>] [--dry-run]
       [--arg-file <*FILE*>] [--arg <*KEY=VALUE*> [<*KEY=VALUE*> ...]]
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
