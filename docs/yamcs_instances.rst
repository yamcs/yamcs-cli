yamcs instances
===============

.. program:: yamcs instances

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs instances** list [--format <*FORMAT*>]
    | **yamcs instances** start <*INSTANCE*>...
    | **yamcs instances** stop <*INSTANCE*>...


Description
-----------

Read Yamcs instances.


Commands
--------

.. describe:: list [--format <FORMAT>]

    List instances

.. describe:: start <INSTANCE>...

    Start an instance

.. describe:: stop <INSTANCE>...

    Stop an instance


Options
-------

.. option:: --format <FORMAT>

    For subcommands that support it, set the output format to:

    ``table``
        Print a human-friendly table
    ``json``
        Print in JSON format
