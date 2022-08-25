yamcs storage
=============

.. program:: yamcs storage

Synopsis
--------

**yamcs storage ls** [-l] [-r, -R] [<*BUCKET*>]

**yamcs storage mb** <*BUCKET*>...

**yamcs storage rb** <*BUCKET*>...

**yamcs storage cat** <*OBJECT*>...

**yamcs storage cp** <*SRC*> <*DST*>

**yamcs storage mv** <*SRC*> <*DST*>

**yamcs storage rm** <*OBJECT*>...


Description
-----------

Manage object storage.


Commands
--------

ls [-l] [-r, -R] [<BUCKET>]
    | List buckets or objects
    | Synonym: ``list``

mb <BUCKET>...
    Make buckets

rb <BUCKET>...
    Remove buckets

cat <OBJECT>...
    Concatenate object content to stdout

cp <SRC> <DST>
    Copy a file or object

mv <SRC> <DST>
    Move a file or object

rm <OBJECT>...
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
