yamcs parameter-archive
=======================

.. program:: yamcs parameter-archive

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs parameter-archive** rebuild <*START*> <*STOP*>


Description
-----------

Manipulate the Parameter Archive.


Commands
--------

.. describe:: rebuild

    Rebuild the Parameter Archive

    The rebuild must be constrained by using the ``START`` and ``STOP`` options. These values are only hints to the Parameter Archive, which will extend the requested range based on archive segmentation.

    Rebuild run as an asynchronous operation: this command will not await the outcome.


Options
-------

.. option:: <START>

    Date specification in ISO format or as detailed under `Timestamps`_.

.. option:: <STOP>

    Date specification in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

When parsing timestamps, yamcs-cli accepts a specification in ISO format. The following special patterns are also recognised:

* ``now``: current time
* ``now UTC``: current UTC time
* ``today``: 00:00:00 of the current day
* ``today UTC``: 00:00:00 UTC of the current day
* ``yesterday``: 00:00:00 of the day before
* ``yesterday UTC``: 00:00:00 UTC of the day before
* ``tomorrow``: 00:00:00 of the next day
* ``tomorrow UTC``: 00:00:00 UTC of the next day
