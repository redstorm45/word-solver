# WordSolver
A solver I made as a side-project for the game of Scrabble.

I do not own the rights to the game, therefore I cannot distribute a word list for it.

The program is written in python 3, and uses the Tkinter library (pre-installed with most python distributions).

## Why ?

Most software available only permits to list the words available to you using your letters, sometimes adding one from the board. I found this limiting, and wanted something that took "solver" to the next level: give directly all the options on the board, and also provide point-counting.

Also, it is fun to design something efficient.

## Installing

 - Download python 3.7
 - Download the source from github
 - Place a `dico.txt` file next to the other files, see (#getting-a-word-list)
 - Run `main.py`

# Getting a word list

As stated before, no word list is distributed with this software.
It is however easy to get one from the internet that suits your need.

For example, a script can be used to get the French worldlist, as seen [here](https://blog.site2wouf.fr/2018/12/un-lexique-genre-ods7-en-txt.html).

The word list should have one word per line, lower or upper case, with no special characters (only the 26 letters of the alphabet).
