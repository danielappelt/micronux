# Micronux (Beta)

**Micronux** is an editor for Linux to edit programs from the Alesis Micron synthesiser.  
It is just a front end to edit the text files generated by Alesis' program decoder/encoder perl script, and doesn't work in real time (but almost). It's still only a beta and needs testing (see *notes*). Please post bug reports and feature requests on the *Issues* page.


![screenshot of micronux](docs/screenshot.jpg)


### Features

  - Receive and send program sysex messages from any available MIDI port.

  - Edit all program settings, including voice, oscillators, envelopes, filters, mixers, effects, modulation routing, tracking generator and assign xyz knobs.

  - Open and save `.syx` or `.txt` Micron program files.

  - Automatically send program sysex on setting change.


### Notes

  - **Warning:** After receiving a program from the Micron, **save a backup copy** before pressing 'send' or enabling 'auto-send', as these options will **overwrite** the program on the Micron.

  - All changes made on the Micron with xyz knobs, slider, etc... are **not** updated in Micronux and discarded the next time you send from Micronux (or make any edits when *auto-send* is enabled).

  - Check [to do list](docs/TODO.md) and [issues](https://github.com/bergamote/micronux/issues) for planned features and bugs.


### Install


You're gonna need python3, PySide2 and pyrtmidi. In a terminal type the following:

    sudo apt install python3-pip libasound2-dev
    pip3 install PySide2 wheel rtmidi

Then simply run `./micronux.py` from micronux's folder, or make a launcher shortcut with:

    python3 ./micronux.py --create-launcher

Update to the latest version with `git pull`.


### Usage

To receive a sysex connect your MIDI in and out cables, make sure that the right MIDI port is selected then click `receive`. On the Micron bring up the `Send MIDI sysex?` option and press down the control knob.

Pressing `send` (or enabling 'auto-send' by ticking the checkbox next to it) will **overwrite** the program with the same name on the Micron.

To create a new program, click on the program's name (top line of the green area) and give it a unique name.

The `revert` button *should* revert the changes made since the last open, save or receive (whichever came last). In case of problem, the last received program is automatically backed up in the `programs/cache` folder.


### About

*Micronux* is written in **Python 3** and uses the **PySide2** bindings for its **QT** graphical interface, which is built using **QT Designer**. It uses **rtmidi** to send/receive sysex programs through MIDI.

The user interface is inspired by the physical layout of the Ion synthesiser as well as existing Mac/Windows editors. Since the amount of controls and settings of the Micron can be overwhelming, the goal is to simplify and promote the more commonly used settings.

Additionally, one goal is to keep Micronux functional on a netbook screen, so limited to a size of 1024x600 pixels.
