yamcs parameter-archive
=======================

.. program:: yamcs parameter-archive

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs parameter-archive** rebuild <*START*> <*STOP*>
    | **yamcs parameter-archive** purge


Description
-----------

Manipulate the Parameter Archive.


Commands
--------

.. describe:: rebuild

    Rebuild the Parameter Archive.

    This operation must be constrained by using the ``START`` and ``STOP`` options. These values are only hints to the Parameter Archive, which will extend the requested range based on archive segmentation.

    Rebuild run as an asynchronous operation: this command will not await the outcome.


.. describe:: purge

    Remove all data from the Parameter Archive

Options
-------

.. option:: <START>

    With ``rebuild``, date specification in ISO format or as detailed under `Timestamps`_.

.. option:: <STOP>

    With ``rebuild``, date specification in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

.. include:: _includes/timestamps.rst
