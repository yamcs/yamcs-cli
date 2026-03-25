yamcs parameters
================

.. program:: yamcs parameters

Description
-----------

.. rst-class:: synopsis

    | **yamcs parameters** list [--format <*FORMAT*>]
    | **yamcs parameters** describe <*PARAMETER*>
    | **yamcs parameters** get [--next [--timeout <*TIMEOUT*>]] <*PARAMETER*>
    | **yamcs parameters** set [--date <*DATE*>] <*PARAMETER*> <*VALUE*>
    | **yamcs parameters** export-csv [--interval <*INTERVAL*>]
    |   [-s <*DATE*>, --since <*DATE*>] [-u <*DATE*>, --until <*DATE*>] <*PARAMETER*>


Desription
----------

Manage parameters.


Commands
--------

.. describe:: list [--format <FORMAT>]

    List parameters

.. describe:: describe <PARAMETER>

    Describe a parameter

.. describe:: get <PARAMETER>

    Get a parameter's value

.. describe:: set <PARAMETER> <VALUE>

    Set a parameter's value (unless this is a readonly parameter).

.. describe:: export-csv <PARAMETER>

    Export parameter values in CSV format


Options
-------

.. option:: --processor <PROCESSOR>

    With ``get`` and ``set``, specifies the name of the target processor.

    Default is ``realtime``.

.. option:: --next

    With ``get``, wait for the next parameter value to be processed by Yamcs.

    If not set, the latest received value is returned.

.. option:: --timeout <TIMEOUT>

    With ``get``, this indicates the maximum time to wait for a new value if the ``next`` option is used.

.. option:: --date <DATE>

    Value time. If unspecified, defaults to mission time.

    .. include:: _includes/timestamps.rst

.. option:: --interval <INTERVAL>

    With ``export-csv``, limit values to max one per interval (in seconds).

.. option:: -s <DATE>, --since <DATE>

    With ``export-csv``, include values not older than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    With ``export-csv``, include values not newer than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: --format <FORMAT>

    For subcommands that support it, set the output format to:

    ``table``
        Print a human-friendly table
    ``json``
        Print in JSON format


Timestamps
----------

.. include:: _includes/timestamps.rst
