# module: importer.py
#
# save files


import subprocess
from micronux import converter, midi


newSettings = {}
convert_cache = './programs/cache/convert.txt'


# Keep track of settings that changed
def setting_changed(ui):
    widget = ui.app.focusWidget()
    # workaround for radiobuttons
    if 'waveform' in widget.objectName():
        wave = widget.objectName()
        if '1' in wave:
            widget = ui.win.osc_1_waveform
        elif '2' in wave:
            widget = ui.win.osc_2_waveform
        elif '3' in wave:
            widget = ui.win.osc_3_waveform

    if not widget in newSettings:
        newSettings.update({widget.objectName(): widget})

        auto_send = ui.win.ctrl_auto_send.isChecked()
        if auto_send and midi.send_ready:
            midi.send_ready = False
            save_file(midi.send_cache, ui.settings_list, ui.allSettings)
            port = ui.win.ctrl_midi_port.currentText()
            if midi.interface('send', port):
                midi.send_ready = True

    ui.win.ctrl_revert.setEnabled(True)


def clear_changes(ui):
    newSettings.clear()
    ui.win.ctrl_revert.setEnabled(False)


def revert_changes(ui, settings_list, allSettings):
    clear_changes(ui)
    ui.map_widgets(settings_list, allSettings)
    ui.lcd_message('revert')


def export_line(widget, allSettings):
    setting = allSettings[widget.objectName()]
    if hasattr(widget, 'value'):
        new_value = widget.value()
    elif hasattr(widget, 'currentText'):
        new_value = widget.currentText()
    elif hasattr(widget, 'checkedButton'):
        new_value = widget
    elif hasattr(widget, 'checkState'):
        new_value = widget
    else:
        new_value = 'nope'
    line = setting.name+': '
    line += str(setting.format_val(new_value))
    return line


def build_txt_file(settings_list, allSettings):
    txt_file = '# Micron Program File\n'
    txt_file += '# generated by Micronux\n\n'
    for setting in settings_list:
        if setting in newSettings:
            line = export_line(newSettings[setting], allSettings)
            txt_file += line+'\n'
        else:
            line = allSettings[setting].name+': '
            line += allSettings[setting].value
            txt_file += line+'\n'
    return txt_file


def save_file(file_path, settings_list, allSettings):
    txt = build_txt_file(settings_list, allSettings)
    if file_path.endswith('.txt'):
        fname = file_path
    elif file_path.endswith('.syx'):
        fname = convert_cache
    else:
        return False

    txt_file = open(fname, 'w')
    txt_file.write(txt)
    txt_file.close()

    if file_path.endswith('.syx'):
        if converter.ipd(convert_cache):
            cache_syx = convert_cache[:-3]+'syx'
            subprocess.run(['mv', cache_syx, file_path])
        else:
            return False
    return True
