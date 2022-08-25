yamcs tables
============

.. program:: yamcs tables

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs tables** list
    | **yamcs tables** describe <*TABLE*>
    | **yamcs tables** dump [-d <*DIR*>, --dir <*DIR*>] [--gzip] <*TABLE*>...
    | **yamcs tables** load [-d <*DIR*>, --dir <*DIR*>] [--gzip] <*TABLE*>...


Description
-----------

Read and manipulate tables.


Commands
--------

.. describe:: list

    List tables

.. describe:: describe <TABLE>

    Describe a table

.. describe:: dump [-d <DIR>, --dir <DIR>] [--gzip] <TABLE>...

    Dump table data

.. describe:: load [-d <DIR>, --dir <DIR>] [--gzip] <TABLE>...

    Load data into a table


Options
-------

.. option:: -d DIR, --dir DIR

    Specifies the directory where to locate dump files. Defaults to current directory.

.. option:: --gzip

    With ``dump``, compress the output.

    With ``load``, decompress the dump.

