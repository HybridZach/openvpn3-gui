# Standard imports
import logging
import os
import sys
from configparser import ConfigParser

import httplib2
# From imports
from PyQt5 import QtCore, QtWidgets, QtGui

from gsl import remove_cache

# Set config file and global variables
global config_
config = ConfigParser()
config.read('config.ini')

# Check config file and set configs acordingly
# VPN profile DIR
profile_dir = config.get('Config Settings', 'profiledir')
# Set default VPN profile
config_ = config.get('Config Settings', 'default_vpn_profile')
# Set default log level
debug_logging = config.get('Config Settings', 'debug')
# Debug handling
if debug_logging == 'on':
    logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)
else:
    print("Debugging not set by default")
    pass

# Create global for current connected vpn device (if exists)
from gsl import vpn_tun_grab

vpn_tun_grab()
os.chdir('/tmp/vpn_gui/tun/')
stream_dc = os.popen('cat ' + 'tmp*')
text = stream_dc.read().replace('\n', '')
vpn_device = text

# Check for CL argv and set acordingly
if len(sys.argv) > 1:
    config_ = sys.argv[1]
    os.chdir(profile_dir)
    # Making sure VPN is disconnected first if connected to begin with
    os.popen("openvpn3 session-manage -I " + vpn_device + " --disconnect")
    print("\nWaiting 2 seconds for disconnection, and connecting via CLI arg \n")
    os.popen('sleep 2')
    stream_con = os.popen("openvpn3 session-start --config" + " " + config_)
    text = stream_con.read()
    print("\n" + text + "\n")
else:
    print("No VPN set via CLI.")


