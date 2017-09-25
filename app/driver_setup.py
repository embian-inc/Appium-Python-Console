import sys, os, time, imp, glob, subprocess, platform
import ko, en
from appium import webdriver
from desired_capabilities import get_desired_capabilities

def setUp(self):
    set_config(self)
    desired_caps = get_desired_capabilities(self.platform_version, self.device_name, self.apk_filename)
    self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

def set_config(self):
    config_filename = os.path.join('app','config.py')
    self.native_only = False
    self.lang = 'en-us'
    self.BANNER = en.APC_BANNER
    self.HELP = en.HELP_MSG
    self.mode = 'APC'
    
    for v in sys.argv:
        if '--config' in v:
            t = v.split('=')
            if len(t) == 2:
                config_filename = t[1]
        if '--native' in v:
            self.native_only = True
        if '--adb-path' in v:
            t = v.split('=')
            if len(t) == 2:
                self.adb_cmd = t[1]
        if '-kor' in v:
            self.lang = 'ko-kr'
            self.BANNER = ko.APC_BANNER
            self.HELP = ko.HELP_MSG
        if '--mode' in v:
            t = v.split('=')
            if len(t) == 2 and t[1] == 'm':
                self.mode = 'Manual_Test'
            if len(t) == 2 and t[1] == 'dev':
                self.mode = 'dev'

    config_file = os.path.join(config_filename)
    config = imp.load_source('config', config_file)

    self.platform_name = config.PLATFORM_NAME
    self.device_name = config.DEVICE_NAME
    self.platform_version = config.PLATFORM_VERSION
    self.apk_filename = config.APK_FILE_NAME
    self.save_dir = '%s' % ( time.strftime('%y-%m-%d_%H%M%S', time.localtime()) )
    self.doc_save_dir = os.path.join(config.DOC_SAVE_DIR, self.apk_filename, self.save_dir)
    make_sure_path_exists(self.doc_save_dir)

    ## uiautomator2 server patch
    # uiautomator2_server_patch(config)

    ## clean
    # clean(self)

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def uiautomator2_server_patch(config):
    # uiautomator2 server patch
    uiaumator2_patch_test = None
    uiaumator2_patch_server = None
    for apk in [os.path.abspath(f) for f in glob.glob("uiautomator2/*.apk")]:
        if 'debug' not in os.path.basename(apk):
            uiaumator2_patch_test = apk
        else:
            uiaumator2_patch_server = apk

    uiaumator2_apks = glob.glob("%s/node_modules/appium-uiautomator2-driver/uiautomator2/*.apk" % config.APPIUM_HOME)

    cp_cmd = 'cp'
    if 'window' in platform.platform().lower():
        cp_cmd = 'copy'
    patch_list = []
    for apk in uiaumator2_apks:
        if 'debug' not in os.path.basename(apk):
            patch_list.append('%s %s %s' % (cp_cmd, uiaumator2_patch_test, apk))
        else:
            patch_list.append('%s %s %s' % (cp_cmd, uiaumator2_patch_server, apk))

    for patch in patch_list:
        popen = subprocess.Popen(patch, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (stdoutdata, stderrdata) = popen.communicate()
        if stderrdata != '':
            print "\nPatch Failed: %s" % patch

def clean(self):
    print "Device cleaning....."
    cleans = [
        self.adb_cmd + ' uninstall io.appium.uiautomator2.server',
        self.adb_cmd + ' uninstall io.appium.uiautomator2.server.test',
        self.adb_cmd + ' uninstall io.appium.settings',
        self.adb_cmd + ' uninstall io.appium.unlock'
    ]
    for clean in cleans:
        popen = subprocess.Popen(clean, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (stdoutdata, stderrdata) = popen.communicate()
        if stderrdata != '':
            print "\nClean Failed: %s" % clean

    home_key = self.adb_cmd + ' shell input keyevent KEYCODE_HOME'
    popen = subprocess.Popen(home_key, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    if stderrdata != '':
        print "\nadb command Failed: %s" % home_key
    else:
        print "OK"
