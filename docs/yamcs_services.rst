yamcs services
==============

.. program:: yamcs services

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs services** list [--format <*FORMAT*>]
    | **yamcs services** start <*SERVICE*>...
    | **yamcs services** stop <*SERVICE*>...


Description
-----------

Read and manipulate services.


Commands
--------

.. describe:: list [--format <FORMAT>]

    List services

.. describe:: start <SERVICE>...

    Start a service

.. describe:: stop <SERVICE>...

    Stop a service


Options
-------

.. option:: --format <FORMAT>

    For subcommands that support it, set the output format to:

    ``table``
        Print a human-friendly table
    ``json``
        Print in JSON format
