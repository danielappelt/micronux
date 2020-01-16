# module: trader.py
#
# Handle files generated by/for
# alesis micron/ion program decoder/encoder.
import subprocess, sys, os.path

ion_decoder_path = 'alesis/ion_program_decoder.pl'
default_prog = 'prog/default.txt'
midi_cache = 'prog/received.syx'

# convert text line to name/value pair
def text_to_setting(line):
    line = line.strip()
    if line:
        if line.startswith('#'): # remove comments
            return False
        else:
            pair = line.split(':')
            # white spaces not allowed
            name = pair[0].replace(' ','_')
            # minus symbol not allowed
            if name.startswith('tracking_point_'):
                name = name.replace('-','m')
            value = pair[1].strip()
            return [name, value]
    else:
        return False

# convert name/value pair to text line
def setting_to_text(name, value):
    if name.startswith('tracking_point_'):
        name = name.replace('m','-')
    name = name.replace('_',' ')
    line = name+': '+value+'\n'
    return line

### Read sysex into settings
def import_file(file_name):
    # convert syx to text
    if file_name.endswith('.syx'):
        fix_syx(file_name)
        cmd = [ion_decoder_path, '-b', file_name]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            # change file suffix
            file_name = file_name[:-3]+'txt'
        else:
            # alesis' script shows error here
            file_name = default_prog
    elif not file_name.endswith('.txt'):
        print('File type must be .txt or .syx')
        file_name = default_prog
    # read text file into a dict
    txt_file = open(file_name)
    settings = {}
    print('loading '+file_name)
    for line in txt_file:
        pair = text_to_setting(line)
        if pair:
            settings[pair[0]] = pair[1]
    txt_file.close()
    return settings


def export_file(file_name):
    return True

### Receive sysex and return settings
def receive_sysex(midi_port):
    # dump amidi port to file
    cmd = ['amidi', '-t', '3', '-p']
    cmd +=  [midi_port, '-r', midi_cache]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        fix_syx(midi_cache)
        settings = import_file(midi_cache)
        return settings
    else:
        # shows amidi error
        return False

### Check the command line arguments
def startup(args):
    if len(args) == 1:
        # without argument, load the default program
        settings = import_file(default_prog)
    else:
        # receive sysex option
        if args[1] == '-r':
            try:
                # check if port given
                args[2]
            except:
                print('Please specify a MIDI port')
                sys.exit(1)
            else:
                settings = receive_sysex(arg[2])
        # otherwise check if argument is a valid file
        elif os.path.isfile(args[1]):
            settings = import_file(args[1])
        else:
            print('Error opening "'+args[1]+'": File not found')
            sys.exit(1)
    return settings

### Fix syx function
# try to trim down sysex files when
# size is more than 434 bytes
def fix_syx(path):
    size = os.path.getsize(path)
    if size > 434:
        with open(path, 'rb') as file:
            syx = file.read()
        start = syx.find(b'\xf0\x00')
        end = syx.find(b'\xf7')+1
        # if length between f0 00 and f7
        # is 434 byte, it's a micron sysex
        if (end - start) == 434:
            new_content = syx[start:end]
            # backup old sysex
            backup = open(path[:-4]+'_old.syx', 'wb')
            backup.write(syx)
            backup.close()
            fixed = open(path, 'wb')
            fixed.write(new_content)
            fixed.close()
