yamcs parameter-archive
=======================

.. program:: yamcs parameter-archive

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs parameter-archive** rebuild [-s <*DATE*>, --since <*DATE*>]
    |   [-u <*DATE*>, --until <*DATE*>]
    | **yamcs parameter-archive** purge
    | **yamcs parameter-archive** backfilling enable
    | **yamcs parameter-archive** backfilling disable


Description
-----------

Manage the Parameter Archive.


Commands
--------

.. describe:: rebuild

    Rebuild the Parameter Archive.

    This operation may be constrained by using the ``--since`` and ``--until`` options. These values are only hints to the Parameter Archive, which will extend the requested range based on archive segmentation.

    Rebuild run as an asynchronous operation: this command will not await the outcome.


.. describe:: purge

    Remove all data from the Parameter Archive


.. describe:: backfilling

   Enable or disable backfilling in the Parameter Archive


Options
-------

.. option:: -s <DATE>, --since <DATE>

    With ``rebuild``, date specification in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    With ``rebuild``, date specification in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

.. include:: _includes/timestamps.rst
