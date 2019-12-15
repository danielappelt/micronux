# File: micronux.py
# A Python/QT setting editor for the Micron synth

import sys
from micronux import gui, textfile, mapwidgets, lcd

debug = True

# setup app and window
myQtGui = gui.make_gui('micronux/micronux.ui', 'Micronux', 'fusion')
app = myQtGui['app']
window = myQtGui['window']

# import settings text file
settings = textfile.import_file('test.txt')

# set values to widgets
mapwidgets.mapping(settings, app, window)

# function to pass slider value to lcd
def pass_to_lcd():
    global app
    global window
    global settings
    lcd.update(app, window, settings)

# Fix focus policy of sliders
# and connect them to LCD display.
for widget in app.allWidgets():
    widg_type = type(widget).__name__
    if (widg_type == 'QDial') or (widg_type == 'QSlider'):
        widget.setFocusPolicy(gui.Qt.FocusPolicy.WheelFocus)
        widget.valueChanged.connect(pass_to_lcd)

sys.exit(app.exec_())
