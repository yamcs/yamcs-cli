yamcs tables
============

.. program:: yamcs tables

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs tables** list
    | **yamcs tables** describe <*TABLE*>
    | **yamcs tables** dump [-d <*DIR*>, --dir <*DIR*>] [--gzip]
    |   [-q <*QUERY*>, --query <*QUERY*> ] [--query-file <*FILE*>]
    |   <*TABLE*>...
    | **yamcs tables** load [-d <*DIR*>, --dir <*DIR*>] [--gzip] <*TABLE*>...
    | **yamcs tables** rebuild-histogram [-s <*DATE*>, --since <*DATE*>]
    |   [-u <*DATE*>, --until <*DATE*>] <*TABLE*>...


Description
-----------

Read and manipulate tables.


Commands
--------

.. describe:: list

    List tables

.. describe:: describe <TABLE>

    Describe a table

.. describe:: dump [-d <DIR>, --dir <DIR>] [-q <QUERY>, --query <QUERY>] [--query-file FILE] [--gzip] <TABLE>...

    Dump table data

.. describe:: load [-d <DIR>, --dir <DIR>] [--gzip] <TABLE>...

    Load data into a table

.. describe:: rebuild-histogram [-s <DATE>, --since <DATE>] [-u <DATE>, --until <DATE>] <TABLE>...

    Rebuilds the histogram for a table. This may be necessary for example after bulk loading data.


Options
-------

.. option:: -d <DIR>, --dir <DIR>

    Specifies the directory where to locate dump files. Defaults to current directory.

.. option:: --gzip

    With ``dump``, compress the output.

    With ``load``, decompress the dump.

.. option:: -q <QUERY>, --query <QUERY>

    With ``dump``, provide a SQL WHERE search condition to limit the rows included in the output.

.. option:: --query-file <FILE>

    With ``dump``, specify the path to a file containing a SQL WHERE search condition to limit the rows included in the output.

.. option:: -s <DATE>, --since <DATE>

    With ``rebuild-histogram``, include records not older than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.

.. option:: -u <DATE>, --until <DATE>

    With ``rebuild-histogram``, include records not newer than the specified date.

    The date should be specified in ISO format or as detailed under `Timestamps`_.


Timestamps
----------

.. include:: _includes/timestamps.rst
