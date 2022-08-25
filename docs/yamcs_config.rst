yamcs config
============

.. program:: yamcs config

Synopsis
--------

**yamcs config get** <*PROPERTY*>

**yamcs config list**

**yamcs config set** <*PROPERTY*> <*VALUE*>

**yamcs config unset** <*PROPERTY*>


Description
-----------

Manage Yamcs CLI properties.


Commands
--------

get <PROPERTY>
    Get value of CLI property

list
    List CLI properties

set <PROPERTY> <VALUE>
    Set CLI property

unset <PROPERTY>
    Unset CLI property


Configuration File
------------------

Configuration properties are stored to the file ``$HOME/.config/yamcs-cli/config`` and divided in sections. Properties affect the commands' behavior.

Currently all supported properties belong to the ``core`` section only.

Example
~~~~~~~

code-block:: properties

    [core]
    url = http://localhost:8090
    instance = simulator

Properties
~~~~~~~~~~

url
    Yamcs Server URL

instance
    Yamcs instance name
