yamcs rocksdb
=============

.. program:: yamcs rocksdb

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs rocksdb** tablespaces
    | **yamcs rocksdb** compact [--dbpath <*DBPATH*>] <*TABLESPACE*> <*CF*>


Description
-----------

Manage RocksDB storage engine.


Commands
--------

.. describe:: tablespaces

    List processors

.. describe:: compact [--dbpath <DBPATH>] <TABLESPACE> <CF>

    Delete a processor


Options
-------

.. option:: --dbpath <DBPATH>

    With ``compact``, specify a path within the tablespace. Leave unspecified for the root database.
