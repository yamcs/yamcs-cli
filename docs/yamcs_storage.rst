yamcs storage
=============

.. program:: yamcs storage

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs storage** ls [-l] [-r, -R] [<*BUCKET*>]
    | **yamcs storage** mb <*BUCKET*>...
    | **yamcs storage** rb <*BUCKET*>...
    | **yamcs storage** cat <*OBJECT*>...
    | **yamcs storage** cp <*SRC*> <*DST*>
    | **yamcs storage** mv <*SRC*> <*DST*>
    | **yamcs storage** rm <*OBJECT*>...


Description
-----------

Manage object storage.


Commands
--------

.. describe:: ls [-l] [-r, -R] [<BUCKET>]

    | List buckets or objects
    | Synonym: ``list``

.. describe:: mb <BUCKET>...

    Make buckets

.. describe:: rb <BUCKET>...

    Remove buckets

.. describe:: cat <OBJECT>...

    Concatenate object content to stdout

.. describe:: cp <SRC> <DST>

    Copy a file or object

.. describe:: mv <SRC> <DST>

    Move a file or object

.. describe:: rm <OBJECT>...

    Remove objects


Options
-------

.. option:: -l

    With ``ls``, list in long format.

.. option:: -r, -R

    With ``ls``, list recursively.

.. option:: <SRC>

    With ``cp``, local file or an object in the format ys://BUCKET/OBJECT.

.. option:: <DST>

    With ``cp``, local file, or an object in the format ys://BUCKET/OBJECT.

    With ``mv``, local file, local directory, or an object in the format ys://BUCKET/OBJECT.
