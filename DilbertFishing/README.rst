Hunter Damron's ASCII Fishing inspired by Dilbert
=================================================

Description
-----------

This is a simple fishing game based on a cartoon of Dilbert "carpet fishing"
It is written using Python Curses using ASCII art for the graphics.
Below is a description of the installation instructions and a guide to the intended gameplay.

HOWTO
-----

INSTALL
~~~~~~~

To install, run ``python setup.py sdist`` to create a tarbell file then run ``pip install dist/DilbertFishing-X.Y.Z.tar.gz``.
This will add the command ``fishing`` to your path variable.
This software will be available on pypi.org soon which can be installed with simply ``pip install DilbertFishing``.
This software was written and tested on a Ubuntu machine, so there are no guarantees about its functionality on Windows or Mac.

GAMEPLAY
~~~~~~~~

The goal of the game is to catch fish. Like real fishing, there is no point value for each fish, just the joy of catching them.
Since these fish are digital, they do not have the same nutritional value, but the excitement of catching them is real
Use the arrow keys to move your 'bobber' (represented with '<>') around the 'pond'.
Fish spawn at random locations on random time intervals but occasionally it will spawn in the same location as your bobber.
When this happens, you'll be surprised by a pretty ASCII art fish.
You can change the default values (size 5, random_mean 3, and random_std_dev 1) by adding command line options.
These options are added in the form ``fishing [value name] [value]`` with any number of arguments.
Note that if arguments are repeated, the last value is used

TITLE: Dilbert Fishing

AUTHOR: Hunter Damron

DATE DUE: Thurday, Feb 9, 2017

DATE SUBMITTED: Thursday, Feb 9, 2017

COURSE TITLE: Game Design

MEETING TIMES: 10:30-12:00 Tuesday, Thursday

HONOR CODE: On my honor, I have neither given nor received unauthorized help on this assignment. Signed Hunter Damron.

INPUT FILE: N/A

OUTPUT FILE: N/A

TUTORS: N/A

RESOURCES: N/A

COMMENTS
--------

I added the bells and whistles.

BIBLIOGRAPHY
------------

# ASCII images from http://www.ascii-code.com/ascii-art/animals/fish.php - The ASCII art fish
