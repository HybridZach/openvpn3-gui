# Standard imports
import glob
import itertools
import os
import sys
# From imports
from configparser import ConfigParser
from tempfile import mkstemp

# Set config file and global variables
global config_
config = ConfigParser()
config.read('config.ini')


# Function to call openvpn3 sessions-list in GUI (neatened up)
def vpn_status_grab():
    # Check to see if the VPN cache DIR somehow exists
    if glob.glob('/tmp/vpn_gui/'):
        """Do nothing if exists because needed"""
    # Make VPN cache DIR
    else:
        os.mkdir('/tmp/vpn_gui/')
    # Check to see if vpn_status_grab file(s) exist already
    if glob.glob('/tmp/vpn_gui/tmp*'):
        # Make sure in right directory first
        os.chdir('/tmp/vpn_gui/')
        # Remove old cache if exists
        os.popen('rm -r tmp*')
    # Begin creating new cache for vpn_status_grab
    else:
        # Create empty temp files in the cache folder
        fd, tmp_file_pipe = mkstemp(dir='/tmp/vpn_gui/')
        fd, tmp_file_list = mkstemp(dir='/tmp/vpn_gui/')

        # Pipe openvpn3 sessions list to tempoary temp file being used as pipe variable
        os.system('openvpn3 sessions-list >' + tmp_file_pipe)

        # Function to clean up the output of console pipe
        def list_make():
            with open(tmp_file_pipe, 'r+') as file:
                if 'No sessions available\n' in file.read():
                    print("No VPN is running. \n No network?")
                else:
                    with open(tmp_file_pipe, 'r+') as file2_:
                        lines = file2_.readlines()
                        lines = [line.split() for line in lines]
                        lines2 = (lines[2:7])
                        merged = list(itertools.chain(*lines2))
                        created_ = merged[0:5]
                        print(' '.join(created_))
                        pid_ = merged[6:8]
                        print(' '.join(pid_))
                        user_ = merged[8:10]
                        print(' '.join(user_))
                        interface_ = merged[10:12]
                        print(' '.join(interface_))
                        config_name_ = merged[12:15]
                        print(' '.join(config_name_))
                        session_name_ = merged[18:21]
                        print(' '.join(session_name_))
                        con_status_ = merged[21:26]
                        con_status_.remove(con_status_[1])
                        print(' '.join(con_status_))

        # Save the cleaned up console output to that file
        stdout_backup = sys.stdout
        with open(tmp_file_list, 'r+') as file_:
            sys.stdout = file_
            list_make()
        sys.stdout = stdout_backup
        os.unlink(tmp_file_pipe)


# Function to grab tun device via openvpn3 sessions-list
def vpn_tun_grab():
    # Does tun dir exist?
    if glob.glob('/tmp/vpn_gui/tun'):
        pass
    # Create the directory
    else:
        os.makedirs('/tmp/vpn_gui/tun')
        os.chdir(r'/tmp/vpn_gui/tun')
    # Create the temp files for tun device pipe
    fd, tmp_file_pipe_tun = mkstemp(dir='/tmp/vpn_gui/tun')
    fd, tmp_file_list_tun = mkstemp(dir='/tmp/vpn_gui/tun')
    # Pipe openvpn3 sessions list to tempoary temp file being used as pipe variable
    os.system('openvpn3 sessions-list >' + tmp_file_pipe_tun)

    # Clean up the output of console pipe (showing only interface this time)
    def tun_grab():
        with open(tmp_file_pipe_tun, 'r+') as file:
            if 'No sessions available\n' in file.read():
                print("No VPN is running. \n No network?")
            else:
                with open(tmp_file_pipe_tun, 'r+') as file2:
                    lines = file2.readlines()
                    lines = [line.split() for line in lines]
                    lines2 = (lines[2:7])
                    merged = list(itertools.chain(*lines2))
                    interface_ = merged[11:12]
                    interface = ' '.join(interface_)
                    print(interface)

    # Save the cleaned up console output to that file
    stdout_backup = sys.stdout
    with open(tmp_file_list_tun, 'r+') as file:
        sys.stdout = file
        tun_grab()
    sys.stdout = stdout_backup
    # print(os.getcwd())
    os.popen('rm ' + tmp_file_pipe_tun)


# Function for main GUI to remove cache files if not already removed
def remove_cache():
    os.chdir('/tmp/')
    if glob.glob('vpn_gui/'):
        os.popen('rm -r vpn_gui/')
    else:
        pass