# MainWindow instance creation
class UiMainWindow(object):
    # Un-used for now external label updater function
    """def update_label(self):
        self.update = update.label_update(self)"""

    # Create layouts and UI
    def setupui(self, mainwindow):
        mainwindow.setObjectName("MainWindow")
        mainwindow.resize(420, 420)
        os.chdir(os.path.dirname(__file__))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.ip_check_button = QtWidgets.QPushButton(self.centralwidget)
        self.ip_check_button.setObjectName("ip_check_button")
        self.gridLayout.addWidget(self.ip_check_button, 5, 0, 1, 1)
        self.close_button = QtWidgets.QPushButton(self.centralwidget)
        self.close_button.setObjectName("close_button")
        self.gridLayout.addWidget(self.close_button, 7, 0, 1, 1)
        self.input_button = QtWidgets.QPushButton(self.centralwidget)
        self.input_button.setObjectName("input_button")
        self.gridLayout.addWidget(self.input_button, 2, 0, 1, 1)
        self.vpn_connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.vpn_connect_button.setObjectName("vpn_connect_button")
        self.gridLayout.addWidget(self.vpn_connect_button, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.vpn_dc_button = QtWidgets.QPushButton(self.centralwidget)
        self.vpn_dc_button.setObjectName("vpn_dc_button")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.vpn_dc_button, 6, 0, 1, 1)
        mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainwindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 420, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDebug = QtWidgets.QMenu(self.menubar)
        self.menuDebug.setObjectName("menuDebug")
        mainwindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainwindow)
        self.statusbar.setObjectName("statusbar")
        mainwindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(mainwindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addSeparator()
        # self.actionPopout = QtWidgets.QAction(mainwindow)
        # self.actionPopout.setObjectName("actionPopout")
        self.actionVPN_status = QtWidgets.QAction(mainwindow)
        self.actionVPN_status.setObjectName("actionVPN_status")
        # self.actionDebug_print = QtWidgets.QAction(mainwindow)
        # self.actionDebug_print.setObjectName("actionDebug_print")
        self.menuFile.addAction(self.actionExit)
        # self.menuDebug.addAction(self.actionPopout)
        # self.menuDebug.addAction(self.actionPopout)
        self.menuDebug.addAction(self.actionVPN_status)
        # self.menuDebug.addAction(self.actionDebug_print)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDebug.menuAction())
        self.retranslateui(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)
        self.actionExit.triggered.connect(lambda: self.exit_button())
        self.actionVPN_status.triggered.connect(lambda: self.vpn_status())
        # self.actionDebug_print.triggered.connect(lambda: self.debug_print())
        # self.actionPopout.triggered.connect(lambda: self.debug_())

    # Text translation and definitions
    def retranslateui(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("MainWindow", "VPN GUI"))
        self.ip_check_button.setText(_translate("MainWindow", "IP Checker"))
        self.close_button.setText(_translate("MainWindow", "Close"))
        self.input_button.setText(_translate("MainWindow", "Manual VPN profile"))
        self.vpn_connect_button.setText(_translate("MainWindow", "VPN Connect"))
        # Some exception handling for making sure the vpn profile is somehow not set to a non-existent dir
        try:
            # Ensuring GUI CWD for VPN profiles exists
            os.chdir(profile_dir)
            print('GUI CWD is:', os.getcwd())
            # If exists show normal GUI greeting label
            self.label.setText(_translate("MainWindow", "OPENVPN3 GUI \n Version 0.1"))
        except:
            # Exception for this is to show in GUI label and continue to not break GUI
            self.label.setText(_translate("MainWindow", "The VPN directory \n set in config does not exist!"))
            pass
        self.vpn_dc_button.setText(_translate("MainWindow", "Disconnect VPN"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDebug.setTitle(_translate("MainWindow", "Debug"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Close the GUI."))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        # self.actionPopout.setText(_translate("MainWindow", "Debug Log"))
        # self.actionPopout.setStatusTip(_translate("MainWindow", "Tail any debugging."))
        # self.actionPopout.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionVPN_status.setText(_translate("MainWindow", "VPN status"))
        self.actionVPN_status.setStatusTip(_translate("MainWindow", "Current VPN status."))
        self.actionVPN_status.setShortcut(_translate("MainWindow", "Ctrl+S"))
        # self.actionDebug_print.setText(_translate("MainWindow", "Debug Print"))
        # self.actionDebug_print.setStatusTip(_translate("MainWindow", "Console print."))
        # self.actionDebug_print.setShortcut(_translate("MainWindow", "Ctrl+D"))
        # Set button action functions (as seen below)
        self.close_button.clicked.connect(self.exit_button)
        self.ip_check_button.clicked.connect(self.ip_checker)
        self.vpn_dc_button.clicked.connect(self.vpn_dc_)
        self.vpn_connect_button.clicked.connect(self.vpn_connect_)
        self.input_button.clicked.connect(self.showinputdialog)

    # Functions (Mainly of buttons)
    def vpn_dc_(self):
        os.chdir(profile_dir)
        print(os.getcwd())
        stream_dc = os.popen("openvpn3 session-manage -I " + vpn_device + " --disconnect")
        # Delete old status files
        remove_cache()
        text = stream_dc.read()
        self.label.setText(text)
        self.label.adjustSize()

    def vpn_status(self):
        # from gsl import final_list
        from gsl import vpn_status_grab
        vpn_status_grab()
        os.chdir('/tmp/vpn_gui')
        stream_dc = os.popen('tail ' + 'tmp*')
        text = stream_dc.read()
        self.label.setText(text)
        remove_cache()

    """def debug_(self):
        pathlib.Path(__file__).parent.resolve()
        stream_debug = os.popen('tail -n 5 debug.log')
        debug_output = stream_debug.read()
        self.label.setText(debug_output)
        self.label.adjustSize()"""

    def vpn_connect_(self):
        # Making sure VPN is disconnected first if connected to begin with
        os.popen("openvpn3 session-manage -I " + vpn_device + " --disconnect")
        self.label.setText("Waiting 2 seconds for disconnection.")
        os.popen('sleep 2')
        # Delete old status files
        remove_cache()
        # Making sure in VPN config folder
        os.chdir(profile_dir)
        stream_con = os.popen("openvpn3 session-start --config" + " " + config_)
        text = stream_con.read()
        self.label.setText(text)
        self.label.adjustSize()

    @staticmethod
    def exit_button():
        remove_cache()
        sys.exit()

    def ip_checker(self):
        # Check for internet first?
        self.label.setText('Checking for connection...')

        conn = httplib2.HTTPSConnectionWithTimeout("1.1.1.1", timeout=1)
        try:
            conn.request("HEAD", "/")
            stream_ip = os.popen('curl ifconfig.me/ip')
            ip_output = stream_ip.read()
            self.label.setText('Your external IP is: \n' + ip_output)
            self.label.adjustSize()
        except:
            # If no connection found display that to the user via GUI label
            self.label.setText("There is no network connection.")

    # Input dialog for manual VPN profile specification
    def showinputdialog(self):
        text, ok_pressed = QtWidgets.QInputDialog.getText(None,
                                                          "Input",
                                                          "Please specify profile",
                                                          QtWidgets.QLineEdit.Normal,
                                                          "")
        if ok_pressed and text != '':
            global config_
            config_ = text
            print(config_ + ' was just set as current profile.')
            # Making sure VPN is disconnected first if connected to begin with
            os.popen("openvpn3 session-manage -I " + vpn_device + " --disconnect")
            self.label.setText("Waiting 2 seconds for disconnection.")
            os.popen('sleep 2')
            # Delete old status files
            remove_cache()
            # Making sure in VPN config folder
            os.chdir(profile_dir)
            stream_con = os.popen("openvpn3 session-start --config" + " " + config_)
            text = stream_con.read()
            self.label.setText(text)
            self.label.adjustSize()
        if text == '':
            print('No profile was specified.')
            self.label.setText('No profile was specified.')
            self.label.adjustSize()

    # Un-used staticmethod function for printing debugs in the console via GUI
    # Remove comments to debug_print variable to enable
    # @staticmethod
    """def debug_print():
        print(config_)
        print(os.getcwd())"""


# Main python app
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupui(MainWindow)
    MainWindow.show()
    sys.exit([app.exec_(), remove_cache()])
