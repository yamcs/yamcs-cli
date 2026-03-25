yamcs links
===========

.. program:: yamcs links

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs links** list [--format <*FORMAT*>]
    | **yamcs links** enable <*LINK*>...
    | **yamcs links** disable <*LINK*>...
    | **yamcs links** describe <*LINK*>
    | **yamcs links** run-action <*LINK*> <*ACTION*>


Description
-----------

Read and manipulate data links.


Commands
--------

.. describe:: list [--format <FORMAT>]

    List links

.. describe:: enable

    Enable a link

.. describe:: disable

    Disable a link

.. describe:: describe

    Describe a link

.. describe:: run-action

    Run a custom action


Options
-------

.. option:: --format <FORMAT>

    For subcommands that support it, set the output format to:

    ``table``
        Print a human-friendly table
    ``json``
        Print in JSON format
