yamcs tables
============

.. program:: yamcs tables

Synopsis
--------

**yamcs tables list**

**yamcs tables describe** <*TABLE*>

**yamcs tables dump** [-d <*DIR*>, --dir <*DIR*>] [--gzip] <*TABLE*>...

**yamcs tables load** [-d <*DIR*>, --dir <*DIR*>] [--gzip] <*TABLE*>...


Description
-----------

Read and manipulate tables.


Commands
--------

list
    List tables

describe <TABLE>
    Describe a table

dump [-d <DIR>, --dir <DIR>] [--gzip] <TABLE>...
    Dump table data

load [-d <DIR>, --dir <DIR>] [--gzip] <TABLE>...
    Load data into a table


Options
-------

.. option:: -d DIR, --dir DIR

    Specifies the directory where to locate dump files. Defaults to current directory.

.. option:: --gzip

    With ``dump``, compress the output.

    With ``load``, decompress the dump.

