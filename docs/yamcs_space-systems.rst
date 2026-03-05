yamcs space-systems
===================

.. program:: yamcs space-systems

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs space-systems** list
    | **yamcs space-systems** describe <*SPACESYSTEM*>
    | **yamcs space-systems** export [--xtce-version <*VERSION*>] <*SPACESYSTEM*>


Description
-----------

Read space systems.


Commands
--------

.. describe:: list

    List space systems

.. describe:: describe <SPACESYSTEM>

    Describe a space system

.. describe:: export <SPACESYSTEM>

    Export an XTCE representation of a space system


Options
-------

.. option:: --xtce-version <VERSION>

    XTCE version. One of ``1.2`` or ``1.3``.

    Default is ``1.2``
