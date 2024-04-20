yamcs login
===========

.. program:: yamcs login

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs login** [-u <*USERNAME*>, --username <*USERNAME*>]
    |   [--instance <*INSTANCE*>] [<*URL*>]


Description
-----------

Login to a Yamcs server.


Options
-------

.. option:: <URL>

    The server URL. Example: ``http://localhost:8090``

.. option:: -u <USERNAME>, --username <USERNAME>

    Username

.. option:: --instance <INSTANCE>

    Initial instance.

    This defaults to the first available instance on the
    target Yamcs server.


Environment
-----------

``YAMCS_CLI_PASSWORD``
    Provide a password instead of prompting for input.
