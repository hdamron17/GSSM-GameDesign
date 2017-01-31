Hunter Damron's Footsteps
=========================

Description
-----------

This is a digitalized version of the old game Footsteps. 
It is written using Python Curses using ASCII art for the graphics. 
Below is a description of the installation instructions and a guide to the intended gameplay.

HOWTO
-----

INSTALL
~~~~~~~

To install, run ``python setup.py sdist`` to create a tarbell file then run ``pip install dist/Footsteps-X.Y.Z.tar.gz``.
This will add the command ``footsteps`` to your path variable.
This software will be available on pypi.org soon which can be installed with simply ```pip install Footsteps```.
This software was written and tested on a Ubuntu machine, so there are no guarantees about its functionality on Windows or Mac.

GAMEPLAY
~~~~~~~~

The game begins with a brief overview of the game rules. 
Each player aims to move the coin to the farthest square on their side.
On each round, each player bets a certain amount of energy from their starting supply.
(This implementation assumes 7 squares and 50 initial energy points, but it is easily changed in the script)
The coin moves one square in the direction of the player which bet the most money but both lose their energy points.
The left player adds and subtracts energy with the keys 'w' and 's' respectively then locks in their answer with the 'd' key.
The right player adds and subtracts energy with the keys 'o' and 'l' respectively then locks in their answer with the 'k' key.
This rendition of the rules are provided by Niel Bowers in Leeds, England.

TITLE: Footsteps

AUTHOR: Hunter Damron

DATE DUE: Tuesday, January 31, 2017

DATE SUBMITTED: Tuesday, January 31, 2017

COURSE TITLE: Game Design

MEETING TIMES: 10:30-12:00 Tuesday, Thursday

HONOR CODE: On my honor, I have neither given nor received unauthorized help on this assignment. Signed Hunter Damron.

INPUT FILE: N/A

OUTPUT FILE: N/A

TUTORS: N/A

COMMENTS
--------
I did not realize we had freedom to make our own game so I copied the assignment
game rules and format almost exactly. 

BIBLIOGRAPHY
------------
http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html

https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

https://packaging.python.org/distributing/

https://docs.python.org/2/distutils/setupscript.html

RESOURCES
---------
Neil Bowers's rendition of Footsteps, Leeds, England, 1992
