yamcs dbshell
=============

.. program:: yamcs dbshell

Synopsis
--------

.. rst-class:: synopsis

    | **yamcs dbshell** [*OPTIONS*]


Description
-----------

Launch Yamcs DB Shell.


Options
-------

.. option:: -c <COMMAND>, --command <COMMAND>

    Run a single SQL command string.

.. option:: -N, --skip-column-names

    Don't print column names.


DB Shell Commands
-----------------

The shell sends each SQL statement that you issue to Yamcs. There is also a set of commands that are interpreted by dbshell itself. For a list of these, type help or \h at the shell prompt:

.. code-block:: text

    simulator> help

    List of dbshell commands:
    ?          (\?) Show help.
    delimiter  (\d) Set statement delimiter.
    edit       (\e) Edit a command with $EDITOR.
    exit       (\q) Synonym for quit.
    help       (\h) Display this help.
    nopager    (\n) Disable pager. Results are printed to stdout.
    pager      (\P) Print results to a pager.
    quit       (\q) Quits the DB Shell.
    rehash     (\#) Rebuild completion hash.
    source     (\.) Execute an SQL script file, provided as argument.
    status     (\s) Print status information.
    system     (\!) Execute a system command.
    use        (\u) Use another instance, provided as argument.

.. describe:: help [<COMMAND>], \h [<COMMAND>], ? [<COMMAND>], \? [<COMMAND>]

    Display a help message listing all available commands.

    If you provide an argument, the help message for that specific command is shown.

.. describe:: delimiter <STRING>, \d <STRING>

    Change the string that separates SQL statements. Default is the semicolon character: ``;``.

.. describe:: edit, \e

    Open an editor for entering the next SQL statement. This uses the editor indicated by the ``$EDITOR`` environment variable.

.. describe:: nopager, \n

    Disable result paging. It is disabled by default.

.. describe:: pager, \P

    Enable result paging. It is disabled by default.

.. describe:: quit, \q

    Quits the DB Shell.

.. describe:: rehash, \#

    Reload database objects, used for completion.

.. describe:: source <FILENAME>, \. <FILENAME>

    Run statements from the provided file.

.. describe:: status, \s

    Print information on the current state.

.. describe:: system <COMMAND>, \! <COMMAND>

    Execute a local command in a subshell.

.. describe:: use <INSTANCE>, \u <INSTANCE>

    Switch the prompt to another instance.
