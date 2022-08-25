yamcs config
============

.. program:: yamcs config

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs config** get <*PROPERTY*>
    | **yamcs config** list
    | **yamcs config** set <*PROPERTY*> <*VALUE*>
    | **yamcs config** unset <*PROPERTY*>


Description
-----------

Manage Yamcs CLI properties.


Commands
--------

.. describe:: get <PROPERTY>

    Get value of CLI property

.. describe:: list

    List CLI properties

.. describe:: set <PROPERTY> <VALUE>

    Set CLI property

.. describe:: unset <PROPERTY>

    Unset CLI property


Configuration File
------------------

Configuration properties are stored to the file ``$HOME/.config/yamcs-cli/config`` and divided in sections. Properties affect the commands' behavior.

Currently all supported properties belong to the ``core`` section only.

Example
~~~~~~~

.. code-block:: ini

    [core]
    url = http://localhost:8090
    instance = simulator

Properties
~~~~~~~~~~

.. describe:: url

    Yamcs Server URL

.. describe:: instance

    Yamcs instance name
