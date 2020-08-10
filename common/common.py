# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import logging
import time
import traceback
from datetime import datetime

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not lib_path in sys.path:
    sys.path.append(lib_path)
from automator.uiautomator import Device
from automator.uiautomator import Selector
from automator.uiautomator import AutomatorDevice
from configs import GetConfigs, Configs
from automator.adb import Adb
import random
from configs import AppConfig
from functools import wraps
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import subprocess

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result

    return wrapper


class UIParser():
    @staticmethod
    def nest(self, func):
        def wrapper(*args, **kwargs):
            func(args)

        return wrapper

    @staticmethod
    def run(obj, params, exceptfunc=None):
        device = obj if isinstance(obj, Device) else obj.device

        def param_parser(param):
            if isinstance(param, dict):
                for k, v in param.items():
                    if v == None:
                        param.pop(k)
            else:
                for v in param:
                    if v == None:
                        param.remove(v)

        def error(param):
            if param.has_key("assert") and param['assert'] == False:
                return False
            else:
                print "%s error!" % param
                exceptfunc() if (exceptfunc) else None
                return True

        def listfoo(param):
            resault = True
            if isinstance(param["content"], list):
                for content in param["content"]:
                    param_tmp = param
                    param_tmp["content"] = content
                    resault = resault and listfoo(param)
            elif param["id"] == "meta":
                resault = resault and getattr(obj, param["content"])(
                    *param["action"]["param"] if param.has_key("action") and param["action"].has_key("param") else [])
            else:
                print param
                if param_parser(param["id"]) == {}:
                    return True
                select = device(**{param["id"]: param["content"]})
                action = select.wait.exists(timeout=5000) if not param.has_key("wait") else select.wait.exists(
                    timeout=int(param["wait"]))
                if action and not (param.has_key("action") and param["action"] == None):
                    getattr(select, "click")(None) if not param.has_key("action") else getattr(select,
                                                                                               param["action"]["type"])(
                        *param["action"]["param"] if param["action"].has_key("param") else [])
                    time.sleep(
                        param["action"]["delay"] if param.has_key("aciton") and param["action"].has_key("delay") else 0)
                resault = resault and action
            return resault

        def dictfoo(param):
            resault = True
            if not param.has_key("id"):
                return False
            if isinstance(param["id"], list):
                for content in param["id"]:
                    param_tmp = param
                    param_tmp["id"] = content
                    if param["id"].has_key("action"):
                        param_tmp["action"] = param["action"]
                    resault = resault and listfoo(param)
            elif param["id"].has_key("meta"):
                resault = resault and getattr(obj, param["id"]["meta"])(
                    *param["action"]["param"] if param.has_key("action") and param["action"].has_key("param") else [])
            else:
                if param_parser(param["id"]) == {}:
                    return True
                select = device(**param["id"])
                # action=select.wait.exists(timeout = 5000) if ((not param.has_key("wait")) or ((param.has_key("wait") and param["wait"]))) else select.wait.exists(timeout = int(param["wait"]))
                action = select.wait.exists(timeout=5000) if not param.has_key("wait") else select.wait.exists(
                    timeout=int(param["wait"]))
                if action and not (param.has_key("action") and param["action"] == None):
                    getattr(select, "click")(None) if not param.has_key("action") else getattr(select,
                                                                                               param["action"]["type"])(
                        *param["action"]["param"] if param["action"].has_key("param") else [])
                    time.sleep(
                        param["action"]["delay"] if param.has_key("aciton") and param["action"].has_key("delay") else 0)
                resault = resault and action
            return resault

        for param in params:
            if isinstance(param, list):
                UIParser.run(obj, param)
            else:
                if param.has_key("id") and isinstance(param["id"], dict):
                    if not dictfoo(param):
                        if (error(param)):
                            return False
                elif param.has_key("id") and param.has_key("content") and not isinstance(param["id"], dict):
                    if not listfoo(param):
                        if (error(param)):
                            return False
        return True


def create_folder():
    """Create folder to save pic & log.     
    Return a folder path or None
    Exception: OSError
    """
    log_path = os.environ.get("LOG_PATH")
    if log_path is None:
        # log_path = sys.path[0][sys.path[0].find(':') + 1:] + '\\results'
        log_path = sys.path[0][sys.path[0].find(':') + 1:] + '/results'
    if not os.path.exists(log_path):
        logger.debug("log_path not exsit")
        os.makedirs(log_path)
    if not os.path.exists(log_path):
        return None
    return log_path


