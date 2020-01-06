# Micronux

**Micronux** will be a graphical editor for Linux to edit programs from the Alesis Micron synthesiser.  
It is just meant as a front end to edit for the text files generated by Alesis' program decoder/encoder perl script, and doesn't work in real time (but eventually should get really close).

### Work in progress

Micronux is in early days development and doesn't do anything useful right now. For something that actually works on GNU/Linux, see the simple (yet smart) perl script by ralphgonz [here](https://sites.google.com/site/ralphgonz/music-micron).


![screenshot of micronux](docs/screenshot.jpg)


### [To Do List](docs/TODO.md)


### Usage

You'll need python3, PySide2 and make the script executable. You'll also need amidi to receive and send sysex.

    sudo apt install amidi python3-pip
    pip3 install PySide2
    chmod +x micronux.py
    ./micronux.py

*Micronux* reads the `default.txt` file in the `prog` folder.    
**For now**, to open a different text or sysex file, you can specify its path on the command line:

    ./micronux.py mysysex.syx

And you can receive a sysex from the Micron with the option `-r` followed by the MIDI port address (as listed by `amidi -l`):

    ./micronux.py -r <midi_port>


### About

*Micronux* is written in **Python 3** and uses the **PySide2** bindings for its **QT** graphical interface, which is built using **QT Designer**. It will use **amidi** to send/receive sysex programs through midi.

The user interface is inspired by the physical layout of the Ion synthesiser as well as existing Mac/Windows editors. Since the amount of controls and settings of the Micron can be overwhelming, the goal is to simplify and promote the more commonly used settings.

Additionally, one goal is to keep Micronux functional on a netbook screen, so limited to a size of 1024x600 pixels. The use of tabs and pop-up windows should eventually give access to all the settings.
