yamcs parameters
================

.. program:: yamcs parameters

Description
-----------

.. rst-class:: synopsis

    | **yamcs parameters** list
    | **yamcs parameters** describe <*PARAMETER*>
    | **yamcs parameters** get [--date <*DATE*>] <*PARAMETER*>
    | **yamcs parameters** set [--next [--timeout <*TIMEOUT*>]] <*PARAMETER*> <*VALUE*>


Desription
----------

Manage parameters.


Commands
--------

.. describe:: list

    List parameters

.. describe:: describe <PARAMETER>

    Describe a parameter

.. describe:: get <PARAMETER>

    Get a parameter's value

.. describe:: set <PARAMETER> <VALUE>

    Set a parameter's value (if this parameter is not readonly).


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