def createlogger(name):
    """Create a logger named specified name with the level set in config file.  
    return a logger
    """
    config = GetConfigs("common")
    lev_key = config.getstr("LOG_FITER", "Default", "common").upper()
    lev_dict = {"DEBUG": logging.DEBUG, "INFO": logging.INFO,
                "WARNING": logging.WARNING, "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL}
    logger = logging.getLogger(name)
    logger.setLevel(lev_dict[lev_key])
    ch = logging.StreamHandler()
    current_time = time.strftime('%Y_%m_%d %H_%M_%S', time.localtime(time.time()))
    fh = logging.FileHandler(current_time + "_CTS_Verifier" + ".log")

    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d: [%(levelname)s] [%(name)s] [%(funcName)s][%(lineno)d] %(message)s',
        '%y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    fh.setFormatter(formatter)
    return logger


logger = createlogger("COMMON")


def log_traceback(traceback):
    """print traceback information with the log style.
    """
    str_list = traceback.split("\n")
    for string in str_list:
        logger.warning(string)


def connect_device(device_name):
    """connect_device(device_id) -> Device    
    Connect a device according to device ID.
    """
    environ = os.environ
    device_id = environ.get(device_name)
    if device_id == None:
        device_id = device_name
    # backend = Configs("common").get("backend", "Info")
    logger.debug("Device ID is " + device_id)
    device = Device(device_id)
    if device is None:
        logger.critical("Cannot connect device.")
        raise RuntimeError("Cannot connect %s device." % device_id)
    return device


def startactivity(serial, packet, activity):
    """start activity
    """
    adb = Adb(serial)
    data = adb.shell("am start -n %s/%s" % (packet, activity))
    if data.find("Error") > -1:
        return False
    return True


def random_name(index_num):
    numseed = "0123456789"
    sa = []
    for i in range(5):
        sa.append(random.choice(numseed))
    stamp = ''.join(sa)
    strname = 'Auto%02d_' % (index_num + 1) + stamp
    logger.debug('Create a random name %s.' % strname)
    return strname


class Common(object):
    """Provide common functions for all scripts."""

    def __init__(self, device, mod=None, sdevice=None, timeout=5000):
        self.timeout = timeout
        self.mdevice_id = device
        self.sdevice_id = sdevice
        if isinstance(device, Device):
            self.device = device
        else:
            self.device = connect_device(device)
        if sdevice == None:
            pass
        elif isinstance(sdevice, Device):
            self.sdevice = sdevice
        else:
            print "sdevice:%s", sdevice
            self.sdevice = connect_device(sdevice)
        self.logger = createlogger(mod)
        self.log_path = create_folder()
        self.config = GetConfigs("common")
        self.appconfig = AppConfig("appinfo")
        self.appconfig.set_section(mod)
        self.adb = self.device.server.adb
        if sdevice:
            self.adb_sdevice = self.sdevice.server.adb
        self.suc_times = 0
        try:
            self.mod_cfg = GetConfigs(mod)
            self.test_times = 0
            self.dicttesttimes = self.mod_cfg.get_test_times()
            for test_time in self.dicttesttimes:
                self.test_times += int(self.dicttesttimes[test_time])
            self.logger.info("Trace Total Times " + str(self.test_times))
        except:
            pass

    def device(self):
        return self.device

    def sdevice(self):
        return self.sdevice


    def clear_notification(self):
        self.logger.info("clear notification")
        if self.device(description="Clear all notifications.").exists:
            self.device(description="Clear all notifications.").click()
            return True
        self.device.open.notification()
        if self.device(description="Clear all notifications.").wait.exists(timeout=2000):
            self.device(description="Clear all notifications.").click()
            self.device.delay(1)
            return True
        if self.device(text="CLEAR ALL").wait.exists(timeout=2000):
            self.device(text="CLEAR ALL").click()
            self.device.delay(1)
            return True
        elif self.device(scrollable=True).exists:
            for i in range(3):
                # self.device.swipe(650, 1380, 650, 1000)
                notification = self.device(resourceId="com.android.systemui:id/notification_stack_scroller")
                if notification.exists:
                    notification.scroll.vert.toEnd(steps=20)
                    self.device.wait("idle")
                    if self.device(description="Clear all notifications.").wait.exists(timeout=2000):
                        self.device(description="Clear all notifications.").click()
                        self.device.delay(1)
                        return True
                    if self.device(text="CLEAR ALL").wait.exists(timeout=2000):
                        self.device(text="CLEAR ALL").click()
                        self.device.delay(1)
                        return True
        self.device.press.back()

    def check_device_administrators(self,check_item):
        state = ""
        self.logger.debug("start to check the %s's administrator is Activate or not?")
        self.enter_settings("Security & location")
        self.device(scrollable=True).scroll.vert.to(text="Device admin apps")
        if self.device(text="Device admin apps").wait.exists(timeout=5000):
            self.device(text="Device admin apps").click()
        count = self.device(resourceId="android:id/list",className="android.widget.ListView").child(className="android.widget.LinearLayout").count
        print "count:", count

        for index in range(count):
            if self.device(resourceId="android:id/list", className="android.widget.ListView").child(
                    className="android.widget.LinearLayout", index=index).wait.exists(timeout=5000):
                appName = ""
                if self.device(resourceId="android:id/list").child(
                        className="android.widget.LinearLayout", index=index).child(
                        className="android.widget.RelativeLayout").child(
                        resourceId="com.android.settings:id/name").wait.exists(timeout=5000):
                    appName = self.device(resourceId="android:id/list").child(
                        className="android.widget.LinearLayout", index=index).child(
                        className="android.widget.RelativeLayout").child(
                        resourceId="com.android.settings:id/name").get_text()
                else:
                    # 某些title 下的子元素com.android.settings:id/name 并不一定存在
                    continue
                print "appName is :", appName
                if appName == check_item:
                    isChecked = self.device(resourceId="android:id/list").child(className="android.widget.LinearLayout",
                                                                                index=index).child(
                        resourceId="com.android.settings:id/checkbox").isChecked()
                    print "isChecked:", isChecked
                    if isChecked:
                        self.logger.debug("%s is Activate"%appName)
                        state = "Activate"
                    else:
                        self.logger.debug("%s is Deactivate"%appName)
                        if not state == "Activate":
                            state = "Deactivate"
            else:
                break

        self.logger.debug("the item %s's state is %s"%(check_item,state))
        return state

    def active_verifiy_admin(self):
        self.logger.debug("start to active the verifier apk")
        self.enter_settings("Security & location")

        self.device(scrollable=True).scroll.vert.to(text="Device admin apps")
        if self.device(text="Device admin apps").wait.exists(timeout=5000):
            self.device(text="Device admin apps").click()

        count = self.device(className="android.widget.LinearLayout").count
        print "count:", count
        CTS_verifier_click_count = 0
        for index in range(count):
            if self.device(resourceId="android:id/list", className="android.widget.ListView").child(
                    className="android.widget.LinearLayout", index=index).wait.exists(timeout=5000):
                appName = ""
                if self.device(resourceId="android:id/list").child(
                        className="android.widget.LinearLayout", index=index).child(
                        className="android.widget.RelativeLayout").child(
                        resourceId="com.android.settings:id/name").wait.exists(timeout=5000):
                    appName = self.device(resourceId="android:id/list").child(
                        className="android.widget.LinearLayout", index=index).child(
                        className="android.widget.RelativeLayout").child(
                        resourceId="com.android.settings:id/name").get_text()
                else:
                    # 某些title 下的子元素com.android.settings:id/name 并不一定存在
                    continue
                # print "appName is :", appName

                if appName == "CTS Verifier":
                    CTS_verifier_click_count += 1
                    isChecked = self.device(resourceId="android:id/list").child(className="android.widget.LinearLayout",
                                                                                index=index).child(
                        resourceId="com.android.settings:id/checkbox").isChecked()
                    # print "isChecked:", isChecked
                    if not isChecked and CTS_verifier_click_count == 2:
                        self.device(resourceId="android:id/list").child(className="android.widget.LinearLayout",
                                                                        index=index).child(
                            resourceId="com.android.settings:id/checkbox").click()
                        self.device(scrollable=True).scroll.vert.to(text="Activate this device admin app")
                        self.device(text="Activate this device admin app").click()

                        self.logger.debug("Active CTS Verifier  Successfully")

            else:
                break
        return True

    def Deactive_verifiy_admin(self,item):
        self.logger.debug("start to Deactive the %s apk"%item)
        self.enter_settings("Security & location")

        self.device(scrollable=True).scroll.vert.to(text="Device administrators")
        if self.device(text="Device administrators").wait.exists(timeout=5000):
            self.device(text="Device administrators").click()

        count = self.device(className="android.widget.LinearLayout").count
        print "count:", count

        for index in range(count):
            if self.device(resourceId="android:id/list", className="android.widget.ListView").child(
                    className="android.widget.LinearLayout", index=index).wait.exists(timeout=5000):
                appName = ""
                if self.device(resourceId="android:id/list").child(
                        className="android.widget.LinearLayout", index=index).child(
                        className="android.widget.RelativeLayout").child(
                        resourceId="com.android.settings:id/name").wait.exists(timeout=5000):
                    appName = self.device(resourceId="android:id/list").child(
                        className="android.widget.LinearLayout", index=index).child(
                        className="android.widget.RelativeLayout").child(
                        resourceId="com.android.settings:id/name").get_text()
                else:
                    # 某些title 下的子元素com.android.settings:id/name 并不一定存在
                    continue
                print "appName is :", appName
                if appName == item:
                    isChecked = self.device(resourceId="android:id/list").child(className="android.widget.LinearLayout",
                                                                                index=index).child(
                        resourceId="com.android.settings:id/checkbox").isChecked()
                    print "isChecked:", isChecked
                    if isChecked:
                        self.device(resourceId="android:id/list").child(className="android.widget.LinearLayout",
                                                                        index=index).child(
                            resourceId="com.android.settings:id/checkbox").click()
                        self.device(scrollable=True).scroll.vert.to(text="Deactivate this device admin app")
                        self.device(text="Deactivate this device admin app").click()

                        self.logger.debug("Deactive CTS Verifier  Successfully")
            else:
                break

        return True


    def time_task(self, start_time, seconds):
        end_time = time.time()
        print "end_time is %s", end_time
        duration = end_time - start_time
        print "duration is %s", duration
        if duration >= seconds:
            self.logger.debug("The time '%s' is over,return false,break the while circle" % seconds)
            return False
        else:
            self.logger.debug("The duration is %ss,less than %ss" % (duration, seconds))
            return True

    def save_fail_img(self, newimg=None):
        """save fail image to log path.        
        argv: The picture want to save as failed image.
        """

        # path = (self.log_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        path = (self.log_path + "/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        if newimg is None:
            self.logger.debug("Take snapshot.")
            newimg = self.device.screenshot(path)
        if newimg is None:
            self.logger.warning("newimg is None.")
            return False
        self.logger.error("Fail: %s" % (path))
        return True

    def send_checklistpass_img(self, emailList=""):
        """save fail image to log path.
        argv: The picture want to save as failed image.
        """

        # path = (self.log_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        path = (self.log_path + "/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        self.logger.debug("Start take a snapshot.")
        self.device.screenshot(path)
        self.logger.error("The Path is: %s" % (path))
        self.send_daily_checklistpass_report_email(path, emailList)

    def send_checklistfail_img(self, emailList=""):
        """save fail image to log path.
        argv: The picture want to save as failed image.
        """

        # path = (self.log_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        path = (self.log_path + "/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        self.logger.debug("Start take a snapshot.")
        self.device.screenshot(path)
        self.logger.error("The Path is: %s" % (path))
        self.send_daily_checklistfail_report_email(path, emailList)

    def send_fail_img(self, emailList=""):
        """save fail image to log path.
        argv: The picture want to save as failed image.
        """

        # path = (self.log_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        path = (self.log_path + "/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        self.logger.debug("Start take a snapshot.")
        self.device.screenshot(path)
        self.logger.error("The Path is: %s" % (path))
        # self.send_daily_report_email(path, emailList)

    def get_fingerprint(self):
        '''sdk version of connected device.'''
        fingerprint = ""
        try:
            fingerprint = self.adb.cmd("shell", "getprop", "ro.build.fingerprint").communicate()[0].decode(
                "utf-8").strip()
        except:
            self.logger.warning(traceback.format_exc())
        return fingerprint

    def send_daily_checklistpass_report_email(self, path, emailList):
        subject = "[CTS Verifier][PreCheckList]" + " Pass"
        username = "18768013577"
        password = 'z91718485'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        strTo = []
        if emailList == "":
            strTo = ['18768013577@163.com']
            self.logger.info("emailList is null,so send the result to everyone: %s" % strTo)
        else:
            strTo = emailList.split(",")

        # msg['to'] = ','.join(emailList)
        msg['from'] = '18768013577@139.com'

        jpgpart = MIMEApplication(open(path, 'rb').read())
        jpgpart.add_header('Content-Disposition', 'attachment', filename='test.png')
        msg.attach(jpgpart)

        fingerprint = self.get_fingerprint()
        htmlreport = "<h2>Hi all,</h2> " \
                     "<h4>Please check the attachment, thanks!</h4>" \
                     "<h4>The FingerPrint is: </h4> " \
                     "<p>" + fingerprint + "</p>"

        thebody = MIMEText(htmlreport, 'html', 'utf-8')
        msg.attach(thebody)

        smtp = smtplib.SMTP()
        smtp.connect('smtp.139.com:25')
        smtp.login(username, password)
        smtp.sendmail(msg['from'], strTo, msg.as_string())
        self.logger.info("send smoke daily report to %s successful" % strTo)
        smtp.quit()
        return True

    def send_daily_checklistfail_report_email(self, path, emailList):
        subject = "[CTS Verifier][PreCheckList]" + " Fail"
        username = "18768013577"
        password = 'z91718485'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        strTo = []
        if emailList == "":
            strTo = ['18768013577@163.com']
            self.logger.info("emailList is null,so send the result to everyone: %s" % strTo)
        else:
            strTo = emailList.split(",")

        # msg['to'] = ','.join(emailList)
        msg['from'] = '18768013577@139.com'

        jpgpart = MIMEApplication(open(path, 'rb').read())
        jpgpart.add_header('Content-Disposition', 'attachment', filename='test.png')
        msg.attach(jpgpart)

        fingerprint = self.get_fingerprint()
        htmlreport = "<h2>Hi all,</h2> " \
                     "<h4>Please check the attachment, thanks!</h4>" \
                     "<h4>The FingerPrint is: </h4> " \
                     "<p>" + fingerprint + "</p>"

        thebody = MIMEText(htmlreport, 'html', 'utf-8')
        msg.attach(thebody)

        smtp = smtplib.SMTP()
        smtp.connect('smtp.139.com:25')
        smtp.login(username, password)
        smtp.sendmail(msg['from'], strTo, msg.as_string())
        self.logger.info("send smoke daily report to %s successful" % strTo)
        smtp.quit()
        return True

    def send_daily_report_email(self, path, emailList):
        # TODO 修改成其他邮箱
        subject = "[CTS Verifier][Cross profile intent filters are set]" + " Result"
        username = "18768013577"
        password = 'z91718485'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        strTo = []
        if emailList == "":
            strTo = ['18768013577@163.com']
            self.logger.info("emailList is null,so send the result to everyone: %s" % strTo)
        else:
            strTo = emailList.split(",")

        # msg['to'] = ','.join(emailList)
        msg['from'] = '18768013577@139.com'

        jpgpart = MIMEApplication(open(path, 'rb').read())
        jpgpart.add_header('Content-Disposition', 'attachment', filename='test.png')
        msg.attach(jpgpart)

        fingerprint = self.get_fingerprint()
        htmlreport = "<h2>Hi all,</h2> " \
                     "<h4>Please check the attachment, thanks!</h4>" \
                     "<h4>The FingerPrint is: </h4> " \
                     "<p>" + fingerprint + "</p>"

        thebody = MIMEText(htmlreport, 'html', 'utf-8')
        msg.attach(thebody)

        smtp = smtplib.SMTP()
        smtp.connect('smtp.139.com:25')
        smtp.login(username, password)
        smtp.sendmail(msg['from'], strTo, msg.as_string())
        self.logger.info("send smoke daily report to %s successful" % strTo)
        smtp.quit()
        return True

    def save_fail_img_s(self, newimg=None):
        """save fail image to log path.
        argv: The picture want to save as failed image.
        """
        path = (self.log_path + "/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        if newimg is None:
            self.logger.debug("s-device Take snapshot.")
            newimg = self.sdevice.screenshot(path)
        if newimg is None:
            self.logger.warning("newimg is None.")
            return False
        self.logger.error("Fail: %s" % (path))
        return True

    def get_file_num(self, path, format):
        """get number of file with specified format.
        """
        content = self.adb.shell("ls " + path)
        num = content.count(format)
        self.logger.debug("%s file num is %d." % (format, num))
        return num

    def start_activity(self, packet, activity):
        data = self.device.server.adb.shell("am start -n %s/%s" % (packet, activity))
        if data.find("Error") > -1:
            self.logger.error("Fail: %s/%s" % (packet, activity))
            return False
        return True

    def start_app(self, name, b_desk=True):
        """start app
        arg: name(str) app name
             b_desk(Boolean) whether to start on the desktop
        """
        self.back_to_home()
        # self.device.press.home()
        self.device.delay(0.5)
        self.logger.debug("start app:%s" % name)
        # self.device.server.adb.restart_viewserver()
        if b_desk and self.device(text=name).exists:
            self.device(text=name).click.wait()
            return True
        self.device.press.home()
        if b_desk and self.device(text=name).wait.exists(timeout=1000):
            self.device(text=name).click.wait()
            return True
        elif b_desk and self.device(description=name).exists:
            self.device(description=name).click.wait()
            return True
        elif self.device(description="Apps").exists:
            self.device(description="Apps").click()
            if self.device(text=name).exists:
                self.device(text=name).click.wait()
                return True
            self.device(scrollable=True, resourceId="com.tct.launcher:id/apps_list_view").scroll.vert.toBeginning()
            self.device(scrollable=True).scroll.vert.to(text=name)
            if not self.device(text=name).exists:
                self.device.drag(470, 1250, 470, 970, 5)
            self.device.wait("idle")
            # self.device.wait(30)
            self.device(text=name).click.wait()
            return True
        elif self.device(description="All Items").exists:
            self.device(description="All Items").click()
            self.device.delay(1)
            self.device(text="APPS").click()
            self.device.delay(1)
            if self.device(text=name).exists:
                self.device(text=name).click.wait()
                if self.device(text=name, resourceId="com.blackberry.blackberrylauncher:id/title").exists:
                    self.device(text=name, resourceId="com.blackberry.blackberrylauncher:id/title").click.wait()
                return True
            self.device(scrollable=True,
                        resourceId="com.blackberry.blackberrylauncher:id/apps_view").scroll.vert.toBeginning()
            self.device(scrollable=True, resourceId="com.blackberry.blackberrylauncher:id/apps_view").scroll.vert.to(
                text=name)
            if not self.device(text=name).exists:
                self.device.drag(470, 1250, 470, 970, 5)
            self.device.wait("idle")
            self.device(text=name).click.wait()
            return True
        elif self.device(resourceId= "com.android.launcher3:id/all_apps_handle").wait.exists(timeout=5000) or self.device(description="Apps list").exists:
            self.logger.debug("hanle exists")
            # self.device(resourceId= "com.android.launcher3:id/all_apps_handle").click()
            self.device(description="Apps list").click()
            if self.device(text=name).exists:
                self.device(text=name).click.wait()
                return True
            self.device(scrollable=True, resourceId="com.android.launcher3:id/apps_list_view").scroll.vert.toEnd()
            self.device(scrollable=True, resourceId="com.android.launcher3:id/apps_list_view").scroll.vert.to(text=name)
            if not self.device(text=name).exists:
                self.device.drag(470, 1250, 470, 970, 5)
            self.device.wait("idle")
            # self.device.wait(30)
            self.device(text=name).click.wait()
        self.save_fail_img()
        return False

    def start_app_sdevice(self, name, b_desk=True):
        """start app
        arg: name(str) app name
             b_desk(Boolean) whether to start on the desktop
        """
        self.back_to_home_s()
        # self.device.press.home()
        self.sdevice.delay(0.5)
        self.logger.debug("start app:%s" % name)
        # self.sdevice.server.adb.restart_viewserver()
        if b_desk and self.sdevice(text=name).exists:
            self.sdevice(text=name).click.wait()
            return True
        self.sdevice.press.home()
        if b_desk and self.sdevice(text=name).wait.exists(timeout=1000):
            self.sdevice(text=name).click.wait()
            return True
        elif b_desk and self.sdevice(description=name).exists:
            self.sdevice(description=name).click.wait()
            return True
        elif self.sdevice(description="Apps").exists:
            self.sdevice(description="Apps").click()
            if self.sdevice(text=name).exists:
                self.sdevice(text=name).click.wait()
                return True
            self.sdevice(scrollable=True, resourceId="com.tct.launcher:id/apps_list_view").scroll.vert.toBeginning()
            self.sdevice(scrollable=True).scroll.vert.to(text=name)
            if not self.sdevice(text=name).exists:
                self.sdevice.drag(470, 1250, 470, 970, 5)
            self.sdevice.wait("idle")
            # self.sdevice.wait(30)
            self.sdevice(text=name).click.wait()
            return True
        elif self.sdevice(description="All Items").exists:
            self.sdevice(description="All Items").click()
            self.sdevice.delay(1)
            self.sdevice(text="APPS").click()
            self.sdevice.delay(1)
            if self.sdevice(text=name).exists:
                self.sdevice(text=name).click.wait()
                if self.sdevice(text=name, resourceId="com.blackberry.blackberrylauncher:id/title").exists:
                    self.sdevice(text=name, resourceId="com.blackberry.blackberrylauncher:id/title").click.wait()
                return True
            self.sdevice(scrollable=True,
                         resourceId="com.blackberry.blackberrylauncher:id/apps_view").scroll.vert.toBeginning()
            self.sdevice(scrollable=True, resourceId="com.blackberry.blackberrylauncher:id/apps_view").scroll.vert.to(
                text=name)
            if not self.sdevice(text=name).exists:
                self.sdevice.drag(470, 1250, 470, 970, 5)
            self.sdevice.wait("idle")
            self.sdevice(text=name).click.wait()
            return True
        self.save_fail_img()
        return False

    def back_to_all_apps(self):
        """back_to_all_apps.
        """
        # self.logger.debug("back to all apps")
        for loop in range(4):
            self.device.press.back()
            if self.device(text="exit").wait.exists(timeout=500):
                self.device(text="exit").click()
            elif self.device(text="Quit").wait.exists(timeout=500):
                self.device(text="Quit").click()
            if self.device(resourceId=self.appconfig.id("id_group_title", "MenuNavigation")).wait.exists(timeout=500):
                return True

    def start_all_app(self, num=3):
        '''Call/People/ALL APPS/Messaging/Browser'''
        self.logger.debug("start all app")
        if self.device(description="ALL APPS").exists:
            self.device(description="ALL APPS").click()
        elif self.device(description="Apps").exists:
            self.device(description="Apps").click()
            self.device().fling.horiz.toBeginning()
        self.device().fling.horiz.toBeginning()
        for loop in range(3):
            self.adb.shell("input swipe 500 350 500 1600")
        for i in range(num):
            for j in range(self.device(className="android.widget.TextView").count - 2):
                if self.device(resourceId="com.tct.launcher:id/apps_customize_pane_content").child(index=0).child(
                        index=i).exists:
                    self.device(resourceId="com.tct.launcher:id/apps_customize_pane_content").child(index=0).child(
                        index=i).child(index=j).click()
                    self.device(text="ALL APPS").wait.gone(timeout=20000)
                    self.back_to_all_apps()
            self.device().fling.horiz.forward()
        return False

    def select_menu_item(self, stritem):
        self.device.press.menu()
        self.device.delay(1)
        self.device(text=stritem).click()
        self.device.delay(2)

    def _is_connected(self, type):
        temp_type = type
        if type == "ALL":
            temp_type = "LTE"
        for i in range(5):
            if self.adb.get_data_service_state() == temp_type:
                break
            self.device.delay(5)
        else:
            self.logger.warning("Cannot get %s service." % (type))
            self.device.press.back()
            return False
        for i in range(5):
            if self.adb.get_data_connected_status():
                return True
            self.device.delay(5)
        else:
            self.logger.warning("Cannot connect %s data." % (type))
            self.device.press.back()
            return False

    def switch_network(self, type=None):
        """switch network to specified type.    
        argv: (str)type -- the type of network.    
        """
        self.logger.debug("Switch network to %s." % (type))
        self.start_activity(self.appconfig("RadioInfo", "package"), self.appconfig("RadioInfo", "activity"))
        self.device.delay(2)
        network_type = self.appconfig("RadioInfo", type)
        self.device(scrollable=True).scroll.to(text=self.appconfig("RadioInfo", "set"))
        if self.device(resourceId=self.appconfig.id("RadioInfo", "id_network")).wait.exists(timeout=2000):
            self.device(resourceId=self.appconfig.id("RadioInfo", "id_network")).click()
        self.device(scrollable=True).scroll.to(text=network_type)
        self.device.delay(1)
        self.device(text=network_type).click()
        self._is_connected(type)
        self.back_to_home()

    def scroll_to_case(self, case_name, count=0):
        self.logger.debug("Start to scroll to case:%s" % case_name)
        if self.device(resourceId="android:id/list", scrollable=True).wait.exists(timeout=5000):
            self.device(resourceId="android:id/list", scrollable=True).scroll.vert.to(text=case_name)

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.logger.debug("Start to scroll to case:%s successfully" % case_name)
            self.device(text=case_name).click.wait()

            if self.device(text="OK").exists:
                self.device(text="OK").click.wait()

            if "BYOD Managed Provisioning" == case_name:
                if self.device(text="START BYOD PROVISIONING FLOW").wait.exists(timeout=5000):
                    self.device(text="START BYOD PROVISIONING FLOW").click()

                if self.device(text="DELETE").wait.exists(timeout=3000):
                    self.device(text="DELETE").click()

                if self.device(text="NEXT").wait.exists(timeout=5000):
                    self.device(text="NEXT").click()

                if self.device(text="OK").wait.exists(timeout=5000):
                    self.device(text="OK").click()

                if self.device(text="Setting up your work profile…").wait.exists(timeout=5000):
                    self.logger.debug("Setting up my work profile......")

                if self.device(text="BYOD Managed Provisioning").wait.exists(timeout=15000):
                    self.logger.debug("Setting up my work profile Completed")
                    self.device.delay(5)

            return True
        else:
            self.logger.warning("text '%s' not exists" % case_name)
            # count += 1
            # self.enter_CTSVerifier()
            # if count <= 3:
            # self.scroll_to_case(case_name, count)

        self.logger.debug("Start to scroll to case:%s failed" % case_name)
        return False

    def back_to_home(self):
        """back_to_home.
        """
        self.logger.debug("start to back to home")
        for loop in range(5):
            self.device.press.back()
            if self.device(packageName="com.blackberry.blackberrylauncher").exists:
                self.logger.debug("back to launcher successfully")
                break
            self.device.delay(1)
        self.device.delay(1)
        self.device.press.home()
        self.logger.debug("back to home completed")

    def back_to_verifier_home(self):
        """back_to_home.
        """
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        for loop in range(5):
            if self.device(text=cts_verifier).wait.exists(timeout=2000):
                self.logger.debug("back to CTS Verifier HomePage successfully")
                return True
            self.device.press.back()
            self.device.delay(1)

        self.logger.debug("back to CTS Verifier HomePage failed")
        self.logger.debug("Starting to Enter CTSVerifier again")
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        # self.logger.debug("cts_verifier is: %s" % cts_verifier)

        if self.device(text=cts_verifier).wait.exists(
                timeout=5000):
            self.logger.debug("Already in CTS Verifier HomePage")
            return True

        self.device.press.home()
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        for loop in range(5):
            if self.device(text=cts_verifier).wait.exists(timeout=5000):
                self.logger.debug("enter %s Successfully" % cts_verifier)
                return True
            self.device.press.back()
            self.device.delay(1)

        self.logger.warning("enter CTSVerifier failed")
        return False

    def back_to_verifier_home_sdevice(self):
        """back_to_home.
        """
        sdevice = self.sdevice
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        for loop in range(5):
            if sdevice(text=cts_verifier).wait.exists(timeout=5000):
                self.logger.debug("back to CTS Verifier HomePage successfully")
                return True
            sdevice.press.back()
            sdevice.delay(1)

        self.logger.debug("back to CTS Verifier HomePage failed")
        self.logger.debug("Starting to Enter CTSVerifier again")
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        # self.logger.debug("cts_verifier is: %s" % cts_verifier)

        if sdevice(text=cts_verifier).wait.exists(
                timeout=5000):
            self.logger.debug("Already in CTS Verifier HomePage")
            return True

        sdevice.press.home()
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        for loop in range(5):
            if sdevice(text=cts_verifier).wait.exists(timeout=5000):
                self.logger.debug("enter %s Successfully" % cts_verifier)
                return True
            sdevice.press.back()
            sdevice.delay(1)

        self.logger.warning("enter CTSVerifier failed")
        return False

    def back_to_app_sdevice(self, appname):
        """back_to_app homepage.
        """
        self.logger.debug("bact to Sdevice case:%s" % appname)
        for loop in range(6):
            if self.sdevice(text=appname).exists:
                self.logger.debug("Back to Sdevice %s HomePage successfully" % appname)
                return True
            self.sdevice.press.back()
            self.sdevice.delay(1)

        self.logger.warning("Back to Sdevice %s HomePage failed" % appname)
        return False

    def back_to_app(self, appname):
        """back_to_app homepage.
        """
        self.logger.debug("bact to case:%s" % appname)
        self.device.dump()
        # self.logger.debug("bact to applist:%s"%applist)
        for loop in range(6):
            if self.device(text=appname, packageName="com.android.cts.verifier").exists and not self.device(
                    text="PASS").exists:
                self.logger.debug("Back to %s HomePage successfully" % appname)
                return True
            self.device.press.back()
            self.device.delay(1)

        self.logger.warning("Back to %s HomePage failed" % appname)
        return False

    def enter_CTSVerifier(self):
        self.logger.debug("Starting to Enter CTSVerifier")
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        # self.logger.debug("cts_verifier is: %s" % cts_verifier)

        if self.sdevice(text=cts_verifier).wait.exists(
                timeout=3000):
            self.logger.debug("Already in CTS Verifier HomePage")
            return True

        self.sdevice.press.home()
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        for loop in range(5):
            if self.device(text=cts_verifier).wait.exists(timeout=5000):
                self.logger.debug("enter %s Successfully" % cts_verifier)
                return True
            self.device.press.back()
            self.device.delay(1)

        self.logger.warning("enter CTSVerifier failed")
        return False

    # def enter_CTSVerifier_sdevice(self):
    # self.logger.debug("Starting to Enter CTSVerifier")
    # cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
    # # self.logger.debug("cts_verifier is: %s" % cts_verifier)
    #
    # if self.sdevice(text=cts_verifier).wait.exists(
    # timeout=5000):
    #         self.logger.debug("Already in CTS Verifier HomePage")
    #         return True
    #
    #     self.sdevice.press.home()
    #     self.adb_sdevice.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
    #
    #     for loop in range(5):
    #         if self.sdevice(text=cts_verifier).wait.exists(timeout=5000):
    #             self.logger.debug("enter %s Successfully" % cts_verifier)
    #             return True
    #         self.sdevice.press.back()
    #         self.sdevice.delay(1)
    #
    #     self.logger.warning("enter CTSVerifier failed")
    #     return False

    def back_to_home_s(self):
        """back_to_home.
        """
        # for loop in range(4):
        #     self.sdevice.press.back()
        #     self.sdevice.delay(1)
        # self.sdevice.server.adb.shell("am start -n com.android.settings/com.android.settings.Settings")
        # self.sdevice.delay(1)
        # self.sdevice.press.home()

        self.logger.debug("start to back to home")
        for loop in range(5):
            self.sdevice.press.back()
            if self.sdevice(packageName="com.blackberry.blackberrylauncher").exists:
                self.logger.debug("back to launcher successfully")
                break
            self.sdevice.delay(1)
        self.sdevice.delay(1)
        self.sdevice.press.home()
        self.logger.debug("back to home completed")
    def is_playing_video(self):
        """check if video is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media.player")
        if not data:
            return None
        if "Client" in data:
            self.logger.debug("The video is playing now")
            return True
        else:
            self.logger.debug("The video is not playing.")
            return False

    def is_playing_music(self):
        """check if music is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media_session")
        if not data:
            return None
        if "state=PlaybackState {state=3" in data:
            self.logger.debug("The music is playing now")
            return True
        else:
            self.logger.debug("The music is not playing.")
            return False

    def clear_notification(self):
        self.logger.info("clear notification")
        i = 0
        while i < 3:
            if not self.device(resourceId="com.android.systemui:id/notification_container_parent").exists:
                self.logger.debug("Clear notifications successfully")
                return True
            if self.device(description="Clear all notifications.").exists:
                self.device(description="Clear all notifications.").click()
                self.logger.debug("click 'Clear all notifications.'")
                return True
            else:
                self.logger.debug("can not found 'Clear all notifications.',press back")
                self.device.press.back()
                self.device.delay(1)
            i += 1

    def enable_desallow_switch_and_open_settings(self):
        if self.device(resourceId="com.android.cts.verifier:id/switch_widget").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/switch_widget").click()
            self.logger.debug("enabled disallow switch_widget")
        if self.device(text="OPEN SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN SETTINGS").click()
            self.logger.debug("OPEN SETTINGS...")

    def allow_steps(self):
        self.logger.debug("starting to click allow button")
        count = 1
        while self.device(resourceId="com.android.packageinstaller:id/dialog_container").exists:
            if self.device(text="ALLOW").exists:
                self.device(text="ALLOW").click.wait()
            if self.device(resourceId="com.android.packageinstaller:id/permission_message").ext5:
                permission_message = self.device(
                    resourceId="com.android.packageinstaller:id/permission_message").get_text()
                self.logger.debug("'%s' successfully" % permission_message)
            count += 1
            if count > 6:
                self.logger.debug("skip allow steps failed")
                return False
            time.sleep(0.5)
        self.logger.debug("skip allow steps successfully")
        return True

    def install_credential(self,password="wwww"):
        self.logger.debug("starting to install 'myCA.cer'")

        if not self.device(text="Downloads").ext5:
            assert self.device(description="Show roots").wait.exists(timeout=5000)
            self.device(description="Show roots").click()

            assert self.device(text="Downloads").ext5
            self.device(text="Downloads").click()

        assert self.device(text="myCA.cer").ext5
        self.device(text="myCA.cer").click()
        self.logger.debug("select 'myCA.cer'")

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.wait(1)
            self.device.press.enter()
            self.device.delay(2)

        if self.device(resourceId="com.android.certinstaller:id/credential_name").wait.exists(timeout=5000):
            self.device(resourceId="com.android.certinstaller:id/credential_name").set_text("bug")
            self.device.press.enter()
        if self.device(text="OK").exists:
            self.device(text="OK").click()


    def enable_Location(self):
        self.logger.debug("Starting to enable Location")
        self.enter_settings("Security & location")
        self.scroll_to_text("Location")
        status = ""
        if self.device(resourceId="com.android.settings:id/switch_bar").ext5:
            status = self.device(resourceId="com.android.settings:id/switch_bar").get_text().lower()
        if status == "on":
            self.logger.debug("Location is already enable")
            return True
        if status == "off":
            self.device(resourceId="com.android.settings:id/switch_bar").click()
            self.device.delay(2)
            if self.device(text="ALLOW").exists:
                self.allow_steps()
            status_after = self.device(resourceId="com.android.settings:id/switch_bar").get_text().lower()

            if status_after == "on":
                self.logger.debug("Enable Location successfully")
                return True

        self.logger.debug("Enable Location Failed")
        self.save_fail_img()
        return False

    def scroll_to_text(self, option):
        self.logger.info("scroll to text:%s" % option)
        self.device.dump()
        if self.device(scrollable=True).wait.exists(timeout=2500):
            self.device(scrollable=True).scroll.vert.to(text=option)
        if self.device(text=option).ext5:
            self.device(text=option).click()
            self.logger.info("scroll to text:%s successfully" % option)
            return True
        self.logger.info("scroll to text:%s failed" % option)
        return False

    def enter_settings(self, option):
        '''enter the option of settings screen
         argv: the text of the settings option
        '''
        self.logger.debug("Starting to enter Settings->%s" % option)
        self.adb.shell("am start -n com.android.settings/.Settings")
        for loop in range(3):
            if self.device(resourceId="com.android.settings:id/dashboard_container",
                           packageName="com.android.settings").wait.exists(timeout=10000):
                self.logger.debug("Enter Settings successfully")
                if self.device(text=option).exists:
                    self.device(text=option).click()
                    self.logger.debug("Enter Settings->%s successfully" % option)
                    return True
                else:
                    if self.device(scrollable=True).ext5:
                        self.device(scrollable=True).scroll.vert.to(text=option)
                    if self.device(text=option).wait.exists(timeout=5000):
                        self.device(text=option).click()
                        self.logger.debug("Enter Settings->%s successfully" % option)
                        return True
            else:
                self.logger.debug("Enter Settings Failed,start Settings again.")
                self.start_app("Settings")
        self.logger.debug("Enter Settings->%s failed" % option)
        return False

    def clear_background(self):
        self.logger.info("clear the background")
        self.device.press.recent()
        for i in range(3):
            self.device.swipe(500, 230, 500, 1430, 10)
            self.device.delay(1)
        if self.device(text="CLEAR ALL").wait.exists(timeout=2000):
            self.device(text="CLEAR ALL").click()
        self.device.press.home()

    def delete_all_alarms(self):
        try:
            self.start_app("Clock")
            assert self.device(text="ALARM").ext5
            self.device(text="ALARM").click()

            for loop in range(10):
                if self.device(text="No Alarms").exists:
                    self.logger.debug("Delete all alarms")
                    break
                if self.device(resourceId="com.android.deskclock.bb:id/delete").exists:
                    self.device(resourceId="com.android.deskclock.bb:id/delete").click()
                if self.device(resourceId ="com.android.deskclock:id/arrow").exists:
                    self.device(resourceId ="com.android.deskclock:id/arrow").click()
                if self.device(text="Delete").exists:
                    self.device(text="Delete").click()
                if self.device(description="Expand alarm").exists:
                    self.device(description="Expand alarm").click()

            self.logger.debug("delete all alarms completed")
        except:
            self.save_fail_img()
            self.logger.warning(traceback.format_exc())

    def install_apk(self,serino,apkname):
        try:
            self.logger.debug(
                    "starting to install %s on device:%s"%(serino,apkname))
            p = subprocess.Popen("adb -s %s install -r %s" %(serino,apkname), shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            self.logger.debug("install %s completed"%apkname)
        except:
            self.logger.warning(traceback.format_exc())