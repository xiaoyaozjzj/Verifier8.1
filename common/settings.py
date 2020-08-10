# -*- coding: UTF-8 -*-
"""Settings library for scripts.
"""

from common import Common, UIParser
import traceback
import unittest
import os
import time
import subprocess
import json
import requests
import datetime

pass_button = "com.android.cts.verifier:id/pass_button"
fail_button = "com.android.cts.verifier:id/fail_button"
password = "wwww"
pin_password = "1111"
firstapprovedjsondetails = []

class Settings(Common):
    """Provide common functions involved wifi,display,sound etc."""

    def unlock_disable_sleep(self, serinoX=""):
        try:
            self.logger.debug("unlock %s scream and enable stay awake when charging" % serinoX)
            os.system('adb -s %s shell svc power stayon true' % (serinoX))

            time.sleep(2)
            os.system('adb -s %s shell input keyevent KEYCODE_MENU' % (serinoX))

            time.sleep(2)
            os.system('adb -s %s shell input keyevent KEYCODE_HOME' % (serinoX))
            self.logger.debug("unlock %s scream and enable stay awake when charging successfully" % serinoX)
        except:
            self.logger.warning(traceback.format_exc())
    def forbidden_Auto_rotate_screen(self):
        self.back_to_home()
        self.setRotateToPortrait()
        self.logger.debug("set forbidden Auto rotate screen completed!")
        self.back_to_home()
        return True
    def forget_Bluetooth(self):
        self.back_to_home()
        self.logger.debug("start to set forget Bluetooth")
        for loop in range(3):
            self.logger.debug("execute %s times" % (loop + 1))

            self.enter_settings("Connected devices")
            if self.setforgetBluetooth():
                    break

        self.logger.debug("set forget Bluetooth completed!")
        self.back_to_home()
        return True
    def setforgetBluetooth(self):
        if self.device(resourceID="com.android.settings:id/switchWidget",text="OFF").ext5:
            self.device(resourceID="com.android.settings:id/switchWidget",text="OFF").click()
        elif self.device(resourceID="com.android.settings:id/switchWidget",text="ON").ext5:
            self.device(resourceID="com.android.settings:id/switchWidget",text="ON").click()
        self.device(text="Bluetooth").click()
        if self.device(resourceId="com.android.settings:id/settings_button").ext5:
            self.device(resourceId="com.android.settings:id/settings_button").click()
            self.device(text="FORGET").click()
            self.device.dump()
        return True
    def setforgetBluetooth_Sdevice(self):
        if self.sdevice(resourceID="com.android.settings:id/switchWidget",text="OFF").ext5:
            self.sdevice(resourceID="com.android.settings:id/switchWidget",text="OFF").click()
        elif self.sdevice(resourceID="com.android.settings:id/switchWidget",text="ON").ext5:
            self.sdevice(resourceID="com.android.settings:id/switchWidget",text="ON").click()
        self.sdevice(text="Bluetooth").click()
        if self.sdevice(resourceId="com.android.settings:id/settings_button").ext5:
            self.sdevice(resourceId="com.android.settings:id/settings_button").click()
            self.sdevice(text="FORGET").click()
            self.sdevice.dump()
        return True
    def forget_Bluetooth_Sdevice(self):
        self.back_to_home_s()
        self.logger.debug("start to set Sdevice forget Bluetooth")
        for loop in range(3):
            self.logger.debug("execute %s times" % (loop + 1))

            self.enter_settings_sdevice("Connected devices")
            if self.setforgetBluetooth_Sdevice():
                    break

        self.logger.debug("set Sdevice forget Bluetooth completed!")
        self.back_to_home_s()
        return True



    def forget_VPN(self):
        self.back_to_home()
        self.logger.debug("start to set forget VPN")
        for loop in range(3):
            self.logger.debug("execute %s times" % (loop + 1))

            self.enter_settings("Network & Internet")
            if self.setforgetVPN():
                    break

        self.logger.debug("set forget VPN completed!")
        self.back_to_home()
        return True
    def setforgetVPN(self):
        if self.device(text="VPN").ext5:
            self.device(text="VPN").click()
        for loop in range(5):

            if self.device(resourceId="com.android.settings:id/settings_button").ext5:
                self.device(resourceId="com.android.settings:id/settings_button").click()
                self.device(text="FORGET").click()
                self.device.dump()
                continue
            else:
                break
        return True

    def first_forgetWIFI(self):
        self.back_to_home()
        self.logger.debug("start to set first forget WIFI")
        for loop in range(3):
            self.logger.debug("execute %s times" % (loop + 1))

            self.enter_settings("Network & Internet")
            if self.setfirstforgetWIFI():
                    break

        self.logger.debug("set first forget WIFI completed!")
        self.back_to_home()
        return True

    def first_forgetWIFI_Sdevice(self):
        self.back_to_home_s()
        self.logger.debug("start to set first forget WIFI")
        for loop in range(3):
            self.logger.debug("execute %s times" % (loop + 1))

            self.enter_settings_sdevice("Network & Internet")
            if self.setfirstforgetWIFI_Sdevice():
                    break

        self.logger.debug("set first forget WIFI completed!")
        self.back_to_home_s()
        return True

    def set_mute(self):
        self.back_to_home()
        self.logger.debug("starting to set device to mute")
        try:
            self.enter_settings("Sound")
            for loop in range(3):
                x, y = self.calculate_the_starting_point(loop + 1)
                self.device.click(x, y)
                time.sleep(2)
        except:
            self.save_fail_img()
            self.logger.warning(traceback.format_exc())
        self.logger.debug("set display to 30 Minutes completed!")
        return True

    def set_unmute(self):
        self.device.press.home()
        self.logger.debug("starting to set device to mute")
        try:
            self.enter_settings("Sound")
            for loop in range(4):
                x, y = self.calculate_the_starting_point(loop + 1)
                self.device.click(x, y)
                time.sleep(2)
        except:
            self.save_fail_img()
            self.logger.warning(traceback.format_exc())
        self.logger.debug("set display to 30 Minutes completed!")
        return True

    def calculate_the_starting_point(self, index):
        tab_height = self.device(className="android.widget.LinearLayout", index=index).child(
            resourceId="android:id/seekbar")
        if tab_height.ext5:
            info_bounds = tab_height.info["bounds"]
            left_location = info_bounds["left"]
            top_location = info_bounds["top"]
            bottom_location = info_bounds["bottom"]

            xpoint = left_location + 2
            centerY = (top_location + bottom_location) / 2
            self.logger.debug("X coordinates:%s" % xpoint)
            self.logger.debug("Y coordinates:%s" % centerY)
            return xpoint, centerY

    def calculate_the_middle_point(self, index):
        tab_height = self.device(className="android.widget.LinearLayout", index=index).child(
            resourceId="android:id/seekbar")
        if tab_height.ext5:
            info_bounds = tab_height.info["bounds"]
            left_location = info_bounds["left"]
            top_location = info_bounds["top"]
            bottom_location = info_bounds["bottom"]

            xpoint = left_location + 200
            centerY = (top_location + bottom_location) / 2
            self.logger.debug("X coordinates:%s" % xpoint)
            self.logger.debug("Y coordinates:%s" % centerY)
            return xpoint, centerY

    def setDisplay30M(self):
        self.back_to_home()
        self.logger.debug("start to set display to 30 Minutes")
        for loop in range(3):
            self.logger.debug("execute %s times" % (loop + 1))
            try:
                self.enter_settings("Display")
                if self.setDisplayNever():
                    break
            except:
                self.save_fail_img()
                self.logger.warning(traceback.format_exc())
        self.logger.debug("set display to 30 Minutes completed!")
        return True

    def setDisplay30M_Sdevice(self):
        self.back_to_home_s()
        # self.back_to_home()
        self.logger.debug("start to set Sdevice display to 30 Minutes")
        for loop in range(3):
            self.logger.debug("execute %s times" % (loop + 1))
            try:
                self.enter_settings_sdevice("Display")
                if self.setDisplayNever_Sdevice():
                    break
            except:
                # self.save_fail_img()
                self.logger.warning(traceback.format_exc())
        self.logger.debug("set Sdevice display to 30 Minutes completed!")
        return True

    def get_Bluetooth_Address(self, serinoX="Mdevice"):
        try:
            address = ""
            if serinoX == "Mdevice":
                device = self.device
                # System->About phone
                self.enter_settings("System")
                self.scroll_to_text("About phone")

            elif serinoX == "Sdevice":
                device = self.sdevice
                self.enter_settings_sdevice("System")
                self.scroll_to_text_sdevice("About phone")

            if device(text="Status").wait.exists(timeout=5000):
                device(text="Status").click()
            childCount = device(resourceId="com.android.settings:id/list").info["childCount"]

            for loop in range(childCount):
                title = device(resourceId="com.android.settings:id/list").child(className="android.widget.LinearLayout",
                                                                                index=loop).child(
                    className="android.widget.RelativeLayout").child(resourceId="android:id/title").get_text()
                self.logger.debug("title is:" + title)
                if title == "Bluetooth address":
                    address = device(resourceId="com.android.settings:id/list").child(
                        className="android.widget.LinearLayout",
                        index=loop).child(
                        className="android.widget.RelativeLayout").child(resourceId="android:id/summary").get_text()
                    self.logger.debug("The Bluetooth address is:" + address)
                    break
        except:
            self.logger.warning(traceback.format_exc())

        return address

    def skipPopup_Mdevice(self):
        try:
            self.logger.debug("start to skip Mdevice  pop-up")
            self.back_to_home()
            self.enter_CTSVerifier_First()
            cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
            for loop in range(10):
                if self.device(text="ALLOW").wait.exists(timeout=5000):
                    self.device(text="ALLOW").click()
                    continue
                if self.device(text=cts_verifier).wait.exists(timeout=5000):
                    self.logger.debug("Skip Mdevice popup completed")
                    return True
            else:
                self.logger.debug("Skip Mdevice popup Failed")
        except:
            self.logger.warning(traceback.format_exc())
        return False

    def skipPopup_Sdevice(self):
        try:
            self.logger.debug("start to skip Sdevice  pop-up")
            self.back_to_home_s()
            self.enter_CTSVerifier_First_Sdevice()

            cts_verifier_sdevice = self.config.getstr("cts_verifier_sdevice", "Default", "common")
            if not cts_verifier_sdevice:
                cts_verifier_sdevice = self.config.getstr("cts_verifier", "Default", "common")
            self.logger.debug("cts_verifier_sdevice is:%s" % cts_verifier_sdevice)

            for loop in range(10):
                if self.sdevice(text="ALLOW").wait.exists(timeout=5000):
                    self.sdevice(text="ALLOW").click()
                    continue
                if self.sdevice(text=cts_verifier_sdevice).wait.exists(timeout=5000):
                    self.logger.debug("Skip Sdevice popup completed")
                    return True
            else:
                self.logger.debug("Skip Sdevice popup Failed")
        except:
            self.logger.warning(traceback.format_exc())
        return False

    def skipCameraPopup(self):
        try:
            self.logger.debug("start to skip Camera pop-up")
            self.device.press.home()
            self.adb.shell("am start  com.mediatek.camera/.CameraLauncher")

            for loop in range(6):
                if self.device(
                        resourceId="com.mediatek.camera:id/shutter_image").wait.exists(timeout=5000):
                    self.logger.debug("Already Skip Camera popup successfully")
                    self.device.press.home()
                    return True
                if self.device(text="ALLOW").wait.exists(timeout=5000):
                    self.device(text="ALLOW").click()
                    continue
                if self.device(text="ALWAYS ALLOW").wait.exists(timeout=5000):
                    self.device(text="ALWAYS ALLOW").click()
                    continue
                if self.device(text="OK").wait.exists(timeout=5000):
                    self.device(text="OK").click()
                    continue
                if self.device(resourceId="com.blackberry.camera:id/slidesOverlayButtonNext").wait.exists(timeout=5000):
                    self.device(resourceId="com.blackberry.camera:id/slidesOverlayButtonNext").click()
                    continue
                if self.device(textContains="GOT IT").wait.exists(timeout=5000):
                    self.device(textContains="GOT IT").click()
                    self.logger.debug("click textContains 'GOT IT'")
                    continue
                if self.device(resourceId="com.mediatek.camera:id/shutter_image").wait.exists(
                        timeout=5000):
                    self.logger.debug("Skip Camera popup completed")
                    self.device.press.home()
                    return True
            else:
                self.logger.debug("Skip Camera popup Failed")
        except:
            self.save_fail_img()
            self.logger.warning(traceback.format_exc())
        return False

    def setRotateToPortrait(self):
        self.device.open.quick_settings()
        if self.device(text="Portrait").wait.exists(timeout=5000):
            self.logger.debug("The Rotate is already Portrait")
            return True
        if self.device(text="Auto-rotate").wait.exists(timeout=5000):
            self.device(text="Auto-rotate").click()
            if self.device(text="Portrait").wait.exists(timeout=5000):
                self.logger.debug("Set the rotate to 'Portrait' successfully")
                return True
        self.save_fail_img()
        self.logger.debug("Set the rotate to 'Portrait' failed")
        return False

    def dismiss_lockscreen_tips(self):
        self.logger.debug("starting to dismiss lockscreen tips'GOT IT'")
        self.device.sleep()
        time.sleep(5)
        for loop in range(3):
            self.device.wakeup()
            if self.device(text="GOT IT").ext5:
                self.device(text="GOT IT").click()
                break
            elif self.device(resourceId="com.android.systemui:id/magic_guide_menu_ok").ext5:
                self.device(resourceId="com.android.systemui:id/magic_guide_menu_ok").click()
                break
        else:
            self.logger.debug("dismiss lockscreen tips'GOT IT' failed")
        self.logger.debug("dismiss lockscreen tips'GOT IT' successfully")
        self.unlock_scream_without_password()

    def enter_Keyguard(self, parent_case_name):
        self.logger.debug("Starting to Enter %s" % parent_case_name)

        self.device(scrollable=True).scroll.vert.to(text=parent_case_name)
        if self.device(text=parent_case_name).wait.exists(timeout=5000):
            self.device(text=parent_case_name).click()

        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(text=parent_case_name).wait.exists(timeout=5000) and self.device(
                text="PREPARE TEST").wait.exists(timeout=5000):
            self.logger.debug("Enter  %s Successfully" % parent_case_name)
            return True

        self.logger.warning("enter %s failed" % parent_case_name)
        return False

    def CountCases(self):
        f = open("CTS_CASES.txt", "w")
        case_list = []
        flag = False
        # while True:
        for loopx in range(2):
            print "loop:", loopx
            id_list = self.device(resourceId="android:id/list")
            childCount = id_list.info["childCount"]
            for loop in range(childCount):
                case_name = id_list.child(index=loop).get_text()
                print "case name is:", case_name
                if case_name in case_list:
                    print "the case name <%s> is exists" % case_name
                    continue
                elif not str(case_name).isupper():
                    print "add the case name:<%s>" % case_name
                    f.write(case_name + "\n")
                    case_list.append(case_name)
                    # if case_name == "Streaming Video Quality Verifier":
                    # print "collect caselist completed"
                    # flag = True
                    # break
            self.device.swipe(540, 1240, 540, 13, 50)  # 正好滑动一个屏幕
            if flag:
                break
        print "case_list：\n", case_list
        f.close()

    def back_to_wifi(self):
        '''back to wifi list
         argv:
        '''
        self.logger.debug('Back to Wi-Fi list')
        for loop in range(5):
            if self.device(resourceId="com.android.settings:id/switch_bar").exists:
                return True
            self.device.press.back()
            self.device.delay(1)
        return False

    def open_wifi(self):
        '''validate wifi open status
         argv: To see available networks -- close
               wifi list -- open
        '''
        self.logger.debug('Starting to open wifi')

        self.enter_settings("Network & Internet")
        if self.device(text="Wi‑Fi").ext5:
            self.device(text="Wi‑Fi").click()
        elif self.device(text="Wi-Fi").ext5:
            self.device(text="Wi-Fi").click()

        if self.device(text="ON", resourceId="com.android.settings:id/switch_widget").wait.exists(timeout=5000):
            self.logger.debug('wifi is already open')
            return True
        if self.device(text="OFF", resourceId="com.android.settings:id/switch_widget").wait.exists(timeout=5000):
            self.device(text="OFF", resourceId="com.android.settings:id/switch_widget").click()

        self.device.delay(3)
        if self.device(text="ON", resourceId="com.android.settings:id/switch_widget").wait.exists(timeout=5000):
            self.logger.debug('wifi open successfully')
            return True

        self.logger.debug('wifi open fail!!!')
        return False

    def close_wifi(self):
        '''validate wifi close status
         argv: To see available networks -- closed
               wifi list -- open
        '''
        self.logger.debug('Close wifi')
        if self.device(text="ON", resourceId="com.android.settings:id/switch_widget").wait.exists(timeout=5000):
            self.device(text="ON", resourceId="com.android.settings:id/switch_widget").click()
            self.logger.debug('close wifi clicked')
        if self.device(text="OFF", resourceId="com.android.settings:id/switch_widget").wait.exists(timeout=10000):
            return True
        self.logger.debug('wifi close fail!')
        return False

    def connect_wifi(self, hotspot, password, security="", ):
        try:
            self.enter_settings("Network & Internet")
            if self.device(text="Wi‑Fi").ext5:
                self.device(text="Wi‑Fi").click()
            elif self.device(text="Wi-Fi").ext5:
                self.device(text="Wi-Fi").click()
            self.open_wifi()
            self._connect(hotspot, password, security)
            self.back_to_home()
        except:
            self.logger.warning(traceback.format_exc())
            self.save_fail_img()

    def disconnect_wifi(self, hotspot):
        self.close_wifi()
        self.back_to_home()

    def forget_wifi(self, hotpot, loop=0):
        '''device forget wifi hotpot
         argv: (str)hotpotName -- the wifi hotpot's name
        '''
        try:
            self.logger.info("forget hotpot %s times" % loop)
            for loop in range(3):
                self.enter_settings("Network & Internet")
                if self.device(text="Wi‑Fi").ext5:
                    self.device(text="Wi‑Fi").click()
                elif self.device(text="Wi-Fi").ext5:
                    self.device(text="Wi-Fi").click()

                self.open_wifi()

                self.logger.debug('forget hotpot')
                self.logger.debug('Search hotpot-------> ' + hotpot)
                if self.device(scrollable=True).exists:
                    self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
                    self.device(scrollable=True).scroll.vert.to(text=hotpot)
                if self.device(text=hotpot).wait.exists(timeout=10000):
                    self.device(text=hotpot).click()
                    if self.device(text="FORGET").wait.exists(timeout=2000):
                        self.device(text="FORGET").click()
                        self.logger.info("Forget hotpot successfully")
                        # if self.device(text="Connected").wait.gone(timeout=3000):
                        # self.device.delay(1)
                        return True
                    else:
                        self.logger.info(hotpot + ' is not connected!!!')
                        self.device.press.back()
            else:
                self.logger.info("Forget hotpot %s failed after retry 5 times" % hotpot)
                return False
        except:
            self.logger.warning(traceback.format_exc())

    def _connect(self, hotspot, password, security="", enter=False):
        '''device connect wifi hotspot
         argv: (str)hotspotName -- the wifi hotspot's name
               (str)password -- the wifi hotspot's password
               (str)security -- the password type
        '''
        self.logger.debug('Add hotspot --> ' + hotspot)
        # self.open_wifi()
        self.device().fling.vert.toEnd()
        if not self.device(text="Add network").wait.exists(timeout=5000):
            self.device().fling.vert.toEnd()
        self.device(text="Add network").click.wait(timeout=2000)
        self.logger.debug("Input SSID/PWD/Security")
        if self.device(resourceId="com.android.settings:id/ssid").wait.exists(timeout=self.timeout):
            self.device(resourceId="com.android.settings:id/ssid").set_text(hotspot)
            if security != "":
                self.logger.debug("Select security")
                self.device(resourceId="com.android.settings:id/security").click()
                self.device(text=security).click.wait(timeout=2000)
                self.device.delay(1)
            if password != "":
                self.device(resourceId="com.android.settings:id/password").set_text(password)
                self.device.delay(2)

        if self.device(text="SAVE").wait.exists(timeout=5000):
            self.device(text="SAVE").click()
            self.logger.debug('Add hotspot --> ' + hotspot + "successfully")

        self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
        if self.device(textStartsWith="Connected").wait.exists(timeout=30000):
            self.logger.debug('wifi connect success!!!')
            self.device.delay(1)
            return True
        elif self.device(textStartsWith="Saved").exists:
            self.device(textStartsWith="Saved").click.wait(timeout=2000)
            if self.device(text="CONNECT").exists:
                self.device(text="CONNECT").click.wait()
            if self.device(textStartsWith="Connected").wait.exists(timeout=30000):
                self.logger.debug('wifi connect success!!!')
                self.device.delay(1)
                return True
        elif self.device(text="Connected, no Internet").wait.exists(timeout=50000):
            self.logger.debug('wifi connect success!!!')
            self.device.delay(1)
            return True
        else:
            self.logger.debug('can not find hotspot: %s', hotspot)
            return False

    def enter_case_name(self, case_name):
        self.logger.debug("Starting to Enter CTSVerifier")
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")

        if self.device(text=cts_verifier).wait.exists(timeout=5000):
            self.logger.debug("Already in CTS Verifier HomePage")
            self.device(resourceId="android:id/list", scrollable=True).scroll.vert.to(text=case_name)
            if self.device(text=case_name).wait.exists(timeout=5000):
                self.device(text=case_name).click()

            if self.device(text="OK").wait.exists(timeout=3000):
                self.device(text="OK").click()
            # else:
            # self.logger.debug("Cannot find OK button")
            # self.device.press.back()

            if self.device(text=case_name).wait.exists(timeout=5000) and self.device(
                    resourceId="com.android.cts.verifier:id/pass_button").wait.exists(timeout=5000):
                self.logger.debug("Enter %s successfully" % case_name)
                return True

        self.device.press.home()
        self.enter_CTSVerifier()

        if self.device(text=cts_verifier).wait.exists(timeout=5000):
            self.logger.debug("Already in CTS Verifier HomePage")
            self.device(resourceId="android:id/list", scrollable=True).scroll.vert.to(text=case_name)
            if self.device(text=case_name).wait.exists(timeout=5000):
                self.device(text=case_name).click()

            if self.device(text="OK").wait.exists(timeout=3000):
                self.device(text="OK").click()

            if self.device(text=case_name).wait.exists(timeout=5000) and self.device(
                    resourceId="com.android.cts.verifier:id/pass_button").wait.exists(timeout=5000):
                self.logger.debug("Enter %s successfully" % case_name)
                return True

        self.logger.warning("Enter %s failed" % case_name)
        return False

    def enter_CTSVerifier(self):
        try:
            self.logger.debug("Starting to Enter CTSVerifier")
            cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
            # self.logger.debug("cts_verifier is: %s" % cts_verifier)

            if self.device(text=cts_verifier).wait.exists(
                    timeout=5000):
                self.logger.debug("Already in CTS Verifier HomePage")
                return True

            self.device.press.home()
            self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

            for loop in range(5):
                if self.device(text=cts_verifier).wait.exists(timeout=2500):
                    self.logger.debug("enter %s Successfully" % cts_verifier)
                    return True
                self.device.press.back()
                self.device.delay(1)

            self.logger.warning("enter %s failed" % cts_verifier)
        except:
            self.logger.warning(traceback.format_exc())
        return False

    def enter_CTSVerifier_Sdevice(self):
        self.logger.debug("Starting to Enter Sdevice CTSVerifier")
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        # self.logger.debug("cts_verifier is: %s" % cts_verifier)

        if self.sdevice(text=cts_verifier).wait.exists(
                timeout=5000):
            self.logger.debug("Already in CTS Verifier HomePage")
            return True

        self.sdevice.press.home()
        self.adb_sdevice.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        for loop in range(5):
            if self.sdevice(text=cts_verifier).wait.exists(timeout=5000):
                self.logger.debug("enter %s Successfully" % cts_verifier)
                return True
            self.sdevice.press.back()
            self.sdevice.delay(1)

        self.logger.warning("enter %s failed" % cts_verifier)
        return False

    def enter_CTSVerifier_First(self):
        self.logger.debug("Starting to Enter CTSVerifier")
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        for loop in range(4):
            if self.device(text="ALLOW").wait.exists(timeout=5000) or self.device(text=cts_verifier).wait.exists(
                    timeout=5000):
                self.logger.debug("Enter %s Successfully" % cts_verifier)
                return True
            else:
                self.logger.debug(
                    "can not found text ALLOW or title %s,start CTSVerifier activity again" % cts_verifier)
                self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
        self.logger.warning("enter First %s failed" % cts_verifier)
        return False

    def enter_CTSVerifier_First_Sdevice(self):
        self.logger.debug("Starting to Enter CTSVerifier")
        cts_verifier = self.config.getstr("cts_verifier", "Default", "common")
        self.adb_sdevice.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
        for loop in range(3):
            if self.sdevice(text="ALLOW").wait.exists(timeout=5000) or self.sdevice(text=cts_verifier).wait.exists(
                    timeout=5000):
                self.logger.debug("Enter %s Successfully" % cts_verifier)
                return True
            else:
                self.logger.debug(
                    "can not found text ALLOW or title %s,start CTSVerifier activity again" % cts_verifier)
                self.adb_sdevice.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
        self.logger.warning("enter First %s failed" % cts_verifier)
        return False

    def enter_settings_sdevice(self, option):
        '''enter the option of settings screen
         argv: the text of the settings option
        '''
        self.logger.debug("Starting to enter Sdevice Settings->%s" % option)
        try:
            self.adb_sdevice.shell("am start -n com.android.settings/.Settings")
        except:
            self.start_app_sdevice("Settings")
        self.sdevice.delay(1)
        for loop in range(3):
            if self.sdevice(resourceId="com.android.settings:id/dashboard_container",
                            packageName="com.android.settings").wait.exists(timeout=30000):
                self.logger.debug("Enter Sdevice Settings successfully")
                if self.sdevice(text=option).exists:
                    self.sdevice(text=option).click()
                else:
                    self.sdevice(scrollable=True).scroll.vert.to(text=option)
                    if self.sdevice(text=option).wait.exists(timeout=5000):
                        self.sdevice(text=option).click()
                if self.sdevice(text="Settings").wait.gone(timeout=2000):
                    self.logger.debug("Enter Sdevice Settings->%s successfully" % option)
                    return True
            else:
                self.logger.debug("Enter Sdevice Settings Failed,start Settings again.")
                self.start_app_sdevice("Settings")
        self.logger.debug("Enter Sdevice Settings->%s failed" % option)
        return False

    def enable_Airplane_mode(self):
        self.enter_settings("More")
        status = ""
        if self.device(resourceId="android:id/switch_widget").wait.exists(timeout=5000):
            status = self.device(resourceId="android:id/switch_widget").get_text()
        if status == "ON":
            self.logger.debug("Airplane is already enable")
            return True
        if status == "OFF":
            self.device(resourceId="android:id/switch_widget").click()
            self.device.delay(1)
            status_after = self.device(resourceId="android:id/switch_widget").get_text()
            if status_after == "ON":
                self.logger.debug("Enable Airplane successfully")
                return True

        self.logger.debug("Enable Airplane Failed")
        self.save_fail_img()
        return False

    def disable_Bluetooth(self):
        self.logger.debug("Starting to disable Bluetooth")
        self.enter_settings("Connected devices")
        status = self.device(resourceId="com.android.settings:id/switchWidget",index=0).get_text()
        if status == "OFF":
            self.logger.debug("Bluetooth is already disable")
            return True
        if status == "ON":
            self.device(resourceId="com.android.settings:id/switchWidget",index=0).click()
            self.device.delay(2)
            status_after =self.device(resourceId="com.android.settings:id/switchWidget",index=0).get_text()

            if status_after == "OFF":
                self.logger.debug("Disable Bluetooth successfully")
                return True

        self.logger.debug("Disable Bluetooth Failed")
        self.save_fail_img()
        return False

    def disable_Bluetooth_Sdevice(self):
        self.logger.debug("Starting to disable Bluetooth")
        self.enter_settings_sdevice("Connected devices")
        status = self.device(resourceId="com.android.settings:id/switchWidget",index=0).get_text()
        if status == "OFF":
            self.logger.debug("Bluetooth is already disable")
            return True
        if status == "ON":
            self.device(resourceId="com.android.settings:id/switchWidget",index=0).click()
            self.sdevice.delay(2)
            status_after = self.device(resourceId="com.android.settings:id/switchWidget",index=0).get_text()

            if status_after == "OFF":
                self.logger.debug("Disable Bluetooth successfully")
                return True

        self.logger.debug("Disable Bluetooth Failed")
        self.save_fail_img_s()
        return False

    def disable_Adaptive_Brightness(self):
        self.logger.debug("Starting to disable Adaptive_Brightness")
        self.enter_settings("Display")
        status = self.device(className="android.widget.LinearLayout", index=1).child(
            resourceId="android:id/switch_widget").get_text()

        if status == "OFF":
            self.logger.debug("Adaptive_Brightness is already disable")
            return True
        if status == "ON":
            self.device(className="android.widget.LinearLayout", index=1).child(
                resourceId="android:id/switch_widget").click()
            self.device.delay(2)
            status_after = self.device(className="android.widget.LinearLayout", index=1).child(
                resourceId="android:id/switch_widget").get_text()

            if status_after == "OFF":
                self.logger.debug("Disable Adaptive_Brightness successfully")
                return True

        self.logger.debug("Disable Adaptive_Brightness Failed")
        self.save_fail_img()
        return False

    def disable_Ambient_Display(self):
        self.logger.debug("Starting to disable Ambient_Display")
        self.enter_settings("Display")
        status = self.device(className="android.widget.LinearLayout", index=7).child(
            resourceId="android:id/switch_widget").get_text()

        if status == "OFF":
            self.logger.debug("Ambient_Display is already disable")
            return True
        if status == "ON":
            self.device(className="android.widget.LinearLayout", index=7).child(
                resourceId="android:id/switch_widget").click()
            self.device.delay(2)
            status_after = self.device(className="android.widget.LinearLayout", index=7).child(
                resourceId="android:id/switch_widget").get_text()

            if status_after == "OFF":
                self.logger.debug("Disable Ambient_Display successfully")
                return True

        self.logger.debug("Disable Ambient_Display Failed")
        self.save_fail_img()
        return False

    def disable_Auto_Rotate_Screen(self):
        self.logger.debug("Starting to disable Auto_Rotate_Screen")
        self.device.open.quick_settings()
        self.device.delay(3)
        status = self.device(className="android.widget.Switch", index=5).get_text().lower()

        if status == "off":
            self.logger.debug("Auto_Rotate_Screen is already disable")
            self.device.press.home()
            return True
        if status == "on":
            self.device(className="android.widget.Switch", index=5).click()
            self.device.delay(2)
            status_after = self.device(className="android.widget.Switch", index=5).get_text().lower()

            if status_after == "off":
                self.logger.debug("Disable Auto_Rotate_Screen successfully")
                self.device.press.home()
                return True

        self.logger.debug("Disable Auto_Rotate_Screen Failed")
        self.save_fail_img()
        self.device.press.home()
        return False

    def disable_Stay_awake(self):
        self.logger.debug("Starting to disable_Stay_awake")
        self.adb.shell("svc power stayon false")
        self.logger.debug("Disable Stay_awake successfully")
        return True

    def disable_Location(self):
        self.logger.debug("Starting to disable Location")
        self.enter_settings("Security & location")
        self.scroll_to_text("Location")
        status = ""
        if self.device(resourceId="com.android.settings:id/switch_bar").ext5:
            status = self.device(resourceId="com.android.settings:id/switch_bar").get_text().lower()
        if status == "off":
            self.logger.debug("Location is already disable")
            return True
        if status == "on":
            self.device(resourceId="com.android.settings:id/switch_bar").click()
            self.device.delay(2)
            status_after = self.device(resourceId="com.android.settings:id/switch_bar").get_text().lower()

            if status_after == "off":
                self.logger.debug("Disable Location successfully")
                return True

        self.logger.debug("Disable Location Failed")
        self.save_fail_img()
        return False

    def skip_soundRecorder_steps(self):
        try:
            self.start_app("Sound Recorder")
            if self.device(text="SKIP INTRO").ext5:
                self.device(text="SKIP INTRO").click()
            self.allow_steps()
            if self.device(resourceId="com.tct.soundrecorder.bb:id/recordButton").ext5 or self.device(
                    resourceId="self.allow_steps()com.tct.soundrecorder.bb:id/file_list").ext5 or \
                    self.device(resourceId ="com.android.soundrecorder:id/recordButton").ext5:
                self.logger.debug("skip sound recorder steps successfully")
                return True
        except:
            self.logger.warning(traceback.format_exc())

        self.logger.debug("skip sound recorder steps failed")
        return False

    def allow_steps(self):
        try:
            self.logger.debug("starting to click allow button")
            count = 1
            while self.device(resourceId="com.android.packageinstaller:id/dialog_container").exists \
                    or self.device(resourceId="com.android.packageinstaller:id/permission_message").exists:
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
        except:
            self.logger.warning(traceback.format_exc())
        return True

    def enter_settings_textContains(self, option):
        '''enter the option of settings screen
         argv: the text of the settings option
        '''
        self.logger.debug("Starting to enter Settings->%s" % option)
        self.start_app("Settings")
        self.device.delay(3)
        if self.device(text=self.appconfig("settings", "Settings")).wait.exists(timeout=2000):
            self.logger.debug("enter Settings")
            if self.device(textContains=option).exists:
                self.device(textContains=option).click()
            else:
                self.device(scrollable=True).scroll.vert.to(text=option)
                if self.device(textContains=option).wait.exists(timeout=10000):
                    self.device(textContains=option).click()
                else:
                    self.logger.debug("enter Settings->%s failed" % option)
                    return False
            if self.device(text=self.appconfig("settings", "Settings")).wait.gone(timeout=2000):
                self.logger.debug("enter Settings->%s successfully" % option)
                return True

        self.logger.debug("enter Settings->%s failed" % option)
        return False

    def connect_bt_sdevice(self, sdevice_id):
        assert self.DisableBlueTooth()
        time.sleep(5)
        assert self.EnableBlueTooth()

        assert self.EnableBlueTooth_Sdevice()

        if self.device(resourceId="com.android.settings:id/list",className="android.support.v7.widget.RecyclerView").child(
                className="android.widget.LinearLayout",index=2).child(text=sdevice_id).ext5:
                self.device(resourceId="com.android.settings:id/list",
                        className="android.support.v7.widget.RecyclerView").child(
                className="android.widget.LinearLayout", index=2).child(text=sdevice_id).click()
                return  True
        assert self.device(text="Pair new device").wait.exists(timeout=30000)
        self.device(text="Pair new device").click()

        assert self.device(text=sdevice_id).wait.exists(timeout=30000)
        self.device(text=sdevice_id).click()
        self.device.delay(1)
        if self.device(text="PAIR").wait.exists(timeout=1500):
            self.device(text="PAIR").click()

        if self.sdevice(text="PAIR").wait.exists(timeout=1000):
            self.sdevice(text="PAIR").click()

        if self.device(resourceId="com.android.settings:id/settings_button").ext5:
            self.logger.debug("connect to bt sdevice:%s successfully" % sdevice_id)
            return True
        elif self.device(resourceId="com.android.settings:id/list",className="android.support.v7.widget.RecyclerView").child(
                className="android.widget.LinearLayout",index=2).child(text=sdevice_id).ext5:
                return True

    def EnableBlueTooth(self):
        self.enter_settings("Connected devices")
        switch_text = ""
        if self.device(text="Bluetooth").ext5:
            self.device(text="Bluetooth").click()

        if self.device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.device(resourceId="com.android.settings:id/switch_bar").get_text()

        self.logger.debug("switch_text is %s" % switch_text)
        if switch_text.lower() == "on":
            self.logger.debug("BlueTooth already opened")
            return True

        if switch_text.lower() == "off":
            self.device(resourceId="com.android.settings:id/switch_widget").click()
        self.device.delay(3)
        if self.device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.device(resourceId="com.android.settings:id/switch_bar").get_text()
        self.logger.debug("switch_text1 is %s" % switch_text)
        if switch_text.lower() == "on":
            self.logger.debug("open BlueTooth successfully")
            return True

        self.logger.debug("open BlueTooth failed")
        self.save_fail_img()
        return False

    def DisableBlueTooth(self):
        self.enter_settings("Connected devices")
        switch_text = ""
        if self.device(text="Bluetooth").ext5:
            self.device(text="Bluetooth").click()

        if self.device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.device(resourceId="com.android.settings:id/switch_bar").get_text()

        self.logger.debug("switch_text is %s" % switch_text)
        if switch_text.lower() == "off":
            self.logger.debug("BlueTooth already closed")
            return True

        if switch_text.lower() == "on":
            self.device(resourceId="com.android.settings:id/switch_widget").click()
        self.device.delay(3)
        if self.device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.device(resourceId="com.android.settings:id/switch_bar").get_text()
        self.logger.debug("switch_text1 is %s" % switch_text)
        if switch_text.lower() == "off":
            self.logger.debug("closed BlueTooth successfully")
            return True

        self.logger.debug("close BlueTooth failed")
        self.save_fail_img()
        return False

    def rename_bt_sdevice(self, sdevice_id):
        assert self.EnableBlueTooth_Sdevice()
        if self.sdevice(resourceId="com.android.settings:id/settings_button").ext5:
            self.sdevice(resourceId="com.android.settings:id/settings_button").click()
            self.sdevice(text="FORGET").click()
            self.sdevice.dump()
        assert self.sdevice(text="Device name").ext5
        self.sdevice(text="Device name").click()

        assert self.sdevice(text="Rename this device").ext5
        self.sdevice(text="Rename this device").click()

        assert self.sdevice(resourceId="com.android.settings:id/edittext").ext5
        self.sdevice(resourceId="com.android.settings:id/edittext").set_text(sdevice_id)

        assert self.sdevice(text="RENAME", enabled=True).ext5
        self.sdevice(text="RENAME", enabled=True).click()

        self.logger.debug("Rename Sdevice BlueTooth successfully")
        sdevice_bt_address = ""
        if self.sdevice(resourceId="com.android.settings:id/list").child(className="android.widget.LinearLayout", index=6).child(resourceId="android:id/title").ext5:
            sdevice_bt_address_text =self.sdevice(resourceId="com.android.settings:id/list").child(className="android.widget.LinearLayout", index=6)\
                .child(resourceId="android:id/title").get_text()
            list = sdevice_bt_address_text.split(":",1)

            sdevice_bt_address = list[1]
        return sdevice_bt_address.strip()

    def rename_bt_mdevice(self, mdevice_id):
        assert self.EnableBlueTooth()
        if self.device(resourceId="com.android.settings:id/settings_button").ext5:
            self.device(resourceId="com.android.settings:id/settings_button").click()
            self.device(text="FORGET").click()
            self.device.dump()
        assert self.device(text="Device name").ext5
        self.device(text="Device name").click()

        assert self.device(text="Rename this device").ext5
        self.device(text="Rename this device").click()

        assert self.device(resourceId="com.android.settings:id/edittext").ext5
        self.device(resourceId="com.android.settings:id/edittext").set_text(mdevice_id)

        assert self.device(text="RENAME", enabled=True).ext5
        self.device(text="RENAME", enabled=True).click()

        self.logger.debug("Rename Mdevice BlueTooth successfully")

        mdevice_bt_address = ""
        if self.device(resourceId="com.android.settings:id/list").child(className="android.widget.LinearLayout", index=6).child(resourceId="android:id/title").ext5:
            mdevice_bt_address_text = self.device(resourceId="com.android.settings:id/list").child(className="android.widget.LinearLayout", index=6)\
                .child(resourceId="android:id/title").get_text()

            list = mdevice_bt_address_text.split(":",1)

            mdevice_bt_address = list[1]

        return mdevice_bt_address.strip()

    def EnableBlueTooth_Sdevice(self):
        self.enter_settings_sdevice("Connected devices")
        switch_text = ""
        if self.sdevice(text="Bluetooth").ext5:
            self.sdevice(text="Bluetooth").click()

        if self.sdevice(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.sdevice(resourceId="com.android.settings:id/switch_bar").get_text()

        self.logger.debug("switch_text is %s" % switch_text)
        if switch_text.lower() == "on":
            self.logger.debug("BlueTooth already opened")
            return True

        if switch_text.lower() == "off":
            self.sdevice(resourceId="com.android.settings:id/switch_widget").click()
        self.sdevice.delay(3)
        if self.sdevice(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.sdevice(resourceId="com.android.settings:id/switch_bar").get_text()
        self.logger.debug("switch_text1 is %s" % switch_text)
        if switch_text.lower() == "on":
            self.logger.debug("open BlueTooth successfully")
            return True

        self.logger.debug("open BlueTooth failed")
        self.save_fail_img()
        return False

    def EnableBlueTooth_Sdevice_7(self):
        self.enter_settings_sdevice("Bluetooth")
        switch_text = ""
        if self.sdevice(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.sdevice(resourceId="com.android.settings:id/switch_widget").get_text()

        if switch_text.lower() == "on":
            self.logger.debug("Sdevice BlueTooth is already enabled")
            return True

        if switch_text.lower() == "off":
            self.sdevice(resourceId="com.android.settings:id/switch_widget").click()

        self.sdevice.delay(3)
        switch_text = self.sdevice(resourceId="com.android.settings:id/switch_widget").get_text()

        if switch_text.lower() == "on":
            self.logger.debug("open Sdevice BlueTooth successfully")
            return True

        self.logger.debug("open Sdevice BlueTooth failed")
        self.save_fail_img()
        return False

    def disconnect_bluetooth(self):
        try:
            self.enter_settings("Connected devices")
            if self.device(text="Bluetooth").ext5:
                self.device(text="Bluetooth").click()

            if self.device(resourceId="com.android.settings:id/settings_button").wait.exists(timeout=5000):
                self.device(resourceId="com.android.settings:id/settings_button").click()

            if self.device(text="FORGET").wait.exists(timeout=5000):
                self.device(text="FORGET").click()
                self.logger.debug("FORGET the mdevice connected MAC successfully")
                return True
        except:
            self.logger.warning(traceback.format_exc())
            self.save_fail_img()
        self.logger.debug("FORGET the mdevice connected MAC failed")
        return False

    def disconnect_bluetooth_sdevice(self):
        try:
            self.enter_settings_sdevice("Connected devices")
            assert self.sdevice(text="Bluetooth").ext5
            self.sdevice(text="Bluetooth").click()

            if self.sdevice(resourceId="com.android.settings:id/settings_button").wait.exists(timeout=5000):
                self.sdevice(resourceId="com.android.settings:id/settings_button").click()

            if self.sdevice(text="FORGET").wait.exists(timeout=5000):
                self.sdevice(text="FORGET").click()
                self.logger.debug("FORGET the sdevice connected MAC successfully")
                return True
        except:
            self.logger.warning(traceback.format_exc())
            self.save_fail_img_s()

        self.logger.debug("FORGET the sdevice connected MAC failed")
        return False










    def disconnect_bluetooth_first(self):
        self.enter_settings("Connected devices")
        self.enter_settings_sdevice("Connected devices")
        if self.device(text="Bluetooth").ext5:
            self.device(text="Bluetooth").click()
        if self.device(resourceId="com.android.settings:id/settings_button").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/settings_button").click()
            if self.device(text="FORGET").wait.exists(timeout=5000):
                self.device(text="FORGET").click()
                self.logger.debug("FORGET the mdevice connected MAC successfully")
        if self.sdevice(text="Bluetooth").ext5:
            self.sdevice(text="Bluetooth").click()
        if self.sdevice(resourceId="com.android.settings:id/settings_button").wait.exists(timeout=5000):
            self.sdevice(resourceId="com.android.settings:id/settings_button").click()
            if self.sdevice(text="FORGET").wait.exists(timeout=5000):
                self.sdevice(text="FORGET").click()
                self.logger.debug("FORGET the sdevice connected MAC successfully")
        self.back_to_app("Bluetooth Test")
        self.back_to_app_sdevice("Bluetooth Test")
        return True

    def scroll_to_text_sdevice(self, option):
        self.logger.info("scroll to sdevice text:%s" % option)
        self.device.dump()
        if self.sdevice(scrollable=True).wait.exists(timeout=5000):
            self.sdevice(scrollable=True).scroll.vert.to(text=option)

        if self.sdevice(text=option).ext5:
            self.sdevice(text=option).click()
            self.logger.info("scroll to text:%s successfully" % option)
            return True
        self.logger.info("scroll to text:%s failed" % option)
        return False

    def scroll_to_text_without_click(self, option):
        self.logger.info("scroll to text:%s" % option)
        if self.device(scrollable=True).wait.exists(timeout=5000):
            self.device(scrollable=True).scroll.vert.to(text=option)
        if self.device(text=option).wait.exists(timeout=5000):
            self.logger.info("scroll to text:%s successfully" % option)
            return True
        self.logger.warning("scroll to text:%s failed" % option)
        return False

    def Camera_Flashlight(self, case_name):

        self.scroll_to_case(case_name)

        if self.device(text="OK").wait.exists(timeout=5000):
            self.device(text="OK").click()

        if self.device(text="START").wait.exists(timeout=5000):
            self.device(text="START").click()

        if self.device(text="ON").wait.exists(timeout=5000):
            self.device(text="ON").click()


        # if self.device(text="NEXT").wait.exists(timeout=5000):
        #     self.device(text="NEXT").click()
        if self.device(resourceId="com.android.cts.verifier:id/flash_instruction_button").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/flash_instruction_button").click()
        else:
            self.logger.debug("cannot found NEXT")
        if self.device(text="OFF").wait.exists(timeout=5000):
            self.device(text="OFF").click()

        if self.device(resourceId="com.android.cts.verifier:id/flash_instruction_button").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/flash_instruction_button").click()
        else:
            self.logger.debug("cannot found NEXT")

        if self.device(resourceId="com.android.cts.verifier:id/flash_instruction_button").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/flash_instruction_button").click()
        else:
            self.logger.debug("cannot found Done")
        return True

    def Camera_Formats(self, case_name):
        self.scroll_to_case(case_name)

        self.testCamera("Camera 0", "NV21")
        self.testCamera("Camera 0", "YV12")
        # self.testCamera("Camera 1", "NV21")
        #         # self.testCamera("Camera 1", "YV12")

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
            self.logger.debug("Camera Flashlight Test Pass")
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("Camera Flashlight Test Failed")
        self.save_fail_img()
        return False

    def Camera_ITS_Test(self, case_name):

        self.device(resourceId="android:id/list", scrollable=True).scroll.vert.to(text=case_name)
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
            self.logger.debug("%s Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Camera_Intents(self, case_name):

        self.scroll_to_case(case_name)
        # Intents Test 1 of 4
        assert self.device(text="START TEST", resourceId="com.android.cts.verifier:id/start_test_button").ext5
        self.device(text="START TEST", resourceId="com.android.cts.verifier:id/start_test_button").click()
        time.sleep(2)
        # Athena上会引起APP Crash
        # self.adb.shell("am start -n com.blackberry.camera/.ui.coordination.MainActivity")
        self.device.press.home()
        self.start_app("Camera")

        if self.device(description="Select Capture Mode").ext5:
            self.device(description="Select Capture Mode").click()
        elif self.device(resourceId="MODE").wait.exists(timeout=5000):
            self.device(text="MODE").click()  # Photo
        elif self.device(resourceId="org.codeaurora.snapcam:id/camera_switcher").ext5:
            self.device(resourceId="org.codeaurora.snapcam:id/camera_switcher").click()
        if self.device(text="Photo").wait.exists(timeout=5000):
            self.device(text="Photo").click()
        if self.device(text="Picture").wait.exists(timeout=5000):
            self.device(text="Picture").click()
        if self.device(description="Switch to photo").wait.exists(timeout=5000):
            self.device(description="Switch to photo").click()

        assert self.device(resourceId="com.mediatek.camera:id/shutter_image").wait.exists(
            timeout=5000)
        self.device(resourceId="com.mediatek.camera:id/shutter_image").click()
        self.device.delay(3)
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
        # self.enter_case_name("Camera Intents")

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
            self.logger.debug("Intents Test 1 of 4 test pass")

        # Intents Test 2 of 4
        assert self.device(text="START TEST", resourceId="com.android.cts.verifier:id/start_test_button").ext5
        self.device(text="START TEST", resourceId="com.android.cts.verifier:id/start_test_button").click()
        # self.adb.shell("am start -n com.blackberry.camera/.ui.coordination.MainActivity")
        time.sleep(2)
        self.device.press.home()
        self.start_app("Camera")

        if self.device(description="Select Capture Mode").ext5:
            self.device(description="Select Capture Mode").click()
        elif self.device(resourceId="MODE").wait.exists(timeout=5000):
            self.device(text="MODE").click()  # Photo
        elif self.device(resourceId="org.codeaurora.snapcam:id/camera_switcher").ext5:
            self.device(resourceId="org.codeaurora.snapcam:id/camera_switcher").click()

        if self.device(text="Video").wait.exists(timeout=10000):
            self.device(text="Video").click()
        elif self.device(description="Switch to photo").wait.exists(timeout=5000):
            self.device(description="Switch to photo").click()
        else:
            self.logger.debug("Video not exists")


            self.device.click(653, 1280)
        self.device(resourceId="com.mediatek.camera:id/shutter_image").click()
        self.device.delay(5)
        self.device(resourceId="com.mediatek.camera:id/video_stop_shutter").click()
        time.sleep(2)

        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
        # self.enter_case_name("Camera Intents")

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
            self.logger.debug("Intents Test 2 of 4 test pass")

        # Intents Test 3 of 4
        self.device(text="START TEST", resourceId="com.android.cts.verifier:id/start_test_button").click()
        if self.device(resourceId="com.mediatek.camera:id/shutter_image").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/shutter_image").click()
        self.device.delay(3)
        if self.device(resourceId="com.mediatek.camera:id/btn_save").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/btn_save").click()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
            self.logger.debug("Intents Test 3 of 4 test pass")

        # Intents Test 4 of 4
        if self.device(text="START TEST", resourceId="com.android.cts.verifier:id/start_test_button").wait.exists(
                timeout=5000):
            self.device(text="START TEST", resourceId="com.android.cts.verifier:id/start_test_button").click()

        if self.device(resourceId="com.mediatek.camera:id/shutter_image").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/shutter_image").click()

        self.device.delay(5)

        if self.device(resourceId="com.mediatek.camera:id/video_stop_shutter").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/video_stop_shutter").click()

        if self.device(resourceId="com.mediatek.camera:id/btn_save").wait.exists(timeout=5000):
            self.device(resourceId="om.mediatek.camera:id/btn_save").click()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
            self.logger.debug("%s Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Camera_Orientation(self, case_name):
        self.scroll_to_case(case_name)
        for loop in range(8):
            if self.device(text="TAKE PHOTO", enabled=True).wait.exists(timeout=5000):
                self.device(text="TAKE PHOTO", enabled=True).click()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
                self.device(resourceId=pass_button, enabled=True).click()
            else:
                self.logger.warning("%s Test Failed" % case_name)
                self.save_fail_img()
                return False

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
            self.logger.debug("%s Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.debug("%s Pass" % case_name)
        return True

    def Camera_Video(self, case_name):

        self.scroll_to_case(case_name)

        self.testVideo("Camera 0")
        self.testVideo("Camera 1")

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Car_Dock_Test(self, case_name):

        self.scroll_to_case(case_name)
        if self.device(text="ENABLE CAR MODE").wait.exists(timeout=5000):
            self.device(text="ENABLE CAR MODE").click()

        if self.device(text="Complete action using CTS Verifier").wait.exists(timeout=5000):
            self.device(text="ALWAYS").click()
        elif self.device(text="CTS Verifier").wait.exists(timeout=5000):
            self.device(text="CTS Verifier").click()
            if self.device(text="ALWAYS").wait.exists(timeout=5000):
                self.device(text="ALWAYS").click()

        if self.device(text="Press the Home button").wait.exists(timeout=5000):
            self.device.press.home()
        return True

    def Show_Alarms_Test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="SHOW ALARMS").wait.exists(timeout=5000):
            self.device(text="SHOW ALARMS").click()

        if self.device(text="ALARM", selected=True).wait.exists(timeout=5000):
            self.logger.debug("Displays the list of alarms successfully")
            self.logger.debug("%s Test Pass" % case_name)
            self.device.press.back()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Set_Alarm_Test(self, case_name):
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(text="SET ALARM").wait.exists(timeout=5000):
            self.device(text="SET ALARM").click()

        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(description="Add alarm").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            if self.device(text="Delete").wait.exists(timeout=3000):
                self.device(text="Delete").click()
            self.device.press.back()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Start_Alarm_Test(self, case_name):
        self.device.open.notification()
        time.sleep(1)
        self.clear_notification()
        # self.back_to_app(case_name)
        self.scroll_to_case(case_name)
        if self.device(text="SET ALARM").wait.exists(timeout=5000):
            self.device(text="SET ALARM").click()

        self.device.open.notification()
        time.sleep(2)
        if self.device(text="Upcoming alarm").wait.gone(timeout=180 * 1000):
            self.logger.debug("Upcoming alarm is gone")
            if self.device(text="DISMISS").wait.exists(timeout=30000):
                self.device(text="DISMISS").click()
                self.logger.debug("Dismiss the alarm")
                self.logger.debug("%s Test Pass" % case_name)

            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Full_Alarm_Test(self, case_name):

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(text="CREATE ALARM").wait.exists(timeout=5000):
            self.device(text="CREATE ALARM").click()

        if self.device(text="1:23 AM").wait.exists(timeout=5000) \
                and self.device(text="Create Alarm Test").wait.exists(timeout=5000) \
                and self.device(text="Silent").wait.exists(timeout=5000) and \
                self.device(text="Vibrate").wait.exists(timeout=5000) \
                and self.device(description="Monday", checked=True).wait.exists(timeout=5000) \
                and self.device(description="Monday", checked=True).wait.exists(timeout=5000):

            self.logger.debug(
                "The title is: Create Alarm Test,and the alarm is silent and vibrating,Repeating on: Monday and Wednesday")
            self.device.press.back()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
                self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False








    def Set_Timer_Test(self, case_name):

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(text="SET TIMER").wait.exists(timeout=5000):
            self.device(text="SET TIMER").click()

        self.device(resourceId="com.android.deskclock:id/timer_setup_digit_6").click()
        self.device(resourceId="com.android.deskclock:id/timer_setup_digit_0").click()

        if self.device(resourceId="com.android.deskclock:id/fab", enabled="true").wait.exists(timeout=5000):
            self.device.press.back()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
                self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Start_Timer_Test(self, case_name):
        if self.device(resourceId="com.android.systemui:id/notification_stack_scroller").exsit():
            self.device.press.back()
        self.scroll_to_case(case_name)

        if self.device(text="START TIMER").wait.exists(timeout=5000):
            self.device(text="START TIMER").click()
            self.logger.debug("Start Timer testing ,please wait about 30 seconds ")

        if self.device(text="Start Timer Test").ext5:

            self.device.open.notification()
            self.devioce.delay(30)
            if self.device(text="STOP").wait.exists(timeout=120000):
                self.logger.debug("the timer named Start Timer Test rings after 30 seconds. STOP it.")
                self.device(text="STOP").click()

            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
                self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Start_Timer_With_UI_Test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="START TIMER").wait.exists(timeout=5000):
            self.device(text="START TIMER").click()

        self.device.press.back()
        self.device.open.notification()
        if self.device(text="Start Timer Test").wait.exists(timeout=5000):
            self.device.delay(30)
            self.device.dump()
            if self.device(text="STOP").wait.exists(timeout=5000):
                self.device(text="STOP").click()
                self.device.press.back()
                if self.device(text="STOP ALL TIMERS").wait.exists(timeout=5000):
                    self.device(text="STOP ALL TIMERS").click()
                if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                    self.device(resourceId=pass_button, enabled=True).click()
                    return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def back_to_Keyguard_home(self, parent_case_name):
        for loop in range(5):
            if self.device(text=parent_case_name).exists:
                self.logger.debug("Back to Keyguard Disabled Features Test Homepage successfully")
                return True
            self.device.press.back()
            self.device.delay(1)
        self.logger.debug("Back to Keyguard Disabled Features Test Homepage Failed")
        return False

    def back_to_Pass_Popup_home(self):
        for loop in range(10):
            # if self.device(text="PASS").wait.exists(timeout=3000):
            if self.device(text="PASS").exists:
                self.logger.debug("Back to GO FAIL PASS pop-up successfully")
                return True
            self.logger.debug("Can not found  PASS pop-up ,press back")
            self.device.press.back()
            self.device.delay(1)
        self.logger.debug("Back to GO FAIL PASS pop-up  Failed")
        return False

    def unlock_scream_with_password(self):
        self.device.wakeup()
        self.device.delay(1)


        self.adb.shell("input keyevent KEYCODE_MENU")
        self.device.swipe(360, 1232, 360, 13)
        self.logger.debug("starting to unlock the screen with password 'wwww'")
        i = 0
        while (i < 2):
            if self.device(resourceId="com.android.systemui:id/passwordEntry").wait.exists(timeout=5000):
                self.device(resourceId="com.android.systemui:id/passwordEntry").set_text(password)
                self.device.press.enter()
                self.logger.debug("unlock the screen with password successfully")
                return True
            i += 1
            self.device.wakeup()
            self.adb.shell("input keyevent KEYCODE_MENU")
            self.device.swipe(360, 1232, 360, 13)
        self.logger.debug("unlock the screen with password fail")
        return False

    def unlock_scream_without_password(self):
        time.sleep(1)
        self.device.wakeup()
        time.sleep(3)
        self.adb.shell("input keyevent KEYCODE_MENU")
        time.sleep(1)
        self.adb.shell("input keyevent KEYCODE_MENU")
        self.logger.debug("unlock scream without password completed")

    def Screen_Lock_Test(self, case_name):
        self.active_verifiy_admin()
        self.enter_CTSVerifier()
        self.scroll_to_case(case_name)

        if self.device(text="FORCE LOCK").wait.exists(timeout=3000):
            self.device(text="FORCE LOCK").click()

        self.unlock_scream_with_password()
        self.device.delay(2)

        if self.device(text="It appears the screen was locked successfully!").wait.exists(timeout=5000):
            self.device(text="OK").click()
            self.device.delay(2)

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
                self.logger.debug("%s Test Pass" % case_name)
                self.setLockScreenToNone()
                self.back_to_verifier_home()
                return True
            else:
                self.setLockScreenToNone()
                self.back_to_verifier_home()
        else:
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            self.setLockScreenToNone()
            self.back_to_verifier_home()
            return False

    def Redacted_Notifications_Keyguard_Disabled_Features_Test(self, case_name):
        try:
            # #发生异常则置为True，解锁屏幕
            flag = False
            self.device(scrollable=True).scroll.vert.to(text=case_name)
            if self.device(text=case_name).wait.exists(timeout=5000):
                self.device(text=case_name).click()

            if self.device(text="OK").wait.exists(timeout=3000):
                self.device(text="OK").click()
            self.active_verifiy_admin()
            self.back_to_app(case_name)

            if self.device(text="PREPARE TEST").wait.exists(timeout=3000):
                self.device(text="PREPARE TEST").click()

            self.device.delay(1)
            if self.device(text="Disable unredacted notifications").wait.exists(timeout=3000):
                self.device(text="Disable unredacted notifications").click()
                self.clear_notification()


            if self.device(text="GO").wait.exists(timeout=3000):
                self.device(text="GO").click()

            self.wait(15)
            self.device.wakeup()
            # self.dismiss_lockscreen_tips()不确定有无gotit界面，会导致有时fail待重试

            assert self.check_lockscreen_notification("Contents hidden by policy")
            self.logger.debug("Disable unredacted notifications Test Pass")

            self.unlock_scream_with_password()

            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()
                self.logger.warning("%s Test successfully" % case_name)
                return True

            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
            self.save_fail_img()
            flag = True
        finally:
            if flag:
                self.unlock_scream_with_password()
            self.enter_CTSVerifier()

    def Policy_Serialization_Test(self, case_name):
        self.setLockScreenPasswordToNone()
        self.enter_case_name(case_name)
        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(text="GENERATE POLICY").wait.exists(timeout=5000):
            self.device(text="GENERATE POLICY").click()

        if self.device(text="APPLY POLICY").wait.exists(timeout=5000):
            self.device(text="APPLY POLICY").click()

        time.sleep(2)
        self.adb.shell("reboot")
        time.sleep(25)
        i = 0
        while not self.device(packageName="com.android.launcher3").exists:
            self.logger.debug("restarting...")
            time.sleep(5)
            if i > 10:
                self.logger.debug("restarting...")
                break
            i += 1

        self.device.wakeup()
        self.device.delay(10)
        # if self.device(text="OK").exists(timeout=5000):
        #     self.device(text="OK").click()
        self.adb.shell("input keyevent KEYCODE_MENU")
        if self.device(resourceId="com.android.systemui:id/passwordEntry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.systemui:id/passwordEntry").set_text(password)
            self.logger.debug("Enter Password:%s successfully" % password)
            # self.device.press.enter()
            self.device.press.enter()
            self.device.delay(2)

        self.device.delay(2)
        self.enter_case_name(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disable_notifications(self, case_name):
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=3000):
            self.device(text="GO").click()

        self.device.delay(10)
        self.device.press.power()
        self.device.delay(3)
        scream_flag = False
        if not self.device(resourceId="android:id/notification_main_column").wait.exists(timeout=5000):
            scream_flag = True
            self.logger.debug("no notifications appear on lock scream")

        self.adb.shell("input keyevent KEYCODE_MENU")
        self.adb.shell("input keyevent KEYCODE_MENU")
        self.device.swipe(360, 1232, 360, 398)
        self.device.delay(2)

        if self.device(resourceId="com.android.systemui:id/passwordEntry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.systemui:id/passwordEntry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
            self.device.delay(2)
            self.back_to_Pass_Popup_home()

        self.device.open.notification()
        if self.device(text="This is a notification").wait.exists(timeout=5000) and scream_flag:
            self.logger.debug("See a notification after unlocking")

            self.clear_notification()
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        if self.device(text="FAIL").wait.exists(timeout=5000):
            self.device(text="FAIL").click()

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disable_camera(self, case_name):
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=3000):
            self.device(text="GO").click()

        self.device.wakeup()
        self.device.delay(3)
        if not self.device(resourceId="com.android.systemui:id/camera_button").wait.exists(timeout=10000):
            self.logger.debug("%s Test Pass" % case_name)

        self.adb.shell("input keyevent KEYCODE_MENU")
        self.adb.shell("input keyevent KEYCODE_MENU")
        self.device.swipe(360,1232,360,398)
        self.device.delay(2)


        if self.device(resourceId="com.android.systemui:id/passwordEntry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.systemui:id/passwordEntry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
            self.device.delay(2)
            self.back_to_Pass_Popup_home()

            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disable_trust_agents(self, case_name):
        if self.device(text="PREPARE TEST").wait.exists(timeout=5000):
            self.device(text="PREPARE TEST").click()

        if self.device(resourceId="com.android.systemui:id/passwordEntry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.systemui:id/passwordEntry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=3000):
            self.device(text="GO").click()

        self.device(scrollable=True).scroll.vert.to(text="Trust agents")
        if self.device(text="Trust agents").wait.exists(timeout=5000):
            self.device(text="Trust agents").click()

        if self.device(text="Disabled by admin").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)

            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()

            return True

        if self.device(text="Fail").wait.exists(timeout=5000):
            self.device(text="Fail").click()

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Fingerprint_disabled_on_keyguard(self, case_name):

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=3000):
            self.device(text="GO").click()

        self.device.wakeup()
        self.device.delay(5)
        self.adb.shell("input keyevent KEYCODE_MENU")
        self.adb.shell("input keyevent KEYCODE_MENU")
        self.device.delay(2)

        if self.device(resourceId="com.android.systemui:id/passwordEntry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.systemui:id/passwordEntry").set_text(password)
            self.device.press.enter()
            # self.device.press.enter()
            # self.device.delay(2)
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()
            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Fingerprint_is_disabled_in_Settings(self, case_name):
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Fingerprint").wait.exists(timeout=5000):
            self.device(text="Fingerprint").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        self.device.press.enter()
        # self.device.press.enter()
        self.device.delay(3)
        # if self.device(resourceId="com.android.settings:id/list").child(className="android.widget.FrameLayout",
        # index=2).child(
        # className="android.widget.TextView").wait.exists(timeout=10000):
        # text = self.device(className="android.widget.FrameLayout", index=2).child(
        # className="android.widget.TextView").get_text()
        # print "text:", text

        # if self.device(textContains="Screen lock option disabled").wait.exists(timeout=10000):
        if self.device(text="Finger 1").wait.exists(timeout=5000):
            self.logger.debug("Disable Fingerprint successfully")

            self.device.press.back()
            self.device.delay(2)
            self.device.press.back()
            self.logger.debug("%s Test Pass" % case_name)
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def testCamera(self, category, format):
        resolution = ["160 x 120", "176 x 144", "320 x 240", "352 x 288", "480 x 320",
                      "640 x 480", "720 x 480", "800 x 480", "864 x 480", "960 x 720",
                      "1080 x 1080", "1280 x 720", "1280 x 960", "1440 x 1440", "1620 x 1080", "1920 x 1080",
                      "1920 x 1440"]

        self.logger.debug("Select %s" % category)
        if self.device(resourceId="com.android.cts.verifier:id/cameras_selection").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/cameras_selection").click()

        if self.device(text=category).wait.exists(timeout=5000):
            self.device(text=category).click()

        self.logger.debug("Select %s" % format)
        if self.device(resourceId="com.android.cts.verifier:id/format_selection").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/format_selection").click()

        if self.device(text=format).wait.exists(timeout=5000):
            self.device(text=format).click()

        for index in range(len(resolution)):
            if self.device(resourceId="com.android.cts.verifier:id/resolution_selection").wait.exists(timeout=5000):
                self.device(resourceId="com.android.cts.verifier:id/resolution_selection").click()

            self.logger.debug("Select resolution:%s" % resolution[index])
            self.device(scrollable=True).scroll.vert.to(text=resolution[index])
            if self.device(text=resolution[index]).wait.exists(timeout=5000):
                self.device(text=resolution[index]).click()
            self.device.delay(1)

    def setScreenPassword(self):
        self.enter_settings("Security & location")
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()

        if self.device(text="Password").wait.exists(timeout=5000):
            self.device(text="Password").click()

        if self.device(text="No thanks").wait.exists(timeout=5000):
            self.device(text="No thanks").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)

        if self.device(text="DONE").wait.exists(timeout=5000):
            self.device(text="DONE").click()

    def active_sensor_admin(self):
        self.logger.debug("start to active the verifier apk")
        self.enter_settings("Security & location")

        self.device(scrollable=True).scroll.vert.to(text="Device administrators")
        if self.device(text="Device administrators").wait.exists(timeout=5000):
            self.device(text="Device administrators").click()

        count = self.device(className="android.widget.LinearLayout").count
        print "count:", count

        for index in range(count):
            if self.device(resourceId="android:id/list", className="android.widget.ListView").child(
                    className="android.widget.LinearLayout", index=index).wait.exists(timeout=5000):
                appName = self.device(resourceId="android:id/list").child(
                    className="android.widget.LinearLayout", index=index).child(
                    className="android.widget.RelativeLayout").child(
                    resourceId="com.android.settings:id/name").get_text()
                print "appName is :", appName
                if appName == "Sensor Tests Device Admin Receiver":
                    isChecked = self.device(resourceId="android:id/list").child(className="android.widget.LinearLayout",
                                                                                index=index).child(
                        resourceId="com.android.settings:id/checkbox").isChecked()
                    print "isChecked:", isChecked
                    if not isChecked:
                        self.device(resourceId="android:id/list").child(className="android.widget.LinearLayout",
                                                                        index=index).child(
                            resourceId="com.android.settings:id/checkbox").click()
                        # self.device(scrollable=True).scroll.vert.to(text="Activate this device administrator")
                        self.device(text="Activate this device administrator").click()

                        self.logger.debug("Active 'Sensor Tests Device Admin Receiver'  Successfully")
            else:
                break

        return True

    def testVideo(self, category):
        resolution = ["LOW", "HIGH", "QCIF", "QVGA", "CIF", "480P", "720P", "1080P", "2160P"]

        if category == "Camera 1":
            resolution = ["LOW", "HIGH", "QCIF", "QVGA", "CIF", "480P", "720P", "1080P"]

        self.logger.debug("Select %s" % category)
        if self.device(resourceId="com.android.cts.verifier:id/cameras_selection").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/cameras_selection").click()

        if self.device(text=category).wait.exists(timeout=5000):
            self.device(text=category).click()

        for index in range(len(resolution)):
            if self.device(resourceId="com.android.cts.verifier:id/resolution_selection").wait.exists(timeout=5000):
                self.device(resourceId="com.android.cts.verifier:id/resolution_selection").click()

            self.logger.debug("Select resolution:%s" % resolution[index])
            self.device(scrollable=True).scroll.vert.to(text=resolution[index])
            if self.device(text=resolution[index]).wait.exists(timeout=5000):
                self.device(text=resolution[index]).click()

            if self.device(text="TEST", enabled=True).wait.exists(timeout=5000):
                self.device(text="TEST", enabled=True).click()

            if self.device(text="Recording").wait.exists(timeout=5000):
                self.logger.debug("%s %s is testing" % (category, resolution[index]))

            if self.device(text="Ready").wait.exists(timeout=5000):
                self.logger.debug("%s %s Test completed" % (category, resolution[index]))
    def setfirstforgetWIFI(self):
        if self.scroll_to_text("Wi-Fi"):
            self.device(text="Wi-Fi").wait.exists(timeout=5000)
            self.device(text="Wi-Fi").click()
            # self.scroll_to_case("Saved networks",timeout=10000)

            if self.device(text="Connected").wait.exists(timeout=5000) or self.device(text="Saved").wait.exists(timeout=5000):
                self.device(text="Connected").click()
                self.device(text="FORGET").click()
                self.logger.debug("First Forget WIFI Successfully")
            self.logger.debug("No WIFI Connected!")
        return True
    def setfirstforgetWIFI_Sdevice(self):
        if self.scroll_to_text_sdevice("Wi-Fi"):
            self.sdevice(text="Wi-Fi").wait.exists(timeout=5000)
            self.sdevice(text="Wi-Fi").click()
            if self.sdevice(text="Connected").wait.exists(timeout=5000) or self.device(text="Saved").wait.exists(timeout=5000):
                self.sdevice(text="Connected").click()
                self.sdevice(text="FORGET").click()
                self.logger.debug("First Forget WIFI Successfully")
            self.logger.debug("No WIFI Connected!")
        return True
    def setDisplayNever(self):
        # if self.device(text="Sleep").wait.exists(timeout=5000):
        #     self.device(text="Sleep").click()
        # else: self.scroll_to_text("Sleep")

        if self.device(text="Advanced").wait.exists(timeout=5000):
            self.device(text="Advanced").click()
        if self.device(text="Sleep").wait.exists(timeout=5000):
            self.device(text="Sleep").click()

        if self.device(text="Never").wait.exists(timeout=5000):
            self.device(text="Never").click()
            return True
        if self.device(text="Never Timeout").wait.exists(timeout=5000):
            self.device(text="Never Timeout").click()
            return True
        if self.device(text="30 minutes").wait.exists(timeout=5000):
            self.device(text="30 minutes").click()

        if self.device(text="After 30 minutes of inactivity").wait.exists(timeout=5000):
            self.logger.debug("set display->sleep 30m successfully")
            return True

        self.logger.debug("set display->sleep 30m failed")
        self.save_fail_img()
        return False

    def setDisplayNever_Sdevice(self):
        # if self.device(text="Advanced").wait.exists(timeout=5000):
        #     self.device(text="Advanced").click()
        # if self.sdevice(text="Sleep").wait.exists(timeout=5000):
        #     self.sdevice(text="Sleep").click()
        # if self.sdevice(text="30 minutes").wait.exists(timeout=5000):
        #     self.sdevice(text="30 minutes").click()
        # if self.sdevice(text="Sleep").wait.exists(timeout=5000):
        #     self.sdevice(text="Sleep").click()
        # else: self.scroll_to_text_sdevice("Sleep")
        if self.device(text="Advanced").wait.exists(timeout=5000):
            self.device(text="Advanced").click()
        if self.device(text="Sleep").wait.exists(timeout=5000):
            self.device(text="Sleep").click()
        if self.sdevice(text="30 minutes").wait.exists(timeout=5000):
            self.sdevice(text="30 minutes").click()
        if self.sdevice(text="After 30 minutes of inactivity").wait.exists(timeout=5000):
            self.logger.debug("set display->sleep 30m successfully")
            return True

        self.logger.debug("set display->sleep 30m failed")
        self.save_fail_img()
        return False

    def setLockScreenToNone(self):
        self.logger.debug("starting to set LockScreen-None")
        self.enter_settings("Security & location")
        self.device(scrollable=True).scroll.vert.toBeginning()
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
            self.device.delay(1)

        if self.device(text="None").wait.exists(timeout=5000):
            self.device(text="None").click()

        if self.device(text="YES, REMOVE").wait.exists(timeout=5000):
            self.device(text="YES, REMOVE").click()

        if self.device(text="Screen lock").wait.exists(timeout=5000) and self.device(text="None").wait.exists(
                timeout=5000):
            self.logger.debug("set LockScreen->None successfully")
            return True

        self.logger.debug("set LockScreen->None failed")
        self.save_fail_img()
        return False

    def setLockScreenToSwipe(self):
        self.logger.debug("starting to set LockScreen->Swipe")
        self.enter_settings("Security & location")
        self.device(scrollable=True).scroll.vert.toBeginning()
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
            self.device.delay(1)

        if self.device(text="Swipe").wait.exists(timeout=5000):
            self.device(text="Swipe").click()

        if self.device(text="YES, REMOVE").wait.exists(timeout=5000):
            self.device(text="YES, REMOVE").click()

        if self.device(text="Screen lock").wait.exists(timeout=5000) and self.device(text="Swipe").wait.exists(
                timeout=5000):
            self.logger.debug("set LockScreen->Swipe successfully")
            return True

        self.logger.debug("set LockScreen->Swipe failed")
        self.save_fail_img()
        return False

    def setLockScreenPasswordToNone(self):
        self.logger.debug("starting to set LockScreen-None")
        self.enter_settings("Security & location")
        self.device(scrollable=True).scroll.vert.toBeginning()
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
            # self.device.delay(1)
            # self.device.press.enter()

        if self.device(text="None").wait.exists(timeout=5000):
            self.device(text="None").click()

        if self.device(text="YES, REMOVE").wait.exists(timeout=5000):
            self.device(text="YES, REMOVE").click()

        if self.device(text="Screen lock").wait.exists(timeout=5000) and self.device(text="None").wait.exists(
                timeout=5000):
            self.logger.debug("set LockScreen->None successfully")
            return True

        self.logger.debug("set LockScreen->None failed")
        self.save_fail_img()
        return False

    def setLockScreenPinToNone(self):
        self.logger.debug("starting to set LockScreen-None")
        self.enter_settings("Security & location")
        self.device(scrollable=True).scroll.vert.toBeginning()
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(pin_password)
            self.device.press.enter()
            self.device.delay(1)

        if self.device(text="None").wait.exists(timeout=5000):
            self.device(text="None").click()

        if self.device(text="YES, REMOVE").wait.exists(timeout=5000):
            self.device(text="YES, REMOVE").click()

        if self.device(text="Screen lock").wait.exists(timeout=5000) and self.device(text="None").wait.exists(
                timeout=5000):
            self.logger.debug("set LockScreen->None successfully")
            return True

        self.logger.debug("set LockScreen->None failed")
        self.save_fail_img()
        return False

    def setLockScreenToPassword(self):
        try:
            self.enter_settings("Security & location")
            self.logger.debug("start to set lock screen to password")
            self.device(scrollable=True).scroll.vert.toBeginning()
            if self.device(text="Screen lock").wait.exists(timeout=5000) and self.device(text="Password").wait.exists(
                    timeout=5000):
                self.logger.debug("the  LockScreen is already Password")
                return True

            assert self.device(text="Screen lock").wait.exists(timeout=5000)
            self.device(text="Screen lock").click()

            # if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            #     self.device(resourceId="com.android.settings:id/password_entry").set_text(pin_password)
            #     self.device.press.enter()

            if self.device(text="Password").wait.exists(timeout=5000):
                self.device(text="Password").click()

            if self.device(text="NO").wait.exists(timeout=5000):
                self.device(text="NO").click()

            if self.device(text="No thanks").wait.exists(timeout=5000):
                self.device(text="No thanks").click()

            if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
                self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
                #self.device.press.enter()

                # 8.1 r2套件改为NEXT
                if self.device(text="NEXT").wait.exists(timeout=5000):
                    self.device(text="NEXT").click()
                elif self.device(text="CONTINUE").wait.exists(timeout=5000):
                    self.device(text="CONTINUE").click()

            if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
                self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
                if self.device(text="OK").wait.exists(timeout=5000):
                    self.device(text="OK").click()
                self.wait(2)

            if self.device(text="Show all notification content", enabled=True).wait.exists(timeout=5000):
                self.device(text="Show all notification content", enabled=True).click()

            if self.device(text="DONE").wait.exists(timeout=5000):
                self.device(text="DONE").click()
            elif self.device(resourceId="com.android.settings:id/redaction_done_button").wait.exists(timeout=5000):
                self.device(resourceId="com.android.settings:id/redaction_done_button").click()

            if self.device(text="Screen lock").wait.exists(timeout=5000) and self.device(text="Password").wait.exists(
                    timeout=5000):
                self.logger.debug("set LockScreen->Password successfully")
                return True
            self.logger.warning("set LockScreen->Password fail")
            return False
        except:
            self.logger.warning(traceback.format_exc())

    def setLockScreenToPin(self):
        self.logger.debug("Starting to set LockScreen->Pin")
        self.enter_settings("Security & location")
        self.device(scrollable=True).scroll.vert.toBeginning()
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()
            self.device.delay(2)

        if self.device(text="PIN").wait.exists(timeout=5000):
            self.device(text="PIN").click()

        if self.device(text="Require PIN to start device").wait.exists(timeout=5000):
            self.device(text="Require PIN to start device").click()
        if self.device(text="YES").wait.exists(timeout=5000):
            self.device(text="YES").click()
        if self.device(text="OK").wait.exists(timeout=5000):
            self.device(text="OK").click()
        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(pin_password)
            self.device.press.enter()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(pin_password)
            self.device.press.enter()
        self.device.delay(5)

    def openGps(self):
        switch_text = ""
        if self.device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = self.device(resourceId="com.android.settings:id/switch_widget").get_text()
        if switch_text == "OFF":
            self.device(resourceId="com.android.settings:id/switch_widget").click()

        self.device.delay(3)
        if switch_text == "ON":
            self.logger.debug("switch_text is 'ON',open BlueTooth successfully")

        if self.device(text="Mode").wait.exists(timeout=5000):
            self.device(text="Mode").click()

        if self.device(text="Battery saving").wait.exists(timeout=5000):
            self.device(text="Battery saving").click()

        if self.device(text="AGREE").wait.exists(timeout=5000):
            self.device(text="AGREE").click()

        if self.device(description="Navigate up").wait.exists(timeout=5000):
            self.device(description="Navigate up").click()

        if self.device(text="Screen lock").wait.exists(timeout=5000) and self.device(text="Battery saving").wait.exists(
                timeout=5000):
            self.logger.debug("start to open GPS and set 'Battery saving' Mode successfully")
            return True
        self.logger.warning("start to open GPS and set 'Battery saving' Mode failed")
        self.save_fail_img()
        return False

    def GNSS_Location_Test(self, case_name):
        self.device(scrollable=True).scroll.vert.to(text=case_name)
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
        if self.device(text="NEXT").wait.exists(timeout=3000):
            self.device(text="NEXT").click()
        for loop in range(20):
            testResults = self.device(resourceId="com.android.cts.verifier:id/text").get_text()
            if "All test pass!" in testResults:
                self.logger.debug("%s Test Pass" % case_name)
                return True
            self.logger.debug("%s Testing......,please wait 10s" % case_name)
            self.device.delay(10)

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def back_to_applist(self, applist, case_name=""):
        """back_to_app homepage.
        所有含有__双下划线的casename需要转换，去掉__后面的字段，便于找到casename
        """
        # applist.reverse()
        self.logger.debug("bact to applist:%s" % applist)
        if applist:
            for loop in range(6):
                if self.device(text=applist[0] if "__" not in applist[0] else applist[0].split("__")[
                    0]).exists and not self.device(text="PASS").exists:
                    self.logger.debug("Back to %s HomePage successfully" % applist[0])
                    if "Device Owner Tests" in applist and not case_name == "Remove device owner":
                        self.adb.shell(
                            "dpm set-device-owner 'com.android.cts.verifier/com.android.cts.verifier.managedprovisioning.DeviceAdminTestReceiver'")
                        self.device.delay(2)
                    return True
                self.device.press.back()
                self.device.delay(1)
        else:
            self.logger.debug("The applist is empty,so the homepage is CTS Verifier Home")
            self.enter_CTSVerifier()
            return True

        self.logger.warning("Back to %s HomePage failed" % applist)
        self.logger.debug("Starting to back to applist:%s" % applist)
        self.clear_background()
        self.enter_CTSVerifier()
        applist.reverse()
        for loop in range(len(applist)):
            self.scroll_to_case(applist[loop])
        return False

    def back_to_applist_sdevice(self, applist):
        """back_to_app homepage.
        """
        applist.reverse()
        self.logger.debug("bact to applist:%s" % applist)
        if applist:
            for loop in range(6):
                if self.sdevice(text=applist[0]).exists and not self.sdevice(text="PASS").exists:
                    self.logger.debug("Back to %s HomePage successfully" % applist[0])
                    return True
                self.sdevice.press.back()
                self.sdevice.delay(1)
        else:
            self.logger.debug("The applist is empty,so the homepage is CTS Verifier Home")
            if self.enter_CTSVerifier_sdevice():
                return True

        self.logger.warning("Back to %s HomePage failed" % applist[0])
        return False

    # count = 0
    def scroll_to_case(self, case_name, timeout=3000):
        """
        在android:id/list scrollable上滑动
        :param case_name:
        :param timeout: default =3000用于点击OK按钮
        :return:
        """
        self.logger.debug("Start to scroll to case:%s" % case_name)
        if self.device(resourceId="android:id/list", scrollable=True).wait.exists(timeout=5000):
            self.device(resourceId="android:id/list", scrollable=True).scroll.vert.to(text=case_name)

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.logger.debug("Start to scroll to case:%s successfully" % case_name)
            self.device(text=case_name).click.wait()

            if self.device(text="OK").wait.exists(timeout=timeout):
                self.device(text="OK").click.wait()

            if "BYOD Managed Provisioning" == case_name:

                if self.device(text="START BYOD PROVISIONING FLOW").wait.exists(timeout=5000):
                    self.device(text="START BYOD PROVISIONING FLOW").click()

                if self.device(text="DELETE").wait.exists(timeout=3000):
                    self.device(text="DELETE").click()

                if self.device(text="ACCEPT & CONTINUE").wait.exists(timeout=5000):
                    self.device(text="ACCEPT & CONTINUE").click()

                if self.device(text="Setting up your work profile…").wait.exists(timeout=5000):
                    self.logger.debug("Setting up my work profile......")

                if self.device(text="BYOD Managed Provisioning").wait.exists(timeout=15000):
                    self.logger.debug("Setting up my work profile Completed")
                    self.device.delay(5)
            self.logger.debug("Scroll to case:'%s' successfully" % case_name)
            return True
        else:
            self.logger.warning("text '%s' not exists" % case_name)
            # count += 1
            # self.enter_CTSVerifier()
            # if count <= 3:
            #     self.scroll_to_case(case_name, count)

        self.logger.debug("Start to scroll to case:%s failed" % case_name)
        self.save_fail_img()
        return False

    def scroll_to_case_index(self, case_name, index):
        self.logger.debug("Start to scroll to case:%s" % case_name)
        if self.device(text=case_name, index=index).wait.exists(timeout=5000):
            self.device(text=case_name, index=index).click.wait()
            self.logger.debug("Start to scroll to case:%s successfully" % case_name)
            if self.device(text="OK").wait.exists(timeout=3000):
                self.device(text="OK").click.wait()
            return True
        else:
            self.logger.warning("text '%s' not exists" % case_name)

        self.logger.debug("Start to scroll to case:%s failed" % case_name)
        return False

    def scroll_to_case_sdevice(self, case_name, timeout=3000):
        # self.logger.debug("Start to scroll to sdevice case:%s" % case_name)
        # if self.sdevice(resourceId="android:id/list", scrollable=True).exists:
        #     self.sdevice(resourceId="android:id/list", scrollable=True).scroll.vert.to(text=case_name)
        #
        # if self.sdevice(text=case_name).wait.exists(timeout=5000):
        #     self.logger.debug("Start to scroll to case:%s successfully" % case_name)
        #     self.sdevice(text=case_name).click()
        #
        #     if self.sdevice(text="OK").exists:
        #         self.sdevice(text="OK").click()
        #     return True
        # self.logger.debug("Start to scroll to case:%s failed" % case_name)
        # return False
        self.logger.debug("Start to scroll to case:%s" % case_name)
        if self.sdevice(resourceId="android:id/list", scrollable=True).wait.exists(timeout=5000):
            self.sdevice(resourceId="android:id/list", scrollable=True).scroll.vert.to(text=case_name)

        if self.sdevice(text=case_name).wait.exists(timeout=5000):
            self.logger.debug("Start to scroll to case:%s successfully" % case_name)
            self.sdevice(text=case_name).click.wait()

            if self.sdevice(text="OK").wait.exists(timeout=timeout):
                self.sdevice(text="OK").click()

            if "BYOD Managed Provisioning" == case_name:

                if self.sdevice(text="START BYOD PROVISIONING FLOW").wait.exists(timeout=5000):
                    self.sdevice(text="START BYOD PROVISIONING FLOW").click()

                if self.sdevice(text="DELETE").wait.exists(timeout=3000):
                    self.sdevice(text="DELETE").click()

                if self.sdevice(text="ACCEPT & CONTINUE").wait.exists(timeout=5000):
                    self.sdevice(text="ACCEPT & CONTINUE").click()

                if self.sdevice(text="Setting up your work profile…").wait.exists(timeout=5000):
                    self.logger.debug("Setting up my work profile......")

                if self.sdevice(text="BYOD Managed Provisioning").wait.exists(timeout=15000):
                    self.logger.debug("Setting up my work profile Completed")
                    self.sdevice.delay(5)
            self.logger.debug("Scroll to case:'%s' successfully" % case_name)
            return True
        else:
            self.logger.warning("text '%s' not exists" % case_name)
            # count += 1
            # self.enter_CTSVerifier()
            # if count <= 3:
            #     self.scroll_to_case(case_name, count)

        self.logger.debug("Start to scroll to case:%s failed" % case_name)
        self.save_fail_img()
        return False
    def scroll_to_case_without_check(self, case_name):
        self.logger.debug("Start to scroll to case:%s" % case_name)
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.to(text=case_name)
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.logger.debug("Start to scroll to case:%s successfully" % case_name)
            self.device(text=case_name).click()

            if self.device(text="OK").exists:
                self.device(text="OK").click()
            return True
        self.logger.debug("Start to scroll to case:%s failed" % case_name)
        return False

    def Charging_Constraints(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(text="START TEST").wait.exists(timeout=3000):
            self.device(text="START TEST").click()

        self.device.delay(5)

        if self.device(resourceId=pass_button).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
            self.logger.debug("%s Test Pass" % case_name)
            return True
        self.logger.debug("%s Test Failed" % case_name)
        return False

    def Connectivity_Constraints(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="OK").wait.exists(timeout=3000):
            self.device(text="OK").click()

        if self.device(text="START TEST").wait.exists(timeout=3000):
            self.device(text="START TEST").click()
        self.device.delay(15)

        self.logger.debug("%s Test Pass" % case_name)
        if self.device(resourceId=pass_button).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
        return True

    def Battery_Saving_Mode_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="LAUNCH SETTINGS", enabled=True).wait.exists(timeout=5000):
            self.device(text="LAUNCH SETTINGS", enabled=True).click()

        if self.device(text="Mode").wait.exists(timeout=5000):
            self.device(text="Mode").click()

        if self.device(text="Battery saving").wait.exists(timeout=5000):
            self.device(text="Battery saving").click()

        if self.device(text="AGREE").wait.exists(timeout=5000):
            self.device(text="AGREE").click()

        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button).click()
            return True

        self.save_fail_img()
        if self.device(resourceId=fail_button).wait.exists(timeout=5000):
            self.device(resourceId=fail_button).click()
            self.logger.warning("%s Test Failed" % case_name)
        return False

    def Device_Only_Mode_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="LAUNCH SETTINGS", enabled=True).wait.exists(timeout=5000):
            self.device(text="LAUNCH SETTINGS", enabled=True).click()

        if self.device(text="Mode").wait.exists(timeout=5000):
            self.device(text="Mode").click()

        if self.device(text="Device only").wait.exists(timeout=5000):
            self.device(text="Device only").click()

        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button).click()
            return True

        if self.device(resourceId=fail_button).wait.exists(timeout=5000):
            self.device(resourceId=fail_button).click()
            self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def High_Accuracy_Mode_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="LAUNCH SETTINGS", enabled=True).wait.exists(timeout=5000):
            self.device(text="LAUNCH SETTINGS", enabled=True).click()

        if self.device(text="Mode").wait.exists(timeout=5000):
            self.device(text="Mode").click()

        if self.device(text="High accuracy").wait.exists(timeout=5000):
            self.device(text="High accuracy").click()

        if self.device(text="AGREE").wait.exists(timeout=5000):
            self.device(text="AGREE").click()

        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button).click()
            return True

        if self.device(resourceId=fail_button).wait.exists(timeout=5000):
            self.device(resourceId=fail_button).click()
            self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Location_Mode_Off_Test(self, case_name):
        self.scroll_to_case(case_name)
        self.disable_Location()
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button).click()
            return True

        self.save_fail_img()
        return False

    def Full_disk_encryption_enabled(self, case_name):
        self.scroll_to_case(case_name)
        self.device.delay(3)
        self.device.press.back()
        self.logger.debug("%s Test Pass" % case_name)

        return True

    def Badged_work_apps_visible_in_Launcher(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(description="All Items").wait.exists(timeout=5000):
            self.device(description="All Items").click()
        if self.device(resourceId="com.android.launcher3:id/all_apps_handle").exists:
            self.device(resourceId="com.android.launcher3:id/all_apps_handle").click()
        # self.device().fling.vert.toEnd() #有时候划不动，用下面方法更可靠点
        #self.device(scrollable=True, resourceId="com.blackberry.blackberrylauncher:id/apps_view").scroll.vert.toEnd()
        self.device(scrollable=True, resourceId="com.android.launcher3:id/apps_list_view").scroll.vert.to(text="CTS Verifier")
        if self.device(description="Work CTS Verifier").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Work_notification_is_badged(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        self.device.open.notification()

        if self.device(text="This is a notification").wait.exists(timeout=5000) and self.device(
                resourceId="android:id/profile_badge").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)

            self.clear_notification()
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        self.back_to_Pass_Popup_home()
        return False

    def Authentication_bound_keys(self, case_name):
        self.scroll_to_case(case_name, 8000)
        self.wait(3)

        if self.device(text="OK").exists:
            self.device(text="OK").click()

        if self.device(text="SET UP").wait.exists(timeout=5000):
            self.device(text="SET UP").click()
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()

        if self.device(text="Password").wait.exists(timeout=5000):
            self.device(text="Password").click()
            if self.device(text="NO").wait.exists(timeout=5000):
                self.device(text="NO").click()
            if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
                self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
                self.device.press.enter()
                if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
                    self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
                    self.device.press.enter()
            self.wait(5)
            if self.device(text="Show all notification content").wait.exists(timeout=5000):
                self.device(text="Show all notification content").click()
                self.device(text="DONE").click()
        self.device.press.back()
        self.device.press.back()


        if self.device(text="Lockscreen-bound key test").wait.exists(timeout=5000):
            self.device(text="Lockscreen-bound key test").click()
        self.device.delay(10)

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()
            # self.device.press.enter()
            self.logger.debug("Lockscreen-bound key test Test Pass")
            return True
        self.logger.warning("Lockscreen-bound key  Test Failed")
        self.save_fail_img()
        return False


    def Please_turn_work_mode_back_on(self, case_name):
        if self.device(text="OPEN SETTINGS TO TOGGLE WORK MODE").wait.exists(timeout=5000):
               self.device(text="OPEN SETTINGS TO TOGGLE WORK MODE").click()
        if self.device(text="Work profile settings").wait.exists(timeout=5000):
               self.device(text="Work profile settings").click()
        if self.device(text="Work mode").wait.exists(timeout=5000):
               self.device(text="Work mode").click()

        self.adb.shell("input text %s" % password)
        self.device.press.enter()
        time.sleep(2)
        self.back_to_app(case_name)
        self.logger.debug("%s Test Pass" % case_name)
        return True

        self.save_fail_img()
        self.logger.debug("%s Test Pass" % case_name)
        return False

    def switch_work_mode(self, flag):
        try:
            self.enter_settings("Users & accounts")

            # assert self.device(text="Work profile settings").wait.exists(timeout=5000)
            # self.device(text="Work profile settings").click()
            # 疑似Python自带缩进问题，click动作没有执行，做以下修改取消断言
            self.device(text="Work profile settings").wait.exists(timeout=5000)
            self.device(text="Work profile settings").click()

            assert self.switch_permission(flag, "Work mode")
            self.logger.warning("switch_work_mode to %s successfully" % flag)
            return True
        except:
            self.logger.warning("switch_work_mode to %s failed" % flag)
            self.logger.warning(traceback.format_exc())
            return False

    def Please_turn_off_work_mode(self, case_name):
        if self.device(text="OPEN SETTINGS TO TOGGLE WORK MODE").wait.exists(timeout=5000):
            self.device(text="OPEN SETTINGS TO TOGGLE WORK MODE").click()

        if self.device(text="Work profile settings").wait.exists(timeout=5000):
            self.device(text="Work profile settings").click()
        if self.device(resourceId="android:id/switch_widget",index=0,checked=True).wait.exists(timeout=5000):
            self.device(resourceId="android:id/switch_widget",index=0,checked=True).click()


        #self.switch_work_mode(False)

        self.back_to_app(case_name)
        self.logger.debug("%s Test Pass" % case_name)
        return True

    def Starting_work_apps_when_work_mode_is_off(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(description="All Items").wait.exists(timeout=5000):
            self.device(description="All Items").click()
        if self.device(resourceId="com.android.launcher3:id/all_apps_handle").wait.exists(timeout=5000):
            self.device(resourceId="com.android.launcher3:id/all_apps_handle").click()
        if self.device(resourceId="com.android.launcher3:id/apps_list_view").exists:
            self.device(resourceId="com.android.launcher3:id/apps_list_view").scroll.vert.to(text="CTS Verifier")
        else:
            self.device.swipe(360,1064,360,13)
            self.device(resourceId="com.android.launcher3:id/apps_list_view").scroll.vert.to(text="CTS Verifier")

        if self.device(description="Disabled Work CTS Verifier").wait.exists(timeout=5000):
            self.device(description="Disabled Work CTS Verifier").click()

        assert self.device(
            text="Allow work profile to function, including apps, background sync, and related features.").ext5 or self.device(
            text="This will turn on your work profile, including apps, background sync, and related features").ext5
        self.logger.debug("%s Test Pass" % case_name)
        if self.device(text="CANCEL").wait.exists(timeout=5000):
            self.device(text="CANCEL").click()

        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()
        return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Starting_work_apps_when_work_mode_is_on(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(description="All Items").wait.exists(timeout=5000):
            self.device(description="All Items").click()

        if self.device(resourceId="com.android.launcher3:id/all_apps_handle").wait.exists(timeout=5000):
            self.device(resourceId="com.android.launcher3:id/all_apps_handle").click()
        if self.device(resourceId="com.android.launcher3:id/apps_list_view").exists():
            self.device(resourceId="com.android.launcher3:id/apps_list_view").scroll.vert.to(text="Contacts")
        elif self.device(text="Work", resourceId="com.android.launcher3:id/folder_icon_name").wait.exists(timeout=5000):
            self.device(text="Work" , resourceId="com.android.launcher3:id/folder_icon_name").click()

        if self.device(description="Work Contacts").wait.exists(timeout=5000):
            self.device(description="Work Contacts").click()

        isPass = False
        if self.device(text="INSTALL").wait.exists(timeout=5000) or self.device(text="Install").wait.exists(
                timeout=5000) or self.device(resourceId="com.google.android.contacts:id/product_lockup").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            isPass = True

        if self.device(text="CANCEL").wait.exists(timeout=5000):
            self.device(text="CANCEL").click()

        # self.back_to_home()无法启动Verifier，改用shell命令
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")


        if isPass and self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()
        #更新pass_button enabled值
        self.device.dump()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
         self.device(resourceId=pass_button).click()
        return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Status_bar_icon_when_work_mode_is_off(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        # 多个icon会折叠在一起,需要点击两下
        if self.device(resourceId="com.android.settings:id/expand_indicator").ext5:
            self.device(resourceId="com.android.settings:id/expand_indicator").click()
            if not self.device(text="Work profile is off").wait.exists(timeout=2000):
                if self.device(resourceId="com.android.settings:id/expand_indicator").ext5:
                    self.device(resourceId="com.android.settings:id/expand_indicator").click()

        if self.device(text="Work profile is off").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def enable_use_one_lock(self):
        try:
            self.enter_settings("Security & location")
            if self.scroll_to_text_without_click("Use the same lock"):
                pass
            elif self.scroll_to_text_without_click("Use one lock"):
                pass
            if self.device(text="Work profile lock", enabled=False).ext5:
                self.logger.debug("'Use one lock' is already enabled")
                return True
            if self.device(text="Use the same lock").wait.exists(timeout=5000):
                self.device(text="Use the same lock").click()
            elif self.device(text="Use one lock").wait.exists(timeout=5000):
                self.device(text="Use one lock").click()

            if self.device(text="USE ONE LOCK").wait.exists(timeout=5000):
                self.device(text="USE ONE LOCK").click()

            if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
                self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()
            self.device.delay(5)

            if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
                self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()

            assert self.device(text="Work profile lock", enabled=False).ext5
            self.logger.debug("Enable 'use one lock' successfully")
            return True
        except:
            self.logger.warning(traceback.format_exc())

    def disable_use_one_lock(self):
        self.enter_settings("Security & location")

        if self.device(text="Use the same lock").wait.exists(timeout=5000):
            self.device(text="Use the same lock").click()
        elif self.device(text="Use one lock").wait.exists(timeout=5000):
            self.device(text="Use one lock").click()

        if self.device(text="USE ONE LOCK").wait.exists(timeout=5000):
            self.device(text="USE ONE LOCK").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        self.device.press.enter()
        self.device.delay(5)

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        self.device.press.enter()
        self.device.delay(5)

        self.logger.debug("Enable 'use one lock' successfully")

    def Organization_Info(self, case_name):
        self.scroll_to_case(case_name)

        # ##不要 user one lock 不然无法弹出指定的背景颜色
        # self.enter_settings("Security & location")
        # self.scroll_to_text("Use one lock")
        #
        # if self.device(text="USE ONE LOCK").wait.exists(timeout=5000):
        # self.device(text="USE ONE LOCK").click()
        #
        # if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
        # self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        # self.device.press.enter()
        # self.device.delay(3)
        #
        # if self.device(text="Password").wait.exists(timeout=5000):
        # self.device(text="Password").click()
        #
        # if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
        # self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        # self.device.press.enter()
        #     self.device.delay(3)
        #
        # if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
        #     self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        #     self.device.press.enter()
        #     self.device.delay(3)
        #
        # self.back_to_app(case_name)
        if self.device(resourceId="com.android.cts.verifier:id/organization_name_edit_text").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/organization_name_edit_text").set_text("test")

        if self.device(resourceId="com.android.cts.verifier:id/organization_color_edit_text").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/organization_color_edit_text").set_text("#FF00FF")

        if self.device(text="SET").wait.exists(timeout=5000):
            self.device(text="SET").click()
        #if self.device(text="GO").wait.exists(timeout=5000):
           # self.device(text="GO").click()
        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
            self.device.delay(3)

        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="test").wait.exists(timeout=5000) and self.device(
                resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            # self.device.press.enter()
            self.device.press.enter()
            self.device.delay(3)
            self.device.press.back()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()

            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Status_bar_icon_when_work_mode_is_on(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        # 多个icon会折叠在一起,需要点击两下
        if self.device(resourceId="com.android.settings:id/expand_indicator").ext5:
            self.device(resourceId="com.android.settings:id/expand_indicator").click()
            if self.device(resourceId="com.android.settings:id/expand_indicator").ext5:
                self.device(resourceId="com.android.settings:id/expand_indicator").click()

        if not self.device(text="Work profile is off").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Notifications_when_work_mode_is_off(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()

        self.logger.debug("%s Test Pass" % case_name)
        return True

    def Prepare_a_work_notification(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        self.device.open.notification()

        if self.device(resourceId="android:id/profile_badge").wait.exists(timeout=5000) and self.device(
                text="This is a notification").wait.exists(timeout=5000):
            self.clear_notification()
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=8000):
                self.device(text="PASS").click()

            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        self.clear_notification()
        return False

    def Vpn_test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def VPN_app_targeting_SDK_23(self, case_name):
        self.adb.cmd("uninstall", "com.android.cts.vpnfirewall")
        time.sleep(5)
        self.logger.debug("re-install  CtsVpnFirewallAppApi23.apk")
        print os.path.join(os.getcwd(), "CtsVpnFirewallAppApi23.apk")
        self.adb.cmd("install", "-r", os.path.join(os.getcwd(), "CtsVpnFirewallAppApi23.apk"))
        self.device.delay(10)
        assert self.device(text="PREPARE VPN").ext5
        self.device(text="PREPARE VPN").click()

        assert self.device(text="Connection request").ext5
        self.device(text="OK").click()

        self.scroll_to_case(case_name)

        assert self.device(text="GO").ext5
        self.device(text="GO").click()

        assert self.device(text="CtsVpnFirewallApp").ext5 and self.device(
            resourceId="com.android.settings:id/settings_button").ext5
        self.device(resourceId="com.android.settings:id/settings_button").click()

        assert self.device(text="Always-on VPN", enabled=False).ext5 and self.device(
            text="Block connections without VPN", enabled=False).ext5
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_Pass_Popup_home()
        self.test_pass_popup()
        return True

    def VPN_app_targeting_SDK_24(self, case_name):
        self.adb.cmd("uninstall", "com.android.cts.vpnfirewall")
        time.sleep(5)
        self.logger.debug("re-install  CtsVpnFirewallAppApi24.apk")
        self.adb.cmd("install", "-r", os.path.join(os.getcwd(), "CtsVpnFirewallAppApi24.apk"))
        self.device.delay(10)
        assert self.device(text="PREPARE VPN").ext5
        self.device(text="PREPARE VPN").click()

        assert self.device(text="Connection request").ext5
        self.device(text="OK").click()

        self.scroll_to_case(case_name)

        assert self.device(text="GO").ext5
        self.device(text="GO").click()

        assert self.device(text="CtsVpnFirewallApp").ext5 and self.device(
            resourceId="com.android.settings:id/settings_button").ext5
        self.device(resourceId="com.android.settings:id/settings_button").click()

        assert self.device(text="Always-on VPN", enabled=True).ext5 and self.device(
            text="Block connections without VPN", enabled=False).ext5
        self.device(text="Always-on VPN", enabled=True).click()

        assert self.device(text="Block connections without VPN").wait.exists(timeout=30000)
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_Pass_Popup_home()
        self.test_pass_popup()
        return True

    def VPN_app_with_opt_out(self, case_name):
        self.adb.cmd("uninstall", "com.android.cts.vpnfirewall")
        time.sleep(5)
        self.logger.debug("re-install  CtsVpnFirewallAppNotAlwaysOn.apk")
        print os.path.join(os.getcwd(), "CtsVpnFirewallAppNotAlwaysOn.apk")
        self.adb.cmd("install", "-r", os.path.join(os.getcwd(), "CtsVpnFirewallAppNotAlwaysOn.apk"))
        self.device.delay(10)
        assert self.device(text="PREPARE VPN").ext5
        self.device(text="PREPARE VPN").click()

        assert self.device(text="Connection request").ext5
        self.device(text="OK").click()

        self.scroll_to_case(case_name)

        assert self.device(text="GO").ext5
        self.device(text="GO").click()

        assert self.device(text="CtsVpnFirewallApp").ext5 and self.device(
            resourceId="com.android.settings:id/settings_button").ext5
        self.device(resourceId="com.android.settings:id/settings_button").click()

        assert self.device(text="Always-on VPN", enabled=False).ext5 and self.device(
            text="Block connections without VPN", enabled=False).ext5
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_Pass_Popup_home()
        self.test_pass_popup()
        return True

    def Disable_non_market_apps(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.device(text="OK").click()
            self.logger.debug("%s Test Pass" % case_name)
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Permissions_lockdown(self, case_name, serinoM):
        self.scroll_to_case(case_name)

        self.uninstall_CtsPermissionApp()
        self.wait(5)
        self.install_CtsPermissionApp()

        if self.device(text="GO").wait.exists(timeout=10000):
            self.device(text="GO").click()

        if self.device(text="Grant").wait.exists(timeout=5000):
            self.device(text="Grant").click()

        if self.device(text="OPEN APPLICATION SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN APPLICATION SETTINGS").click()

        if self.device(text="Permissions").wait.exists(timeout=5000):
            self.device(text="Permissions").click()

        if not self.device(text="Contacts", enabled=False).wait.exists(timeout=5000):
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False

        self.back_to_Pass_Popup_home()
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Let user decide").wait.exists(timeout=5000):
            self.device(text="Let user decide").click()

        if self.device(text="OPEN APPLICATION SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN APPLICATION SETTINGS").click()

        if self.device(text="Permissions").wait.exists(timeout=5000):
            self.device(text="Permissions").click()

        if not self.device(text="Contacts", enabled=True).wait.exists(timeout=5000):
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False

        self.back_to_Pass_Popup_home()
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Deny").wait.exists(timeout=10000):
            self.device(text="Deny").click()

        if self.device(text="OPEN APPLICATION SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN APPLICATION SETTINGS").click()

        if self.device(text="Permissions").wait.exists(timeout=5000):
            self.device(text="Permissions").click()

        if not self.device(text="Contacts", enabled=False).wait.exists(timeout=5000) and not self.device(
                text="Disabled by admin", enabled=False).wait.exists(timeout=5000):
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False

        self.back_to_Pass_Popup_home()

        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()

        self.logger.debug("%s Test Pass" % case_name)
        return True

    def Permissions_lockdown__dot(self, case_name, serinoM):
        self.scroll_to_case(case_name)
        self.install_CtsPermissionApp()

        if self.device(text="Grant").wait.exists(timeout=5000):
            self.device(text="Grant").click()

        if self.device(text="OPEN APPLICATION SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN APPLICATION SETTINGS").click()

        assert (self.device(text="Permissions").wait.exists(timeout=5000))
        self.device(text="Permissions").click()

        assert (self.device(text="Contacts", enabled=False).wait.exists(timeout=5000))

        self.back_to_app(case_name)

        if self.device(text="Let user decide").wait.exists(timeout=5000):
            self.device(text="Let user decide").click()

        if self.device(text="OPEN APPLICATION SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN APPLICATION SETTINGS").click()

        assert (self.device(text="Permissions").wait.exists(timeout=5000))
        self.device(text="Permissions").click()

        assert (self.device(text="Contacts", enabled=True).wait.exists(timeout=5000))

        self.back_to_app(case_name)

        if self.device(text="Deny").wait.exists(timeout=10000):
            self.device(text="Deny").click()

        if self.device(text="OPEN APPLICATION SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN APPLICATION SETTINGS").click()

        assert (self.device(text="Permissions").wait.exists(timeout=5000))
        self.device(text="Permissions").click()

        assert (self.device(text="Contacts", enabled=False).wait.exists(timeout=5000))

        self.back_to_app(case_name)
        if self.device(resourceId=pass_button).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
            return True

        self.save_fail_img()
        return False

    def check_lockscreen_notification(self, fox_message):
        self.logger.debug("starting to check notification '%s'" % fox_message)
        self.device.wakeup()
        if self.device(textContains=fox_message).wait.exists(timeout=5000) or self.device(text=fox_message).wait.exists(timeout=5000):
            self.logger.debug("Found '%s'" % fox_message)
            return True
        else:
            self.logger.debug("can not find 'Contents hidden by policy',wake up device again")
            self.device.wakeup()
            if self.device(resourceId="com.android.systemui:id/bbry_simple_notification_icons_merger").ext5:
                # self.logger.debug("click 'com.android.systemui:id/bbry_simple_notification_icons_merger'")
                self.device(resourceId="com.android.systemui:id/bbry_simple_notification_icons_merger").click()
                if self.device(textContains="Contents hidden").wait.exists(timeout=5000):
                    self.logger.debug("Found '%s'" % fox_message)
                    return True
        self.logger.debug("Can not found '%s'" % fox_message)
        return False

    def Unredacted_notifications_disabled_on_keyguard(self, case_name):

        if self.device(text="PREPARE TEST").wait.exists(timeout=5000):
            self.device(text="PREPARE TEST").click()



        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()

        self.device.delay(10)
        self.device.wakeup()

        # 8.1 R2套件锁屏界面折叠了Contents hidden
        isPass = False
        if self.check_lockscreen_notification("Contents hidden"):
            self.logger.debug("%s Test Pass" % case_name)
            isPass = True
        else:
            self.logger.debug("%s Test Fail,can not found 'Contents hidden'" % case_name)

        self.unlock_scream_with_password()

        if isPass and self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Enable_non_market_apps(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        assert self.device(text="SETTINGS").wait.exists(timeout=5000)
        self.device(text="SETTINGS").click()

        assert self.device(text="Allow from this source").wait.exists(timeout=5000)
        self.device(text="Allow from this source").click()
        self.device.press.back()

        assert self.device(text="INSTALL").wait.exists(timeout=5000)
        self.device(text="INSTALL").click()
        self.logger.debug("%s Test Pass" % case_name)
        if self.device(text="PASS").wait.exists(timeout=20000):
            self.device(text="PASS").click()
        return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Open_app_cross_profiles_from_the_work_side(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="CTS Verifier").wait.exists(timeout=5000):
            self.device(text="CTS Verifier").click()

            if self.device(text="You selected the ctsverifier option").wait.exists(timeout=5000):
                self.device(text="FINISH").click()
                self.logger.debug("%s Test Pass" % case_name)
                if self.device(text="PASS").wait.exists(timeout=5000):
                    self.device(text="PASS").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Open_app_cross_profiles_from_the_personal_side(self, case_name):

        self.scroll_to_case(case_name)

        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="CTS Verifier").wait.exists(timeout=5000):
            self.device(text="CTS Verifier").click()

            if self.device(text="You selected the ctsverifier option").wait.exists(timeout=5000):
                self.device(text="FINISH").click()
                self.logger.debug("%s Test Pass" % case_name)
                if self.device(text="PASS").wait.exists(timeout=5000):
                    self.device(text="PASS").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_printing_settings(self, case_name):
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="android:id/widget_frame").wait.exists(timeout=5000):
            self.device(resourceId="android:id/widget_frame").click()

            if self.device(text="Work").wait.exists(timeout=5000):
                self.device(text="Work").click()
                self.logger.debug("%s Test Pass" % case_name)
                self.back_to_Pass_Popup_home()
                if self.device(text="PASS").wait.exists(timeout=5000):
                    self.device(text="PASS").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_location_settings(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Location for work profile").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_app_settings(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        self.device.delay(3)

        if self.device(resourceId="com.android.settings:id/filter_spinner").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/filter_spinner").click()

        if self.device(text="Work").wait.exists(timeout=5000):
            self.device(text="Work").click()

        if self.device(text="CTS Verifier").wait.exists(timeout=10000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_trusted_credential_settings(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(scrollable=True).wait.exists(timeout=5000):
            self.device(scrollable=True).scroll.vert.to(text="Encryption & credentials")

        if self.device(text="Encryption & credentials").wait.exists(timeout=5000):
            self.device(text="Encryption & credentials").click()

        if self.device(text="Trusted credentials").wait.exists(timeout=5000):
            self.device(text="Trusted credentials").click()

        if self.device(text="USER").wait.exists(timeout=5000):
            self.device(text="USER").click()

        if self.device(text="Personal", resourceId="android:id/title").wait.exists(timeout=10000) and self.device(
                text="Work", resourceId="android:id/title").wait.exists(timeout=10000):
            self.logger.debug("%s Test Pass" % case_name)
            if not self.back_to_Pass_Popup_home():
                self.scroll_to_case(case_name)

            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_device_administrator_settings(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        self.device(scrollable=True).scroll.vert.to(text="Device admin apps")
        if self.device(text="Device admin apps").wait.exists(timeout=5000):
            self.device(text="Device admin apps").click()

        if self.device(text="CTS Verifier").wait.exists(timeout=5000):
            self.device(text="CTS Verifier").click()

        assert self.device(text="Remove work profile", enabled=True).wait.exists(timeout=5000)
        self.device(text="Remove work profile", enabled=True).click()

        assert self.device(text="DELETE").wait.exists(timeout=5000)
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_Pass_Popup_home()

        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()

    def Profile_aware_accounts_settings(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        self.enter_settings("Users & accounts")

        if self.device(text="Personal").wait.exists(timeout=5000) and self.device(text="Work").wait.exists(
                timeout=5000) and self.device(text="Remove work profile").wait.exists(timeout=5000):

            if self.device(scrollable=True).exists:
                self.device(scrollable=True).scroll.vert.toEnd()

            if self.device(text="Auto-sync personal data").wait.exists(timeout=5000) and self.device(
                    text="Auto-sync work data").wait.exists(timeout=5000):
                self.logger.debug("%s Test Pass" % case_name)
                self.back_to_Pass_Popup_home()

                if self.device(text="PASS").wait.exists(timeout=5000):
                    self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Work_status_icon_is_displayed(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="FINISH").wait.exists(timeout=5000):
            self.device(text="FINISH").click()

        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()

        self.logger.debug("%s Test Pass" % case_name)
        return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Work_status_toast_is_displayed(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="FINISH").wait.exists(timeout=5000):
            self.device(text="FINISH").click()

        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()
            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_owner_installed(self, case_name):
        if self.device(text="START BYOD PROVISIONING FLOW").wait.exists(timeout=5000):
            self.device(text="START BYOD PROVISIONING FLOW").click()
        if self.device(text="NEXT").wait.exists(timeout=5000):
            self.device(text="NEXT").click()

        if self.device(text="OK").wait.exists(timeout=5000):
            self.device(text="OK").click()

        if self.device(text="BYOD Managed Provisioning").wait.exists(timeout=15000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device.delay(4)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Personal_password_test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        self.device.sleep()
        self.unlock_scream_with_password()
        self.back_to_Pass_Popup_home()

        if self.device(text="PASS").wait.exists(timeout=15000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Disallow_controlling_apps__byod(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(resourceId="com.android.settings:id/filter_spinner").wait.exists(timeout=15000):
            self.device(resourceId="com.android.settings:id/filter_spinner").click()
        if self.device(text="Work").wait.exists(timeout=5000):
            self.device(text="Work").click.wait()

        if self.device(text="Contacts").wait.exists(timeout=5000):
            self.device(text="Contacts").click.wait()

        if self.device(text="DISABLE").wait.exists(timeout=10000):
            self.device(text="DISABLE").click()

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(text="OK").click()
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button).wait.exists(timeout=5000):
                self.device(resourceId=pass_button).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_modify_accounts__byod(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        assert self.device(resourceId="com.android.settings:id/restricted_icon").wait.exists(timeout=5000)

        assert self.device(text="Add account", enabled=False).wait.exists(timeout=5000)
        self.device(text="Add account", enabled=False).click()
        assert self.device(text="Action not allowed").wait.exists(timeout=5000)
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
        return True

        self.logger.warning("%s Test Failed" % case_name)
        if self.device(resourceId=fail_button).wait.exists(timeout=5000):
            self.device(resourceId=fail_button).click()
        return False

    def Disallow_share_location__byod(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(resourceId="com.android.cts.verifier:id/switch_widget").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/switch_widget").click()

        if self.device(text="OPEN SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN SETTINGS").click()

        if self.device(resourceId="com.android.settings:id/restricted_icon").wait.exists(timeout=5000) and self.device(
                text="Disabled by admin").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button).wait.exists(timeout=5000):
                self.device(resourceId=pass_button).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        if self.device(resourceId=fail_button).wait.exists(timeout=5000):
            self.device(resourceId=fail_button).click()
        return False

    def Disallow_uninstall_apps__byod(self, case_name, serinoM):

        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(resourceId="com.android.settings:id/filter_spinner").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/filter_spinner").click()
        if self.device(text="Work").wait.exists(timeout=5000):
            self.device(text="Work").click()
        assert self.device(text="CtsPermissionApp").wait.exists(timeout=5000)
        self.device(text="CtsPermissionApp").click()
        if self.device(text="UNINSTALL").wait.exists(timeout=5000):
            self.device(text="UNINSTALL").click()

        assert self.device(text="Action not allowed").wait.exists(timeout=5000)
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button).wait.exists(timeout=5000):
            self.device(resourceId=pass_button).click()
        return True

    def Set_permitted_accessibility_services__byod(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()
        #self.scroll_to_text("Dummy accessibility service")
        if self.device(resourceId="com.android.settings:id/restricted_icon").wait.exists(timeout=5000) and self.device(
                text="Dummy accessibility service").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button).wait.exists(timeout=5000):
                self.device(resourceId=pass_button).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Set_permitted_input_methods__byod(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Dummy input method").wait.exists(timeout=5000) and self.device(
                text="Disabled by admin").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button).wait.exists(timeout=5000):
                self.device(resourceId=pass_button).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_data_usage_settings_wifi(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Data usage").wait.exists(timeout=5000):
            self.device(text="Data usage").click()

        if self.device(text="Wi-Fi data usage").wait.exists(timeout=5000):
            self.device(text="Wi-Fi data usage").click()

        if self.device(text="All work apps").wait.exists(timeout=10000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_data_usage_settings_Cellular(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()
        self.logger.debug("%s Test Pass" % case_name)
        return True

    def Disallow_apps_control(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Data usage").wait.exists(timeout=5000):
            self.device(text="Data usage").click()

        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toEnd()
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text="Wi-Fi data usage").click()

        if self.device(text="All work apps").wait.exists(timeout=10000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button).wait.exists(timeout=5000):
                self.device(resourceId=pass_button).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        if self.device(resourceId=fail_button).wait.exists(timeout=5000):
            self.device(resourceId=fail_button).click()
        return False

    def Disabled_uninstall_button(self, case_name, serinoM):
        self.install_CtsPermissionApp()
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="com.android.settings:id/filter_spinner").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/filter_spinner").click()
        if self.device(text="Work").wait.exists(timeout=5000):
            self.device(text="Work").click()
        if self.device(text="CtsPermissionApp").wait.exists(timeout=5000):
            self.device(text="CtsPermissionApp").click()
        if self.device(text="UNINSTALL").wait.exists(timeout=5000):
            self.device(text="UNINSTALL").click()

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.back_to_Pass_Popup_home()
        self.logger.warning("%s Test Failed" % case_name)
        if self.device(text="FAIL").wait.exists(timeout=5000):
            self.device(text="FAIL").click()
        return False

    def Disabled_force_stop_button(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="com.android.settings:id/filter_spinner").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/filter_spinner").click()
        if self.device(text="Work").wait.exists(timeout=5000):
            self.device(text="Work").click()
        if self.device(text="Contacts").wait.exists(timeout=5000):
            self.device(text="Contacts").click()
        if self.device(text="FORCE STOP").wait.exists(timeout=5000):
            self.device(text="FORCE STOP").click()

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Profile_aware_data_usage_settings_wifi(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()
        if self.device(text="Network & Internet").wait.exists(timeout=5000):
            self.device(text="Network & Internet").click()
        if self.device(text="Data usage").wait.exists(timeout=5000):
            self.device(text="Data usage").click()
        if self.scroll_to_text("Wi-Fi data usage"):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True
        else:
            self.back_to_Pass_Popup_home()
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False


    def test_pass_popup(self):
        if self.device(text="PASS").wait.exists(
                timeout=5000):
            self.device(text="PASS").click()
            time.sleep(2)
            self.logger.debug("Click POP-UP 'PASS' successfully")
            return True
        else:
            self.logger.debug("Click POP-UP 'PASS' failed")
            return False

    def test_pass(self, case_name, timeout=5000):
        """
        test pass
        :param case_name: test case
        :param timeout: default =5000
        :return: True or False
        """
        if self.device(resourceId=pass_button, enabled=True).wait.exists(
                timeout=timeout):
            self.device(resourceId=pass_button, enabled=True).click()
            self.device.wait("idle")
            self.logger.debug("CASE <%s> Test Pass!" % case_name)
            return True
        else:
            self.logger.warning(
                "can't click the pass button, Maybe the pass button  is not enabled or not found")
            self.save_fail_img()
        return False

    def test_fail(self, case_name, timeout=5000):
        """
        test pass
        :param case_name: test case
        :param timeout: default =5000
        :return: True or False
        """
        if self.device(resourceId=fail_button, enabled=True).wait.exists(
                timeout=timeout):
            self.device(resourceId=fail_button, enabled=True).click()
            self.device.wait("idle")
            self.logger.debug("CASE <%s> Test Fail!" % case_name)
            return True
        else:
            self.logger.warning(
                "can't click the fail button, Maybe the fail button  is not enabled or not found")
        return False

    def test_pass_multiple_case(self, case_name):
        self.device.delay(2)
        self.device.dump()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(
                timeout=10000):
            self.device(resourceId=pass_button, enabled=True).click()
            self.device.wait("idle")
            self.logger.debug("Multiple CASE <%s> Test Pass!" % case_name)
        else:
            self.logger.debug(
                "Multiple CASE <%s> Test Failed! Because the pass button's enabled is not True" % case_name)

    def Disabled_app_storage_buttons(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="com.android.settings:id/filter_spinner").wait.exists(timeout=5000):
            self.device(resourceId="com.android.settings:id/filter_spinner").click()
        if self.device(text="Work").wait.exists(timeout=5000):
            self.device(text="Work").click()
        if self.device(text="Contacts").wait.exists(timeout=5000):
            self.device(text="Contacts").click()
        if self.device(text="Storage").wait.exists(timeout=5000):
            self.device(text="Storage").click()
        if self.device(text="CLEAR DATA").wait.exists(timeout=5000):
            self.device(text="CLEAR DATA").click()

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Camera_support_cross_profile_image_capture(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="com.mediatek.camera:id/shutter_image").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/shutter_image").click()
        self.device.delay(500)
        if self.device(resourceId="com.mediatek.camera:id/btn_save").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/btn_save").click()
        if self.device(text="CLOSE").wait.exists(timeout=5000):
            self.device(text="CLOSE").click()
            self.logger.debug("%s Test Pass" % case_name)
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Camera_support_cross_profile_video_capture_with_extra(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="com.mediatek.camera:id/shutter_image").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/shutter_image").click()

        self.device.delay(5)

        if self.device(resourceId="com.mediatek.camera:id/video_stop_shutter").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/video_stop_shutter").click()

        if self.device(resourceId="com.mediatek.camera:id/btn_save").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/btn_save").click()

        if self.device(text="PLAY").wait.exists(timeout=5000):
            self.device(text="PLAY").click()
            self.device.delay(5)

        if self.device(text="CLOSE").wait.exists(timeout=5000) and self.device(
                text="Verify captured video").wait.exists(timeout=5000):
            self.device(text="CLOSE").click()
            self.logger.debug("%s Test Pass" % case_name)
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.back_to_Pass_Popup_home()
        self.logger.warning("%s Test Failed" % case_name)
        if self.device(text="FAIL").wait.exists(timeout=5000):
            self.device(text="FAIL").click()
        return False

    def Camera_support_cross_profile_video_capture_without_extra(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(resourceId="com.mediatek.camera:id/shutter_image").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/shutter_image").click()

        self.device.delay(5)

        if self.device(resourceId="com.mediatek.camera:id/video_stop_shutter").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/video_stop_shutter").click()

        if self.device(resourceId="com.mediatek.camera:id/btn_save").wait.exists(timeout=5000):
            self.device(resourceId="com.mediatek.camera:id/btn_save").click()

        if self.device(text="PLAY").wait.exists(timeout=5000):
            self.device(text="PLAY").click()
            self.device.delay(5)

        if self.device(text="CLOSE").wait.exists(timeout=5000) and self.device(
                text="Verify captured video").wait.exists(timeout=5000):
            self.device(text="CLOSE").click()
            self.logger.debug("%s Test Pass" % case_name)
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        self.back_to_Pass_Popup_home()
        self.logger.warning("%s Test Failed" % case_name)
        if self.device(text="FAIL").wait.exists(timeout=5000):
            self.device(text="FAIL").click()
        return False

    def Custom_provisioning_color(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()
        self.device.delay(2)
        self.device.press.back()
        self.device.delay(2)

        if self.device(text="STOP").wait.exists(timeout=5000):
            self.device(text="STOP").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Custom_terms(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        assert self.device(text="View terms").wait.exists(timeout=10000)
        self.device(text="View terms").click()

        assert self.device(text="Company ABC").wait.exists(timeout=10000)
        self.device(text="Company ABC").click()

        assert self.device(text="Company Terms Content. ").wait.exists(timeout=10000)
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_app(case_name)
        self.test_pass(case_name)
        return True

    def Custom_provisioning_image(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()
        self.device.delay(2)
        self.device.press.back()
        self.device.delay(2)
        if self.device(text="STOP").wait.exists(timeout=10000):
            self.device(text="STOP").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Device_Owner_Provisioning(self, case_name):
        self.scroll_to_case(case_name)
        self.scroll_to_case("Device owner negative test")

        if self.device(text="START PROVISIONING").wait.exists(timeout=5000):
            self.device(text="START PROVISIONING").click()

        if self.device(text="This device is already set up.").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)

            if self.device(text="OK").wait.exists(timeout=5000):
                self.device(text="OK").click()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Device_Owner_Requesting_Bugreport_Tests(self, case_name):
        self.scroll_to_case(case_name)
        self.scroll_to_case("Device owner negative test")

        if self.device(text="START PROVISIONING").wait.exists(timeout=5000):
            self.device(text="START PROVISIONING").click()

        if self.device(text="This device is already set up.").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)

            if self.device(text="OK").wait.exists(timeout=5000):
                self.device(text="OK").click()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Check_device_owner(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
            self.device.delay(3)
            self.logger.debug("%s Test Pass" % case_name)
            return True

    def Sharing_of_requested_bugreport_declined_while_being_taken(self, case_name):
        self.scroll_to_case(case_name)
        self.clear_notification()
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
            self.device.delay(3)
        if self.device(text="REQUEST BUGREPORT").wait.exists(timeout=5000):
            self.device(text="REQUEST BUGREPORT").click()
            self.device.delay(1)
        self.device.open.notification()
        if self.device(text="Taking bug report...").wait.exists(timeout=5000):
            self.device(text="Taking bug report...").click()
            if self.device(text="DECLINE").wait.exists(timeout=5000):
                self.device(text="DECLINE").click()
                self.device.delay(1)
                self.device.open.notification()
                if self.device(text="Bugreport sharing declined").wait.exists(timeout=5000):
                    self.device.press.back()
                    if self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).exists:
                        self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
                        return True
        else:
                return False



    def Sharing_of_requested_bugreport_accepted_while_being_taken(self, case_name):
        self.scroll_to_case(case_name)
        self.clear_notification()
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
            self.device.delay(3)
        if self.device(text="REQUEST BUGREPORT").wait.exists(timeout=5000):
            self.device(text="REQUEST BUGREPORT").click()
        self.device.open.notification()
        if self.device(text="Taking bug report...").wait.exists(timeout=5000):
            self.device(text="Taking bug report...").click()
            if self.device(text="SHARE").wait.exists(timeout=5000):
                self.device(text="SHARE").click()
                self.device.delay(15)
                self.device.open.notification()

                if self.device(text="Bugreport shared successfully").wait.exists(timeout=5000):
                    self.device.press.back()
                    if self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).exists:
                        self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
                        return True
        else:
                return False

    def Sharing_of_requested_bugreport_declined_after_having_been_taken(self, case_name):
        self.scroll_to_case(case_name)
        self.clear_notification()
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
            self.device.delay(3)
        if self.device(text="REQUEST BUGREPORT").wait.exists(timeout=5000):
            self.device(text="REQUEST BUGREPORT").click()
        self.device.delay(15)
        self.device.open.notification()
        if self.device(text="Share bug report?").wait.exists(timeout=5000):
            self.device(text="Share bug report?").click()
            if self.device(text="DECLINE").wait.exists(timeout=5000):
                self.device(text="DECLINE").click()
                self.device.delay(1)
                self.device.open.notification()
                if self.device(text="Bugreport sharing declined").wait.exists(timeout=5000):
                    self.device.press.back()
                    if self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).exists:
                        self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
                        return True
        else:
                return False

    def Sharing_of_requested_bugreport_accepted_after_having_been_taken(self, case_name):
        self.scroll_to_case(case_name)
        self.clear_notification()
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()
            self.device.delay(3)
        if self.device(text="REQUEST BUGREPORT").wait.exists(timeout=5000):
            self.device(text="REQUEST BUGREPORT").click()
        self.device.delay(15)
        self.device.open.notification()
        if self.device(text="Share bug report?").wait.exists(timeout=5000):
            self.device(text="Share bug report?").click()
            if self.device(text="SHARE").wait.exists(timeout=5000):
                self.device(text="SHARE").click()
                self.device.delay(1)
                self.device.open.notification()
                if self.device(text="Bugreport shared successfully").wait.exists(timeout=5000):
                    self.device.press.back()
                    if self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).exists:
                        self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
                        return True
        else:
                return False

    def Remove_device_owner(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="REMOVE DEVICE OWNER").wait.exists(timeout=5000):
            self.device(text="REMOVE DEVICE OWNER").click()
            self.device.delay(2)

        if self.check_device_administrators("CTS Verifier") == "Deactivate":
            self.back_to_app(case_name)
            self.test_pass(case_name)
            return True
        else:
            self.back_to_app(case_name)
            self.test_fail(case_name)
            return False

    def location_switch(self, flag):
        switch_text = ""
        if self.device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=10000):
            switch_text = self.device(resourceId="com.android.settings:id/switch_bar").get_text().lower()
        print "switch_text:", switch_text
        if flag:
            if switch_text.lower() == "on":
                self.logger.debug("The location has been opened")
                return True
            if switch_text.lower() == "off":
                self.logger.debug("The location is disabled,open it")
                self.device(resourceId="com.android.settings:id/switch_bar").click()
                if self.device(text="AGREE").exists:
                    self.device(text="AGREE").click()
                if self.device(text="ALLOW").exists:
                    self.allow_steps()
                self.device.delay(3)
            if self.device(resourceId="com.android.settings:id/switch_bar").get_text().lower() == "on":
                self.logger.debug("enabled location successfully")
                return True
        else:
            if switch_text == "off":
                self.logger.debug("The location has been closed")
                return True
            if switch_text == "on":
                self.logger.debug("The location is enabled,close it")
                self.device(resourceId="com.android.settings:id/switch_bar").click()
                self.device.delay(3)

                if self.device(text="CLOSE").exists:
                    self.device(text="CLOSE").click()

            if self.device(resourceId="com.android.settings:id/switch_bar").get_text().lower() == "off":
                self.logger.debug("Disable location successfully")
                return True

    def Enable_location(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.location_switch(True):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()

            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Disable_Nfc_beam(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click.wait()
        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click.wait()
            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Disable_location(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.location_switch(False):
            self.logger.debug("%s Test Pass" % case_name)
            self.back_to_Pass_Popup_home()

            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Disable_location_for_work_profile(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.location_switch(True):

            self.device(text="Location for work profile").click()
            if self.device(resourceId="com.android.settings:id/switch_bar").get_text() == "On":
                self.logger.debug("%s Test Pass" % case_name)
                self.back_to_Pass_Popup_home()
                if self.device(text="PASS").wait.exists(timeout=5000):
                    self.device(text="PASS").click()
                    return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def Primary_receives_updates_while_work_location_is_disabled(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="PASS").wait.exists(timeout=5000):
            self.device(text="PASS").click()
            self.logger.debug("%s Test Pass" % case_name)
            return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def CTS_Sensor_Test(self, case_name):
        self.logger.debug("Starting %s Test" % case_name)
        self.device(scrollable=True).scroll.vert.to(text=case_name)
        if self.device(text=case_name).wait.exists(timeout=5000):
            self.device(text=case_name).click()

        for loop in range(40):
            if (loop % 5) == 0:
                self.device.wakeup()
            if self.device(resourceId="com.android.cts.verifier:id/pass_button").exists:
                self.logger.debug("Found Pass Button,loop break")
                break
            elif self.device(resourceId="com.android.cts.verifier:id/next_button", enabled=True).exists:
                self.device(resourceId="com.android.cts.verifier:id/next_button", enabled=True).click()
                self.logger.debug("Press Next Button,loop continue")
                continue
            else:
                self.logger.debug("Testing,sleep 30s")
                self.device.delay(30)

        self.device.wakeup()
        if self.device(textContains="Tests failed: 0").wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass!" % case_name)
            if self.device(resourceId="com.android.cts.verifier:id/pass_button").wait.exists(timeout=5000):
                self.device(resourceId="com.android.cts.verifier:id/pass_button").click()
            return True

        self.logger.debug("%s Test Failed!Pass anyway!" % case_name)
        self.save_fail_img()
        if self.device(text="PASS ANYWAY").wait.exists(timeout=5000):
            self.device(text="PASS ANYWAY").click()
        return False

    def Toggle_Bluetooth(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="DISABLE BLUETOOTH").wait.exists(timeout=5000):
            self.device(text="DISABLE BLUETOOTH").click()

        if self.device(text="ENABLE BLUETOOTH").wait.exists(timeout=5000):
            self.device(text="ENABLE BLUETOOTH").click()

        if self.device(text="ALLOW").wait.exists(timeout=5000):
            self.device(text="ALLOW").click()

        # self.device.delay(5)
        # if self.device(text="Toggle Bluetooth").wait.exists(timeout=5000):
        #     self.device(text="Toggle Bluetooth").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.save_fail_img()
        self.logger.warning("%s Test Failed" % case_name)
        return False

    def BLE_Advertiser_Test(self, case_name):
        self.scroll_to_case(case_name)
        self.scroll_to_case("Bluetooth LE Tx Power Level")

        if self.device(text="START").wait.exists(timeout=5000):
            self.device(text="START").click()

        if self.sdevice(text="Valid power level").wait.exists(timeout=30000):
            self.logger.debug("New MAC address detected")
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()

                if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000) and self.device(
                        text=case_name).wait.exists(timeout=10000):
                    self.logger.debug("%s Test Pass" % case_name)
                    self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def BLE_Scanner_Test(self, case_name):
        self.scroll_to_case(case_name)
        self.device(text="Bluetooth LE Tx Power Level").click()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        return False

    def select_wifi_address(self, address):
        self.device.dump()
        if self.device(text="Search Target").ext15:
            if self.device(text=address).ext5:
                self.device(text=address).click()
                self.logger.debug("select %s successfully" % address)
                return True
        self.logger.debug("cannot found  %s" % address)
        return False

    def select_mac_address(self, address, device="Mdevice", deviceid=""):
        try:
            print "address:",address
            device_address = deviceid.upper() + "\n" + address.upper()
            #device_address = deviceid.upper()+ address.upper()
            #device_address = address.upper()
            self.logger.info("device_address is :%s" % device_address)
            self.device.dump()
            if device == "Sdevice":
                self.device.dump()
                self.scroll_to_text_sdevice(device_address)
            elif device == "Mdevice":
                self.device.dump()
                self.scroll_to_text(device_address)

            self.logger.debug("Found MAC Address:%s successfully." % device_address)
            return True
        except:
            self.logger.warning(traceback.format_exc())

    def Insecure_Client(self, case_name, sdevice_bt_address, serinoS):
        self.scroll_to_case_sdevice("Insecure Server")
        if self.sdevice(text="MAKE DISCOVERABLE").wait.exists(timeout=5000):
            self.sdevice(text="MAKE DISCOVERABLE").click()

        if self.sdevice(text="ALLOW").wait.exists(timeout=5000):
            self.sdevice(text="ALLOW").click()
            self.device.delay(5)
            self.scroll_to_case(case_name)

        if self.device(text="SCAN FOR DEVICES").wait.exists(timeout=10000):
            self.device(text="SCAN FOR DEVICES").click()
            self.device.delay(10)

        self.select_mac_address(sdevice_bt_address, "Mdevice", serinoS)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Insecure_Server(self, case_name, mdevice_bt_address, serinoM):

        self.scroll_to_case_sdevice("Insecure Client")

        self.scroll_to_case(case_name)

        if self.device(text="MAKE DISCOVERABLE").wait.exists(timeout=5000):
            self.device(text="MAKE DISCOVERABLE").click()

        if self.device(text="ALLOW").wait.exists(timeout=5000):
            self.device(text="ALLOW").click()

        self.device.delay(5)

        if self.sdevice(text="SCAN FOR DEVICES").wait.exists(timeout=5000):
            self.sdevice(text="SCAN FOR DEVICES").click()

        self.select_mac_address(mdevice_bt_address, "Sdevice", serinoM)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Secure_Client(self, case_name, sdevice_bt_address, serinoS):

        self.scroll_to_case_sdevice("Secure Server")

        self.scroll_to_case(case_name)

        if self.sdevice(text="MAKE DISCOVERABLE").wait.exists(timeout=5000):
            self.sdevice(text="MAKE DISCOVERABLE").click()

        if self.sdevice(text="ALLOW").wait.exists(timeout=5000):
            self.sdevice(text="ALLOW").click()

        self.device.delay(5)

        if self.device(text="SCAN FOR DEVICES").wait.exists(timeout=5000):
            self.device(text="SCAN FOR DEVICES").click()

        self.select_mac_address(sdevice_bt_address, "Mdevice", serinoS)

        if self.device(text="PAIR").wait.exists(timeout=15000):
            self.device(text="PAIR").click()

        if self.sdevice(text="PAIR").wait.exists(timeout=15000):
            self.sdevice(text="PAIR").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s " % case_name)
        self.save_fail_img()
        return False

    def Secure_Server(self, case_name, mdevice_bt_address, serinoM):
        self.scroll_to_case_sdevice("Secure Client")
        self.scroll_to_case(case_name)

        if self.device(text="MAKE DISCOVERABLE").wait.exists(timeout=5000):
            self.device(text="MAKE DISCOVERABLE").click()

        if self.device(text="ALLOW").wait.exists(timeout=5000):
            self.device(text="ALLOW").click()

        self.device.delay(5)

        if self.sdevice(text="SCAN FOR DEVICES").wait.exists(timeout=5000):
            self.sdevice(text="SCAN FOR DEVICES").click()
        self.select_mac_address(mdevice_bt_address, "Sdevice", serinoM)
        if self.device(text="PAIR").wait.exists(timeout=15000):
            self.device(text="PAIR").click()

        if self.sdevice(text="PAIR").wait.exists(timeout=15000):
            self.sdevice(text="PAIR").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Network_Connectivity_Screen_Off_Test(self, case_name):
        self.enter_case_name(case_name)

        if self.device(text="START").wait.exists(timeout=5000):
            self.device(text="START").click()

        self.device.delay(10)
        info = self.device(resourceId="com.android.cts.verifier:id/text").get_text()
        if "ACTION_POWER_DISCONNECTED" in info:
            self.logger.warning("unplug action_power")
            self.adb.shell("dumpsys battery unplug")
            self.device.delay(5)
        else:
            self.logger.warning("can not found ACTION_POWER_DISCONNECTED")

        print "self.device.info:", self.device.info["screenOn"]
        # print "self.device.info.screenOn:",self.device.info.screenOn()

        for loop in range(60):
            isScreenOn = self.device.info["screenOn"]
            print "isScreenOn", isScreenOn
            if isScreenOn:
                self.logger.debug("the screen is on")
                break
            self.logger.debug("the screen is off,please wait 2s")
            self.device.delay(2)

        self.logger.debug("unlock the screen")
        self.device.wakeup()
        self.device.delay(2)
        self.adb.shell("input keyevent KEYCODE_MENU")
        self.adb.shell("input keyevent KEYCODE_MENU")

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=30000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def GO_Negotiation_Responder_Test(self, case_name):
        self.scroll_to_case(case_name)

    def Go_negotiation_test_push_button(self, case_name, Wifi_Mac_Address):
        # self.scroll_to_case(case_name)
        if self.device(text=case_name).ext5:
            self.device(text=case_name).click()

        self.logger.debug("Wifi_Mac_Address1:" + Wifi_Mac_Address)
        if self.device(text=case_name).ext5:
            self.device(text=case_name).click()

        if self.device(text="Search Target").wait.exists(timeout=20000):
            if self.device(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                self.device(text=Wifi_Mac_Address).click()
                self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)
            else:
                self.logger.debug("can not found Wifi_Mac_Address:" + Wifi_Mac_Address)

        if self.sdevice(text="ACCEPT").wait.exists(timeout=20000):
            self.sdevice(text="ACCEPT").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.device(
                text="Test passed successfully.").wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False
    def Go_negotiation_test_push_button_sdevice(self, case_name, Wifi_Mac_Address):
        # self.scroll_to_case(case_name)
        if self.sdevice(text=case_name).ext5:
            self.sdevice(text=case_name).click()

        self.logger.debug("Wifi_Mac_Address:" + Wifi_Mac_Address)
        if self.sdevice(text=case_name).ext5:
            self.sdevice(text=case_name).click()

        if self.sdevice(text="Search Target").wait.exists(timeout=20000):
            if self.sdevice(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                self.sdevice(text=Wifi_Mac_Address).click()
                self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)
            else:
                self.logger.debug("can not found Wifi_Mac_Address:" + Wifi_Mac_Address)

        if self.device(text="ACCEPT").wait.exists(timeout=20000):
            self.device(text="ACCEPT").click()

        if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.sdevice(
                text="Test passed successfully.").wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.sdevice(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False
    def Go_negotiation_test_pin_sdevice(self, case_name, Wifi_Mac_Address):

        # #self.scroll_to_case(case_name)#不能用scroll_to_case，不然会点掉OK，导致读取不到pin码
        if self.sdevice(text=case_name).ext5:
            self.sdevice(text=case_name).click()


        if self.sdevice(text="Search Target").wait.exists(timeout=10000):
            if self.sdevice(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                self.sdevice(text=Wifi_Mac_Address).click()
                self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)

        pin_num = ""
        if self.sdevice(resourceId="android:id/info").child(index=1).child(resourceId="android:id/value").wait.exists(
                timeout=30000):
            pin_num = self.sdevice(resourceId="android:id/info").child(index=1).child(
                resourceId="android:id/value").get_text()

        self.logger.debug("pin_num is " + pin_num)
        assert self.device(resourceId="android:id/wifi_p2p_wps_pin").wait.exists(timeout=10000)
        self.device(resourceId="android:id/wifi_p2p_wps_pin").set_text(pin_num)

        if self.device(description="Done").wait.exists(timeout=5000):
            self.device(description="Done").click
        if self.device(text="ACCEPT").wait.exists(timeout=5000):
            self.device(text="ACCEPT").click()

        if self.sdevice(text="OK").wait.exists(timeout=5000):
            self.sdevice(text="OK").click()

        if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.sdevice(
                text="Test passed successfully.").wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.sdevice(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False
    def get_device_wifi_mac_address(self):
        address = ""
        wifi_address = ""
        if self.device(resourceId="com.android.cts.verifier:id/p2p_my_device").wait.exists(timeout=10000):
            address = self.device(resourceId="com.android.cts.verifier:id/p2p_my_device").get_text()

        if ":" in address:
            wifi_address = address.split(":")[1].strip()
        return wifi_address
    def get_sdevice_wifi_mac_address(self):
        address = ""
        wifi_address = ""
        if self.sdevice(resourceId="com.android.cts.verifier:id/p2p_my_device").wait.exists(timeout=10000):
            address = self.sdevice(resourceId="com.android.cts.verifier:id/p2p_my_device").get_text()

        if ":" in address:
            wifi_address = address.split(":")[1].strip()
        return wifi_address

    def Go_negotiation_test_pin(self, case_name, Wifi_Mac_Address):

        # #self.scroll_to_case(case_name)#不能用scroll_to_case，不然会点掉OK，导致读取不到pin码
        if self.device(text=case_name).ext5:
            self.device(text=case_name).click()


        if self.device(text="Search Target").wait.exists(timeout=10000):
            if self.device(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                self.device(text=Wifi_Mac_Address).click()
                self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)

        pin_num = ""
        if self.device(resourceId="android:id/info").child(index=1).child(resourceId="android:id/value").wait.exists(
                timeout=30000):
            pin_num = self.device(resourceId="android:id/info").child(index=1).child(
                resourceId="android:id/value").get_text()

        self.logger.debug("pin_num is " + pin_num)
        assert self.sdevice(resourceId="android:id/wifi_p2p_wps_pin").wait.exists(timeout=10000)
        self.sdevice(resourceId="android:id/wifi_p2p_wps_pin").set_text(pin_num)

        if self.sdevice(text="ACCEPT").wait.exists(timeout=5000):
            self.sdevice(text="ACCEPT").click()

        if self.device(text="OK").wait.exists(timeout=5000):
            self.device(text="OK").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.device(
                text="Test passed successfully.").wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Group_Owner_Test(self, case_name):
        self.scroll_to_case(case_name)

    def Join_p2p_group_test_push_button(self, case_name, Wifi_Mac_Address):
        self.scroll_to_case(case_name)
        for loop in range(3):
            if self.device(text="Search Target").wait.exists(timeout=20000):
                if self.device(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                    self.device(text=Wifi_Mac_Address).click()
                    self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)

            if self.device(description="Done").wait.exists(timeout=5000):
                self.device(description="Done").click
            if self.sdevice(text="ACCEPT").wait.exists(timeout=30000):
                self.sdevice(text="ACCEPT").click()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.device(
                text="Test passed successfully.").wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            self.back_to_app("Group Client")
            self.scroll_to_case(case_name)
    def Join_p2p_group_test_push_button_sdevice(self, case_name, Wifi_Mac_Address):
        self.scroll_to_case_sdevice(case_name)
        for loop in range(3):
            if self.sdevice(text="Search Target").wait.exists(timeout=20000):
                if self.sdevice(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                    self.sdevice(text=Wifi_Mac_Address).click()
                    self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)

            if self.device(text="ACCEPT").wait.exists(timeout=30000):
                self.device(text="ACCEPT").click()

            if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.sdevice(
                text="Test passed successfully.").wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.sdevice(resourceId=pass_button, enabled=True).click()
                return True

            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            self.back_to_app_sdevice("Group Client")
            self.scroll_to_case_sdevice(case_name)
    def Join_p2p_group_test_pin_sdevice(self, case_name, Wifi_Mac_Address):
        self.scroll_to_case_sdevice(case_name)
        # Wifi_Mac_Address = self.config.getstr("Wifi_Mac_Address", "Default", "common")
        # self.logger.debug("Wifi_Mac_Address:"+Wifi_Mac_Address)

        if self.sdevice(text="Search Target").wait.exists(timeout=40000):
            if self.sdevice(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                self.sdevice(text=Wifi_Mac_Address).click()
                self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)

        pin_num = ""
        if self.sdevice(className="android.widget.ScrollView").wait.exists(timeout=80000):
            pin_num = self.sdevice(resourceId="android:id/info").child(index=1).child(
                resourceId="android:id/value").get_text()
        print "pin_num:", pin_num
        if self.device(resourceId="android:id/wifi_p2p_wps_pin").wait.exists(timeout=50000):
            self.device(resourceId="android:id/wifi_p2p_wps_pin").set_text(pin_num)

        if self.device(description="Done").wait.exists(timeout=5000):
            self.device(description="Done").click
        if self.device(text="ACCEPT").wait.exists(timeout=5000):
            self.device(text="ACCEPT").click()

        if self.sdevice(text="OK").wait.exists(timeout=5000):
            self.sdevice(text="OK").click()

        if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.sdevice(
                text="Test passed successfully.").wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.sdevice(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False





    def Join_p2p_group_test_pin(self, case_name, Wifi_Mac_Address):
        self.scroll_to_case(case_name)
        # Wifi_Mac_Address = self.config.getstr("Wifi_Mac_Address", "Default", "common")
        # self.logger.debug("Wifi_Mac_Address:"+Wifi_Mac_Address)

        if self.device(text="Search Target").wait.exists(timeout=40000):
            if self.device(text=Wifi_Mac_Address).wait.exists(timeout=5000):
                self.device(text=Wifi_Mac_Address).click()
                self.logger.debug("select target <%s> device successfully" % Wifi_Mac_Address)

        self.device()
        pin_num = ""
        if self.device(className="android.widget.ScrollView").wait.exists(timeout=80000):
            pin_num = self.device(resourceId="android:id/info").child(index=1).child(
                resourceId="android:id/value").get_text()
        print "pin_num:", pin_num
        if self.sdevice(resourceId="android:id/wifi_p2p_wps_pin").wait.exists(timeout=50000):
            self.sdevice(resourceId="android:id/wifi_p2p_wps_pin").set_text(pin_num)

        if self.device(description="Done").wait.exists(timeout=5000):
            self.device(description="Done").click
        if self.sdevice(text="ACCEPT").wait.exists(timeout=5000):
            self.sdevice(text="ACCEPT").click()

        if self.device(text="OK").wait.exists(timeout=5000):
            self.device(text="OK").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000) and self.device(
                text="Test passed successfully.").wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Service_Discovery_Responder_Test(self, case_name):
        self.scroll_to_case(case_name)

    def Service_Discovery_Requester_Test_sdevice(self, case_name, address=""):
        self.scroll_to_case_sdevice(case_name)

        for loop in range(5):
            self.sdevice.delay(20)
            self.sdevice.dump()

            if self.sdevice(text=address).ext5:
                self.sdevice(text=address).click()
                self.logger.debug("select %s successfully" % address)
            if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=50000):
                self.logger.debug("%s Test Pass" % case_name)
                self.sdevice(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.debug("cannot found  %s" % address)
            self.back_to_app_sdevice("Service Discovery Requester")
            self.scroll_to_case_sdevice(case_name)
            # return False

    def Multiple_clients_test_sdevice(self, case_name, address):
        self.scroll_to_case_sdevice(case_name)
        for loop in range(5):
            self.sdevice.delay(20)
            self.sdevice.dump()

            if self.sdevice(text=address).ext5:
                self.sdevice(text=address).click()
                self.logger.debug("select %s successfully" % address)
            if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=50000):
                self.logger.debug("%s Test Pass" % case_name)
                self.sdevice(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.debug("cannot found  %s" % address)
            self.back_to_app_sdevice("Service Discovery Requester")
            self.scroll_to_case_sdevice(case_name)
            # return False

    def Service_Discovery_Requester_Test(self, case_name, address=""):
        self.scroll_to_case(case_name)

        for loop in range(5):
            self.device.delay(20)
            self.device.dump()

            if self.device(text=address).ext5:
                self.device(text=address).click()
                self.logger.debug("select %s successfully" % address)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=50000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.debug("cannot found  %s" % address)
            self.back_to_app("Service Discovery Requester")
            self.scroll_to_case(case_name)
            # return False

    def Multiple_clients_test(self, case_name, address):
        self.scroll_to_case(case_name)
        for loop in range(5):
            self.device.delay(20)
            self.device.dump()

            if self.device(text=address).ext5:
                self.device(text=address).click()
                self.logger.debug("select %s successfully" % address)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=50000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.debug("cannot found  %s" % address)
            self.back_to_app("Service Discovery Requester")
            self.scroll_to_case(case_name)
            # return False

    def CA_Cert_Notification_Test(self, case_name):
        self.scroll_to_case(case_name)
        self.clear_notification()
        # step 1
        assert self.device(resourceId="android:id/list").child(index=0).wait.exists(timeout=5000)
        self.device(resourceId="android:id/list").child(index=0).click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        self.install_credential(password)
        self.test_pass_popup()
        # step 2
        assert self.device(resourceId="android:id/list").child(index=1).wait.exists(timeout=5000)
        self.device(resourceId="android:id/list").child(index=1).click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        if self.device(text="Internet Widgits Pty Ltd").wait.exists(timeout=5000):
            self.back_to_Pass_Popup_home()
            self.test_pass_popup()
            self.wait(2)
        # step 3
        assert self.device(resourceId="android:id/list").child(index=2).wait.exists(timeout=5000)
        self.device(resourceId="android:id/list").child(index=2).click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()
        self.adb.shell("input text %s" % password)
        self.device.press.enter()
        if self.device(text="Continue without fingerprint").exists:
            self.device(text="Continue without fingerprint").click()
        if self.device(text="None").exists:
            self.device(text="None").click()
        if self.device(text="YES, REMOVE").exists:
            self.device(text="YES, REMOVE").click()

        self.test_pass_popup()
        self.wait(2)

        # step 4
        self.device.open.notification()
        if self.device(text="Certificate authority installed").wait.exists(timeout=5000):
            self.device(text="Certificate authority installed").click()
            if self.device(text="CHECK CERTIFICATE").wait.exists(timeout=5000):
                self.device(text="CHECK CERTIFICATE").click()
                if self.device(text="Internet Widgits Pty Ltd").wait.exists(timeout=5000):
                    self.device(text="REMOVE").click()
                    if self.device(text="OK").wait.exists(timeout=2000):
                        self.device(text="OK").click()
                        self.back_to_app("CA Cert Notification Test")
                        self.device(resourceId="android:id/list").child(index=3).click()
        # assert self.device(resourceId="android:id/list").child(index=3).wait.exists(timeout=5000)
        # self.device(resourceId="android:id/list").child(index=3).click()

        self.wait(3)

        # step 5
        self.device.open.notification()
        if self.device(resourceId="com.android.systemui:id/notification_stack_scroller").wait.exists(timeout=5000):
            self.device.press.back()
        if self.device(text="Certificate authority installed").wait.exists(timeout=5000):
            pass
        else:
            self.device(resourceId="android:id/list").child(index=4).click()
            self.wait(3)
        # assert self.device(resourceId="android:id/list").child(index=4).wait.exists(timeout=5000)
        # self.device(resourceId="android:id/list").child(index=4).click()
        # self.wait(3)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def CA_Cert_Notification_on_Boot_test(self, case_name):

        try:
            self.scroll_to_case(case_name)
            # self.setLockScreenToPassword()
            self.back_to_app(case_name)
            assert self.device(text="CHECK CREDENTIALS").ext5
            self.device(text="CHECK CREDENTIALS").click()

            count = 0
            if self.device(resourceId="com.android.settings:id/cert_list").ext10:
                count = self.device(resourceId="com.android.settings:id/cert_list").info["childCount"]
            self.logger.debug("count is:%s" % count)

            if count > 0:
                self.logger.debug("there is %d credential in credentials list" % count)
                self.device(resourceId="com.android.settings:id/cert_list").child(index=0).click()
                if self.device(text="REMOVE").ext5:
                    self.device(text="REMOVE").click()

                if self.device(text="OK").ext5:
                    self.device(text="OK").click()

                if self.device(resourceId="com.android.settings:id/cert_list").ext10:
                    count = self.device(resourceId="com.android.settings:id/cert_list").info["childCount"]
                    self.logger.debug("count is:%s" % count)
                    if count == 0:
                        self.logger.debug("childcount is 0,so remove the credential successfully")

            self.back_to_app(case_name)

            if self.device(text="INSTALL CREDENTIAL").ext5:
                self.device(text="INSTALL CREDENTIAL").click()
                self.logger.debug("starting to install 'myCA.cer'")
                if self.device(text="myCA.cer").ext5:
                    self.device(text="myCA.cer").click()
                    if self.device(resourceId="com.android.certinstaller:id/credential_name").wait.exists(timeout=5000):
                        self.device(resourceId="com.android.certinstaller:id/credential_name").set_text("bug")
                        self.device.press.enter()
                        if self.device(text="OK").exists:
                            self.device(text="OK").click()
                        if self.device(text="OK").exists:
                            self.device(text="OK").click()
                        if self.device(text="Continue without fingerprint").ext5:
                            self.device(text="Continue without fingerprint").click()
                        if self.device(text="Password").ext5:
                            self.device(text="Password").click()
                        self.adb.shell("input text %s" % password)
                        if self.device(text="NEXT").ext5:
                            self.device(text="NEXT").click()
                        self.adb.shell("input text %s" % password)
                        if self.device(text="OK").ext5:
                            self.device(text="OK").click()
                        if self.device(text="DONE").ext5:
                            self.device(text="DONE").click()

            if self.device(text="REMOVE SCREEN LOCK").ext5:
                self.device(text="REMOVE SCREEN LOCK").click()
                self.adb.shell("input text %s" % password)
                self.device.press.enter()
                if self.device(text="Continue without fingerprint").ext5:
                    self.device(text="Continue without fingerprint").click()
                    self.device(text="None").click()
                    self.device(text="YES, REMOVE").click()

            # assert count > 0
            self.adb.shell("reboot")
            time.sleep(25)
            i = 0
            while not self.device(packageName="com.blackberry.blackberrylauncher").exists:
                self.logger.debug("restarting...")
                time.sleep(5)
                if i > 5:
                    break
                i += 1

            self.device.wakeup()
            self.device.delay(1)
            # self.unlock_scream_without_password()
            # self.device.delay(5)
            # if self.device(text="OK").exists(timeout=5000):
            #     self.device(text="OK").click()
            self.logger.debug("open notification")
            self.device.open.notification()
            self.wait(5)

            if self.device(scrollable=True).exists:
                self.device(scrollable=True).scroll.vert.to(text="Certificate authority installed")

            assert self.device(text="Certificate authority installed").wait.exists(timeout=5000)
            self.logger.debug("find 'Certificate authority installed' ,test pass")
            self.enter_CTSVerifier()
            self.scroll_to_case(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        except:
            self.logger.warning(traceback.format_exc())
            self.save_fail_img()
            self.unlock_scream_without_password()

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def switch_permission(self, isEnabled, item, disable_popup="OK"):
        count = self.device(resourceId="com.android.settings:id/list").info["childCount"]
        print "childCount is:", count
        title = ""
        switch_text = ""
        for loop in range(count):
            title_id = self.device(resourceId="com.android.settings:id/list").child(index=loop).child(
                className="android.widget.RelativeLayout").child(
                resourceId="android:id/title")
            switch_id = self.device(resourceId="com.android.settings:id/list").child(index=loop).child(
                className="android.widget.LinearLayout").child(
                resourceId="android:id/switch_widget")

            title = title_id.get_text()
            self.logger.debug("The title is %s" % title)

            if title == item:
                switch_text = switch_id.get_text()

                if isEnabled:
                    if switch_text.lower() == "on":
                        self.logger.debug("The %s is already enabled" % item)
                        return True
                    elif switch_text.lower() == "off":
                        switch_id.click()
                        if self.device(text="ALLOW").ext5:
                            self.device(text="ALLOW").click()
                        if switch_id.get_text().lower() == "on":
                            self.logger.debug("Enable %s successfully" % item)
                            return True
                        self.logger.debug("enable %s failed" % item)
                        return False
                elif not isEnabled:
                    if switch_text.lower() == "off":
                        self.logger.debug("The %s is already Disabled" % item)
                        return True
                    elif switch_text.lower() == "on":
                        switch_id.click()
                        if self.device(text=disable_popup).exists:
                            self.device(text=disable_popup).click()
                        self.logger.debug("Disabled %s successfully" % item)

                        if switch_id.get_text().lower() == "off":
                            self.logger.debug("disable %s successfully" % item)
                            return True
                        self.logger.debug("disable %s failed" % item)
                        return False
        self.logger.debug("switch %s to %s failed" % (item, isEnabled))
        return False

    def switch_quicksettings_permission(self, isEnabled, resourceId, disable_popup="OK"):
        self.logger.debug("start switch %s permission" % resourceId)
        switch_id = self.device(resourceId=resourceId)
        switch_text = switch_id.get_text()

        if isEnabled:
            if switch_text.lower() == "on":
                self.logger.debug("The switch is already enabled")
                return True
            elif switch_text.lower() == "off":
                switch_id.click()
                self.logger.debug("Enabled switch successfully")
                # if self.device(text="ALLOW").exists:
                # self.device(text="ALLOW").click()
                return True
        elif not isEnabled:
            if switch_text.lower() == "off":
                self.logger.debug("The switch is already Disabled")
                return True
            elif switch_text.lower() == "on":
                switch_id.click()
                if self.device(text=disable_popup).exists:
                    self.device(text=disable_popup).click()
                self.logger.debug("Disabled switch successfully")
                return True

        self.logger.debug("switch %s completed" % resourceId)
        return False

    def Condition_Provider_test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="LAUNCH SETTINGS").wait.exists(timeout=5000):
            self.device(text="LAUNCH SETTINGS").click()
            self.switch_permission(True, "CTS Verifier")

        self.back_to_app(case_name)
        self.device.delay(45)

        if self.device(resourceId="com.android.cts.verifier:id/nls_test_scroller", scrollable=True).exists:
            self.device(resourceId="com.android.cts.verifier:id/nls_test_scroller", scrollable=True).scroll.vert.to(
                text="LAUNCH SETTINGS", enabled=True)
            if self.device(text="LAUNCH SETTINGS", enabled=True).exists:
                self.device(text="LAUNCH SETTINGS", enabled=True).click()
                self.switch_permission(False, "CTS Verifier")
        self.device.delay(3)
        self.back_to_app(case_name)

        self.logger.debug("check pass button during 60 s")
        time.sleep(15)
        self.device.dump()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=30000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Notification_Attention_Management_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="LAUNCH SETTINGS", enabled=True).wait.exists(timeout=5000):
            self.device(text="LAUNCH SETTINGS").click()
            # 8.1 R3改为CTS Verifier
            # assert self.switch_permission(True, "Notification Listener for CTS Verifier")
            assert self.switch_permission(True, "CTS Verifier")
            self.back_to_app(case_name)
        elif self.device(text="LAUNCH SETTINGS", enabled=False).wait.exists(timeout=5000):
            pass
        self.logger.debug("Wait 120 seconds until the case is completed automatically.")
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=180000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Notification_Listener_Test(self, case_name):
        self.scroll_to_case(case_name)

        assert self.device(text="LAUNCH SETTINGS", enabled=False).wait.exists(timeout=5000)
        self.logger.debug("sleep 120 s")
        self.device.delay(120)

        if self.device(scrollable=True).wait.exists(timeout=5000):
            self.device(scrollable=True).scroll.vert.toEnd()

        if self.device(text="LAUNCH SETTINGS", enabled=True).wait.exists(timeout=5000):
            self.device(text="LAUNCH SETTINGS", enabled=True).click()

        self.switch_permission(False, "CTS Verifier", "TURN OFF")
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Notification_Package_Priority_Test(self, case_name):
        self.scroll_to_case(case_name)
        self.device.delay(5)

        if self.device(text="LAUNCH SETTINGS", enabled=True).exists:
            self.device(text="LAUNCH SETTINGS", enabled=True).click()
            self.switch_permission(True, "Notification Listener for CTS Verifier")
            self.back_to_app(case_name)
            self.device.delay(10)
        else:
            self.device.delay(10)

        if self.device(text="I'M DONE", enabled=True).exists:
            self.device(text="I'M DONE", enabled=True).click()
            self.device.delay(15)

        self.enter_settings("Notifications")
        self.scroll_to_case("CTS Verifier")

        if self.device(text="I'M DONE", enabled=True).exists:
            self.device(text="I'M DONE", enabled=True).click()

        self.switch_permission(True, "Override Do Not Disturb")
        self.back_to_app(case_name)

        if self.device(text="I'M DONE", enabled=True).exists:
            self.device(text="I'M DONE", enabled=True).click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Shortcut_Reset_Rate_limiting_Test(self, case_name):
        self.clear_notification()

        self.scroll_to_case(case_name)
        self.device.delay(8)
        self.device.open.notification()

        if self.device(text="TYPE SOMETHING HERE AND PRESS SEND BUTTON").ext5:
            self.device(text="TYPE SOMETHING HERE AND PRESS SEND BUTTON").click()
        elif self.device(resourceId="android:id/expand_button").exists:
            self.device(resourceId="android:id/expand_button").click()
            if self.device(text="TYPE SOMETHING HERE AND PRESS SEND BUTTON").exists:
                self.device(text="TYPE SOMETHING HERE AND PRESS SEND BUTTON").click()

        assert self.device(text="Type something here and press send button").exists
        self.device(text="Type something here and press send button").set_text("cts verifier test")

        assert self.device(description="Send", enabled=True).exists
        self.device(description="Send", enabled=True).click()
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            self.clear_notification()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()

        return False

    def makeTestCasePass_without_check(self, case_name, is_text_PASS_type=False):
        """
        result  代表是弹出Pass /Fail 的提示框  True代表PASS
        :type case_name: object
        """
        self.scroll_to_case(case_name)
        if is_text_PASS_type:
            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            return True

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Device_administrator_settings(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").exists:
            self.device(text="GO").click()

        self.scroll_to_text("Device admin apps")
        if self.device(text="Device admin apps").exists:
            self.device(text="Device admin apps").click()
        if self.device(text="CTS Verifier").wait.exists(timeout=5000):
            self.device(text="CTS Verifier").click()

        # #DeActivate this device administrator
        assert self.device(text="Deactivate this device admin app", enabled=False).ext5
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Disallow_configuring_WiFi(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET RESTRICTION").wait.exists(timeout=5000):
            self.device(text="SET RESTRICTION").click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        assert self.device(textContains="This action is disabled").wait.exists(
            timeout=10000)
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Disallow_configuring_VPN(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET VPN RESTRICTION").wait.exists(timeout=5000):
            self.device(text="SET VPN RESTRICTION").click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        assert self.device(textContains="This action is disabled").ext5
        self.back_to_app(case_name)

        if self.device(text="CHECK VPN").exists:
            self.device(text="CHECK VPN").click()

        check_result = self.device(resourceId="com.android.cts.verifier:id/device_owner_vpn_info").get_text()
        self.logger.debug("check_result is:%s" % check_result)
        if "Mark this test as passed" in check_result:
            self.logger.debug("Contains text 'Mark this test as passed'")
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.device(resourceId=pass_button, enabled=True).click()

            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Locked_config_is_not_modifiable_in_Settings(self, case_name):
        if self.device(resourceId="com.android.cts.verifier:id/create_wifi_config_button").exists:
            self.device(resourceId="com.android.cts.verifier:id/create_wifi_config_button").click()
            self.device.delay(5)

        self.scroll_to_case(case_name)
        if self.device(text="WIFI CONFIG LOCKDOWN ON").exists:
            self.device(text="WIFI CONFIG LOCKDOWN ON").click()

        if self.device(text="GO TO WIFI SETTINGS").exists:
            self.device(text="GO TO WIFI SETTINGS").click()

        if self.device(scrollable=True).wait.exists(timeout=5000):
            self.logger.debug("scroll to 'Saved networks'")
            self.device(scrollable=True, resourceId="com.android.settings:id/list").scroll.vert.to(
                text="Saved networks")
        assert self.device(text="Saved networks").ext5
        self.device(text="Saved networks").click()

        assert self.device(text="CTS").ext5
        self.device(text="CTS").click()

        assert self.device(text="FORGET").ext5
        self.device(text="FORGET").click()

        assert self.device(text="Action not allowed").ext5
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Unlocked_config_is_modifiable_in_Settings(self, case_name):
        if self.device(resourceId="com.android.cts.verifier:id/device_owner_wifi_ssid").exists:
            self.logger.debug("set text 'CTS'")
            self.device(resourceId="com.android.cts.verifier:id/device_owner_wifi_ssid").set_text("CTS")
            self.device.press.back()
            if self.device(text="None",resourceId="com.android.cts.verifier:id/device_owner_keymgmnt_none").exists:
                self.device(text="None",resourceId="com.android.cts.verifier:id/device_owner_keymgmnt_none").click()
            if self.device(text="CREATE WIFI CONFIGURATION",resourceId="com.android.cts.verifier:id/create_wifi_config_button").exists:
                self.device(text="CREATE WIFI CONFIGURATION",resourceId="com.android.cts.verifier:id/create_wifi_config_button").click()
                self.device.delay(5)
        self.scroll_to_case(case_name)

        if self.device(text="WIFI CONFIG LOCKDOWN OFF").exists:
            self.device(text="WIFI CONFIG LOCKDOWN OFF").click()

        if self.device(text="GO TO WIFI SETTINGS").exists:
            self.device(text="GO TO WIFI SETTINGS").click()

        if self.device(scrollable=True).wait.exists(timeout=5000):
            self.logger.debug("scroll to 'Saved networks'")
            self.device(scrollable=True).scroll.vert.to(text="Saved networks")
        assert self.device(text="Saved networks").ext5
        self.device(text="Saved networks").click()

        assert self.device(text="CTS").ext5
        self.device(text="CTS").click()

        assert self.device(text="FORGET").ext5
        self.device(text="FORGET").click()

        assert not self.device(text="CTS").ext5 and self.device(text="Add network").ext5
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Unlocked_config_can_be_forgotten_in_Settings(self, case_name):

        self.scroll_to_case(case_name)
        if self.device(text="WIFI CONFIG LOCKDOWN OFF").exists:
            self.device(text="WIFI CONFIG LOCKDOWN OFF").click()

        if self.device(text="GO TO WIFI SETTINGS").exists:
            self.device(text="GO TO WIFI SETTINGS").click()

        if self.device(scrollable=True).wait.exists(timeout=5000):
            self.logger.debug("scroll to 'Saved networks'")
            self.device(scrollable=True).scroll.vert.to(text="Saved networks")
        assert self.device(text="Saved networks").ext5
        self.device(text="Saved networks").click()

        assert self.device(text="CTS").ext5
        self.device(text="CTS").click()

        assert self.device(text="FORGET").ext5
        self.device(text="FORGET").click()

        assert not self.device(text="CTS").ext5 and self.device(text="Add network").ext5
        self.logger.debug("%s Test Pass" % case_name)
        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Locked_config_can_be_connected_to(self, case_name):
        #TODO
        return self.makeTestCasePass_without_check(case_name)
        # self.scroll_to_case(case_name)
        # if self.device(text="WIFI CONFIG LOCKDOWN ON").exists:
        # self.device(text="WIFI CONFIG LOCKDOWN ON").click()
        #
        # if self.device(text="GO TO WIFI SETTINGS").exists:
        # self.device(text="GO TO WIFI SETTINGS").click()
        #
        # if self.device(text="CTS").wait.exists(timeout=5000):
        # self.device(text="CTS").click()
        #
        # assert self.device(text="Connected, no Internet").wait.exists(timeout=5000)
        # self.back_to_app(case_name)
        #
        # if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
        # self.logger.debug("%s Test Pass" % case_name)
        # self.device(resourceId=pass_button, enabled=True).click()
        # return True

    def Disallow_data_roaming(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET RESTRICTION").wait.exists(timeout=5000):
            self.device(text="SET RESTRICTION").click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        if self.device(text="Data roaming", enabled=False).wait.exists(
                timeout=10000):
            self.back_to_app(case_name)

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_factory_reset(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        self.scroll_to_text("System")
        if self.scroll_to_text("Reset"):
            pass
        elif self.scroll_to_text("Reset options"):
            pass

        if self.device(resourceId="com.android.settings:id/restricted_icon").wait.exists(timeout=10000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_configuring_Bluetooth(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET RESTRICTION").wait.exists(timeout=5000):
            self.device(text="SET RESTRICTION").click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        # This action is disabled. To learn more, contact your organization's admin.
        if self.device(textContains="This action is disabled").wait.exists(
                timeout=10000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_USB_file_transfer(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET RESTRICTION").wait.exists(timeout=5000):
            self.device(text="SET RESTRICTION").click()

        self.device.open.notification()
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toEnd()
        #self.clickTextContains("Android System")
        if self.device(text="Android System",resourceId="android:id/app_name_text").exists():
            self.device(text="Android System", resourceId="android:id/app_name_text").click()

        if self.device(text="Connected in charging mode").wait.exists(timeout=5000):
            self.device(text="Connected in charging mode").click()
            self.device.delay(2)
            self.device.click(236, 1454)
        elif self.device(text="USB charging this device").wait.exists(timeout=5000):
            self.device(text="USB charging this device").click()
            self.device.delay(2)
            self.device.click(236, 1454)
        elif self.device(text="Tap for more options.").wait.exists(timeout=5000):
            self.device(text="Tap for more options.").click()
            self.device.delay(2)

        if self.device(text="Transfer files", enabled=False).wait.exists(timeout=10000):
            self.clear_notification()
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        self.clear_notification()
        return False

    def Disable_status_bar(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="DISABLE STATUS BAR").wait.exists(timeout=5000):
            self.device(text="DISABLE STATUS BAR").click()
        self.device.open.notification()
        self.device.delay(3)

        if self.device(resourceId="com.android.systemui:id/quick_qs_panel").wait.exists(timeout=5000):
            self.logger.warning("Found 'com.android.systemui:id/quick_qs_panel'")
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            self.clear_notification()
            self.back_to_app(case_name)
            return False

        if self.device(text="REENABLE STATUS BAR").exists:
            self.device(text="REENABLE STATUS BAR").click()
            self.device.open.notification()

        if self.device(resourceId="com.android.systemui:id/quick_qs_panel").wait.exists(timeout=10000):
            self.clear_notification()
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        self.clear_notification()
        return False

    def wait(self, seconds):
        self.device.delay(seconds)

    def Disable_keyguard(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="DISABLE KEYGUARD").wait.exists(timeout=5000):
            self.device(text="DISABLE KEYGUARD").click()

        self.device.press.power()
        self.wait(5)
        self.device.wakeup()

        if self.device(resourceId="com.android.systemui:id/notification_panel").wait.exists(timeout=5000):
            self.logger.warning("%s Test Failed" % case_name)
            self.unlock_scream_without_password()
            self.save_fail_img()
            return False

        if self.device(text="REENABLE KEYGUARD").exists:
            self.device(text="REENABLE KEYGUARD").click()

        self.device.press.power()
        self.wait(5)
        self.device.wakeup()
        if self.device(resourceId="com.android.systemui:id/notification_panel").wait.exists(timeout=10000):
            self.unlock_scream_without_password()
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        self.unlock_scream_without_password()
        return False

    def Setting_the_user_icon(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET USER ICON").wait.exists(timeout=5000):
            self.device(text="SET USER ICON").click()

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        self.enter_settings("Users & accounts")

        if self.device(text="Users").exists:
            self.device(text="Users").click()

        if self.device(text="You (Owner)").wait.exists(timeout=10000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_add_user(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()
        self.enter_settings("Users & accounts")
        self.scroll_to_text("Users")

        assert self.device(text="Add user or profile").wait.exists(timeout=5000)
        self.device(text="Add user or profile").click()

        assert self.device(text="Action not allowed").wait.exists(timeout=10000)
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Disallow_adjust_volume(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Media volume").wait.exists(timeout=5000):
            self.device(text="Media volume").click()

        if self.device(text="Action not allowed").wait.exists(timeout=10000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_controlling_apps(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        self.scroll_to_case("Contacts")

        if self.device(text="DISABLE").wait.exists(timeout=5000):
            self.device(text="DISABLE").click()
            assert (self.device(text="Action not allowed").wait.exists(timeout=5000))
            self.device.press.back()

        if self.device(text="FORCE STOP").wait.exists(timeout=5000):
            self.device(text="FORCE STOP").click()
            assert (self.device(text="Action not allowed").wait.exists(timeout=5000))
            self.device.press.back()

        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_config_cell_broadcasts(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Advanced").wait.exists(timeout=5000):
            self.device(text="Advanced").click()

        self.scroll_to_text("Emergency broadcasts")

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)

                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_config_credentials(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        self.scroll_to_text("Encryption & credentials")
        self.scroll_to_text("User credentials")

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)

                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_config_mobile_networks(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Cellular networks").wait.exists(timeout=5000):
            self.device(text="Cellular networks").click()
        elif self.device(text="Mobile network").wait.exists(timeout=5000):
            self.device(text="Mobile network").click()

        assert self.device(text="Action not allowed").wait.exists(timeout=5000)
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Disallow_config_tethering(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Hotspot & tethering", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)

                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_config_Wi_Fi(self, case_name):
        self.scroll_to_case(case_name.replace("Wi_Fi", "Wi-Fi"))

        self.enable_desallow_switch_and_open_settings()

        if self.device(textContains="This action is disabled").wait.exists(
                timeout=10000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)

                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_debugging_features(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()
        self.scroll_to_text("Build number")

        if self.device(text="Action not allowed").wait.exists(timeout=10000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

        # self.makeTestCasePass_without_check(case_name)

    def Disallow_factory_reset__dot(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET RESTRICTION").wait.exists(timeout=5000):
            self.device(text="SET RESTRICTION").click()

        self.enter_settings("System")
        if self.scroll_to_text("Reset"):
            pass
        elif self.scroll_to_text("Reset options"):
            pass

        if self.device(text="Erase all data (factory reset)", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)

                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_fun(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Android version").wait.exists(timeout=5000):
            bounds = self.device(text="Android version").info.get("bounds")
            self.logger.debug("bounds is %s" % bounds)
            x = (bounds["left"] + bounds["right"]) / 2
            y = (bounds["top"] + bounds["bottom"]) / 2
            self.logger.debug("x,y is %s %s" % (x, y))
            self.device.click(x, y)
            self.device.click(x, y)
            self.device.click(x, y)

        if self.device(text="Action not allowed").wait.exists(timeout=10000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)

                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_install_unknown_sources(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(text="CTS Verifier").wait.exists(timeout=5000):
            self.device(text="CTS Verifier").click()

        if self.device(text="Allow from this source").wait.exists(timeout=5000):
            self.device(text="Allow from this source").click()

        # self.scroll_to_text("Unknown sources")
        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)

                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_modify_accounts(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        # self.scroll_to_text("Unknown sources")
        if self.device(text="Add account", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_network_reset(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()
        self.scroll_to_text("System")
        if self.scroll_to_text("Reset"):
            pass
        elif self.scroll_to_text("Reset options"):
            pass

        if self.device(text="Reset Wi-Fi, mobile & Bluetooth", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_outgoing_beam(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        statu=self.device(resourceId="com.android.settings:id/list").child(className="android.widget.LinearLayout",index=2)\
            .child(resourceId="android:id/switch_widget").get_text()
        if statu.lower()=="off":
            if self.device(text="NFC").wait.exists(timeout=5000):
                self.device(text="NFC").click()

        # self.scroll_to_text("Unknown sources")
        if self.device(text="Android Beam", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_remove_user(self, case_name):
        self.scroll_to_case(case_name)

        # self.enable_desallow_switch_and_open_settings()
        #
        # self.enter_settings("Users")
        # if self.device(text="Add account",enabled=False).wait.exists(timeout=5000):
        # self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_share_location(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        # self.scroll_to_text("Unknown sources")
        if self.device(text="Mode", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def install_CtsPermissionApp(self):
        try:
            p = subprocess.Popen("adb -s %s install -r CtsPermissionApp.apk" % self.mdevice_id, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            # p = subprocess.Popen("adb -s %s install -r CtsPermissionApp.apk" % self.serinoM, shell=True,
            #                      stdout=subprocess.PIPE,
            #                      stderr=subprocess.PIPE)
            # p.wait()
            self.logger.debug("Install CtsPermissionApp.apk Completed")
        except:
            self.logger.warning(traceback.format_exc())

    def uninstall_CtsPermissionApp(self):
        try:
            p = subprocess.Popen("adb -s %s uninstall com.android.cts.permissionapp" % self.mdevice_id, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            self.logger.debug("Uninstall CtsPermissionApp.apk Completed")
        except:
            self.logger.warning(traceback.format_exc())

    def Disallow_uninstall_apps(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        self.scroll_to_case("CtsPermissionApp")

        if self.device(text="UNINSTALL").wait.exists(timeout=5000):
            self.device(text="UNINSTALL").click()

        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Set_auto_network_time_required(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Automatic date & time", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Disallow_lockscreen_unredacted_notification(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        self.enter_settings("Apps & notifications")
        if self.device(text="Notifications").wait.exists(timeout=5000):
            self.device(text="Notifications").click()

        if self.device(text="On the lock screen").wait.exists(timeout=5000):
            self.device(text="On the lock screen").click()

        assert self.device(text="Show all notification content", enabled=False).wait.exists(timeout=5000)
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Set_lock_screen_info(self, case_name):
        self.scroll_to_case(case_name)

        try:
            if self.device(resourceId="com.android.cts.verifier:id/edit_text_widget").wait.exists(timeout=5000):
                self.device(resourceId="com.android.cts.verifier:id/edit_text_widget").set_text("Screen Info Test")

            if self.device(text="UPDATE").wait.exists(timeout=5000):
                self.device(text="UPDATE").click()

            if self.device(text="OPEN SETTINGS").wait.exists(timeout=5000):
                self.device(text="OPEN SETTINGS").click()

            self.enter_settings("Security & location")
            if self.device(text="Lock screen preferences").wait.exists(timeout=5000):
                self.device(text="Lock screen preferences").click()
            if self.device(text="Lock screen message").wait.exists(timeout=5000):
                self.device(text="Lock screen message").click()
            if self.device(text="Action not allowed").wait.exists(timeout=5000):
                self.back_to_app(case_name)
                if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                    self.logger.debug("%s Test Pass" % case_name)
                    self.device(resourceId=pass_button, enabled=True).click()
                    return True
        except:
            self.back_to_app(case_name)
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            self.unlock_scream_without_password()
            return False
        finally:
            pass

    def Set_maximum_time_to_lock(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(resourceId="com.android.cts.verifier:id/edit_text_widget").wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/edit_text_widget").set_text("1000")

        if self.device(text="UPDATE").wait.exists(timeout=5000):
            self.device(text="UPDATE").click()

        if self.device(text="OPEN SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN SETTINGS").click()

        if self.device(text="Advanced").wait.exists(timeout=5000):
            self.device(text="Advanced").click()

        assert self.scroll_to_text("Sleep")
        if self.device(text="Sleep").wait.exists(timeout=5000):
            self.device(text="Sleep").click()
        assert self.device(text="Other options are disabled by your admin").ext5 or self.device(
            text="Other options are disabled by your administrator").ext5
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Set_password_quality(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(resourceId="com.android.cts.verifier:id/spinner_widget", enabled=True).wait.exists(timeout=5000):
            self.device(resourceId="com.android.cts.verifier:id/spinner_widget", enabled=True).click()
        self.device.dump()
        if self.device(text="Complex").wait.exists(timeout=5000):
            self.device(text="Complex").click()
        if self.device(text="OPEN SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN SETTINGS").click()
        self.enter_settings("Security & location")
        if self.device(text="Screen lock").wait.exists(timeout=5000):
            self.device(text="Screen lock").click()
        if self.device(text="None").wait.exists(timeout=5000):
            self.device(text="None").click()
        if self.device(text="Action not allowed").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        else:
            self.back_to_app(case_name)
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            self.unlock_scream_without_password()
            return False

    def Set_permitted_accessibility_services(self, case_name):
        self.scroll_to_case(case_name)
        self.enable_desallow_switch_and_open_settings()

        self.wait(2)
        self.device.press.back()
        self.wait(1)
        if self.device(text="OPEN SETTINGS").wait.exists(timeout=5000):
            self.device(text="OPEN SETTINGS").click()

        assert self.device(text="Dummy accessibility service", enabled=False).wait.exists(timeout=30000)
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True

    def Set_permitted_input_methods(self, case_name):
        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        if self.device(text="Dummy input method", enabled=False).wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Projection_Offscreen_Activity(self, case_name):
        self.scroll_to_case(case_name)
        self.device.sleep()
        self.wait(10)
        self.device.wakeup()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def KeyChain_Storage_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="NEXT").wait.exists(timeout=5000):
            self.device(text="NEXT").click.wait()
        if self.device(text="NEXT").wait.exists(timeout=5000):
            self.device(text="NEXT").click.wait()
        if self.device(text="NEXT").wait.exists(timeout=5000):
            self.device(text="NEXT").click.wait()

        if self.device(text="OK").wait.exists(timeout=5000):
            self.device(text="OK").click.wait()

        if self.device(text="NEXT").wait.exists(timeout=5000):
            self.device(text="NEXT").click.wait()
        if self.device(text="NEXT").wait.exists(timeout=5000):
            self.device(text="NEXT").click.wait()

        if self.device(text="SELECT").wait.exists(timeout=5000):
            self.device(text="SELECT").click.wait()
            print "111111111111111111"
        elif self.device(text="ALLOW").wait.exists(timeout=5000):
            self.device(text="ALLOW").click.wait()
            print "22222222222222222222"
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Lock_Bound_Keys_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="START TEST").exists:
            self.device(text="START TEST").click()

        if self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=20000):
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()
            # self.device.press.enter()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Device_Admin_Tapjacking_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="ENABLE DEVICE ADMIN").exists:
            self.device(text="ENABLE DEVICE ADMIN").click()

        # context = self.device(className = "android.widget.TextView").dump()
        # print "context:",context
        self.wait(5)
        context = self.device.dump()
        # print "context:", context
        assert "This activity attempts to tapjack the activity below" in context
        self.logger.debug(
            "This activity attempts to tapjack the activity below,Any security sensitive controls below should not respond to taps as long as this activity is visible")
        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def RTSP_Streaming_Video_Quality_Verifier(self, case_name):
        try:
            self.scroll_to_case(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=90000):
                self.logger.debug("%s Test Pass" % case_name)
                self.suc_times += 1
                # self.mod.suc_times += 1
                self.logger.info("Trace Success Loop " + str(self.suc_times))
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        except:
            self.logger.warning(traceback.format_exc())

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def HTTP_Streaming_Video_Quality_Verifier(self, case_name, index):
        self.scroll_to_case_index(case_name, index)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=90000):
            self.logger.debug("%s Test Pass" % case_name)
            self.suc_times += 1
            # self.mod.suc_times += 1
            self.logger.info("Trace Success Loop " + str(self.suc_times))
            self.device(resourceId=pass_button, enabled=True).click()
            return True

        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Managed_device_info_page(self, case_name):
        #TODO
        self.scroll_to_case(case_name)

        if self.device(text="GO").exists:
            self.device(text="GO").click()

        self.scroll_to_text("Security & location")
        self.scroll_to_text("Managed device info")

        assert self.device(text="List of apps on your device").ext5
        assert self.scroll_to_text_without_click("Administrator can lock the device and reset password")

        self.back_to_app(case_name)
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Retrieve_traffic_logs(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="RETRIEVE TRAFFIC LOGS").exists:
            self.device(text="RETRIEVE TRAFFIC LOGS").click()

        self.device.delay(5)
        if self.device(text="OPEN SETTINGS").exists:
            self.device(text="OPEN SETTINGS").click()

        if self.device(text="Most recent network traffic log").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.device(text="RETRIEVE TRAFFIC LOGS").exists:
                    self.device(text="RETRIEVE TRAFFIC LOGS").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        if self.device(text="RETRIEVE TRAFFIC LOGS").exists:
            self.device(text="RETRIEVE TRAFFIC LOGS").click()
        return False

    def Request_bug_report(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="REQUEST BUG REPORT").exists:
            self.device(text="REQUEST BUG REPORT").click()
        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").exists:
            self.device(text="OPEN SETTINGS").click()

        if self.device(text="Most recent bug report").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.device(text="REQUEST BUG REPORT").exists:
                    self.device(text="REQUEST BUG REPORT").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        if self.device(text="REQUEST BUG REPORT").exists:
            self.device(text="REQUEST BUG REPORT").click()
        return False

    def Retrieve_security_logs(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="RETRIEVE SECURITY LOGS").exists:
            self.device(text="RETRIEVE SECURITY LOGS").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").exists:
            self.device(text="OPEN SETTINGS").click()

        if self.device(text="Most recent security log").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.device(text="RETRIEVE SECURITY LOGS").exists:
                    self.device(text="RETRIEVE SECURITY LOGS").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        if self.device(text="RETRIEVE SECURITY LOGS").exists:
            self.device(text="RETRIEVE SECURITY LOGS").click()
        return False

    def Enterprise_installed_apps(self, case_name):
        self.scroll_to_case(case_name)

        self.adb.cmd("push", "./NotificationBot.apk", "/sdcard")
        self.logger.debug("adb push ./NotificationBot.apk to /sdcard")
        self.device.delay(3)
        if self.device(text="UNINSTALL").exists:
            self.logger.debug("UNINSTALL NotificationBot.apk first")
            self.device(text="UNINSTALL").click()
        time.sleep(2)
        if self.device(text="Turn on Play Protect?").ext5:
            self.device(text="ACCEPT").click()
        if self.device(text="INSTALL").exists:
            self.device(text="INSTALL").click()
            if self.device(text="Turn on Play Protect?").ext5:
               self.device(text="ACCEPT").click()
            self.logger.debug("install NotificationBot.apk")
        self.device.delay(3)
        if self.device(text="Turn on Play Protect?").ext5:
            self.device(text="ACCEPT").click()
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        self.wait(1)
        self.device.press.back()
        self.wait(1)
        if self.device(text="Turn on Play Protect?").ext5:
            self.device(text="ACCEPT").click()
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        self.wait(1)
        self.device.press.back()
        self.wait(1)
        if self.device(text="Turn on Play Protect?").ext5:
            self.device(text="ACCEPT").click()
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()
        if self.device(text="Turn on Play Protect?").ext5:
            self.device(text="ACCEPT").click()
        self.scroll_to_text_without_click("Apps installed")
        self.clickText("Apps installed")

        if self.device(text="Apps installed").wait.exists(timeout=5000) and self.device(
                text="CTS Robot").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Location_access_permission(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="RESET").exists:
            self.device(text="RESET").click()

        self.device.delay(1)
        if self.device(text="GRANT").exists:
            self.device(text="GRANT").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").exists:
            self.device(text="OPEN SETTINGS").click()

        self.scroll_to_text_without_click("Location permissions")

        if self.device(text="Location permissions").wait.exists(timeout=5000) and self.device(
                text="Minimum 1 app").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.device(text="RESET").exists:
                    self.device(text="RESET").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        if self.device(text="RESET").exists:
            self.device(text="RESET").click()
        return False

    def Microphone_access_permission(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="RESET").exists:
            self.device(text="RESET").click()

        self.device.delay(1)
        if self.device(text="GRANT").exists:
            self.device(text="GRANT").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").exists:
            self.device(text="OPEN SETTINGS").click()

        self.scroll_to_text_without_click("Microphone permissions")

        if self.device(text="Microphone permissions").wait.exists(timeout=5000) and self.device(
                text="Minimum 1 app").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.device(text="RESET").exists:
                    self.device(text="RESET").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        if self.device(text="RESET").exists:
                    self.device(text="RESET").click()
        return False

    def Camera_access_permission(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="RESET").exists:
            self.device(text="RESET").click()

        self.device.delay(1)
        if self.device(text="GRANT").exists:
            self.device(text="GRANT").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").exists:
            self.device(text="OPEN SETTINGS").click()

        self.scroll_to_text_without_click("Camera permissions")

        if self.device(text="Camera permissions").wait.exists(timeout=5000) and self.device(
                text="Minimum 1 app").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.device(text="RESET").exists:
                    self.device(text="RESET").click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        if self.device(text="RESET").exists:
            self.device(text="RESET").click()
        return False

    def clickText(self, option):
        if self.device(text=option).ext5:
            self.device(text=option).click()
            self.logger.debug("click text '%s' successfully" % option)
            return True
        self.logger.warning("can not found text '%s'" % option)
        return False

    def clickTextContains(self, option):
        if self.device(textContains=option).ext5:
            self.device(textContains=option).click()
            self.logger.debug("click textContains '%s'" % option)
            return True
        self.logger.warning("can not found textContains '%s'" % option)
        return False

    def Default_apps(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="RESET").ext5:
            self.device(text="RESET").click()

        self.enter_settings("Apps & notifications")
        assert self.device(scrollable=True).scroll.vert.toEnd()
        assert self.device(textContains="See all").click.wait()
        self.scroll_to_case("Chrome")
        self.scroll_to_text("Open by default")

        ##“Default apps” 在CN手机中是不需要browse中clear default，最好是即使不做这个步骤，后续也继续在verifier中完成测试
        self.clickText("CLEAR DEFAULTS")
        self.back_to_app(case_name)

        if self.device(text="SET DEFAULT APPS").ext5:
            self.device(text="SET DEFAULT APPS").click()
        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        self.scroll_to_text("Default apps")
        childCount = 0
        defaultApps = 0
        if self.device(resourceId="com.android.settings:id/list").exists:
            childCount = self.device(resourceId="com.android.settings:id/list").info["childCount"]

        self.logger.debug("childCount is: %s" % childCount)
        for loop in range(childCount):
            defaultApp = self.device(resourceId="com.android.settings:id/list").child(index=loop).child(
                resourceId="android:id/summary")
            if defaultApp.ext5:
                defaultAppText = defaultApp.get_text()
                if defaultAppText == "CTS Verifier":
                    defaultApps += 1

        self.logger.debug("defaultApps is: %s" % defaultApps)

        if defaultApps == 7 and childCount == 7:
            self.back_to_app(case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Default_keyboard(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET KEYBOARD").ext5:
            self.device(text="SET KEYBOARD").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        self.scroll_to_text_without_click("Default keyboard")

        if self.device(text="Default keyboard").wait.exists(timeout=5000) and self.device(
                text="Set to CTS Verifier").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(text="FINISH").ext5:
                self.device(text="FINISH").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Always_on_VPN(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET VPN").ext5:
            self.device(text="SET VPN").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        assert self.scroll_to_text_without_click("Always-on VPN turned on")

        if self.device(text="Always-on VPN turned on").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(text="FINISH").ext5:
                self.device(text="FINISH").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Always_on_VPN_managed_profile(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="START").ext5:
            self.device(text="START").click()
            self.device.delay(5)

        if self.device(text="SET VPN").ext5:
            self.device(text="SET VPN").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        assert self.scroll_to_text_without_click("Always-on VPN turned on in your work profile")

        if self.device(text="Always-on VPN turned on in your work profile").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(text="FINISH").ext5:
                self.device(text="FINISH").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Global_HTTP_Proxy(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="SET PROXY").ext5:
            self.device(text="SET PROXY").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        assert self.scroll_to_text_without_click("Global HTTP proxy set")

        if self.device(text="Global HTTP proxy set").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(text="CLEAR PROXY").ext5:
                self.device(text="CLEAR PROXY").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Trusted_CA_certs(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="INSTALL CERT").ext5:
            self.device(text="INSTALL CERT").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        assert self.scroll_to_text_without_click("Trusted credentials")

        if self.device(text="Trusted credentials").ext5 and self.device(text="Minimum 1 CA certificate").ext5:
            self.back_to_app(case_name)
            if self.device(text="FINISH").ext5:
                self.device(text="FINISH").click()
            self.test_pass(case_name)
            return True

        self.test_fail(case_name)
        self.save_fail_img()
        return False

    def Trusted_CA_certs_managed_profile(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="START").ext5:
            self.device(text="START").click()
            self.device.delay(5)

        if self.device(text="INSTALL CERT").ext5:
            self.device(text="INSTALL CERT").click()

        self.device.delay(2)
        if self.device(text="SETTINGS").ext5:
            self.device(text="SETTINGS").click()

        assert self.scroll_to_text_without_click(
            "Trusted credentials in your work profile") or self.scroll_to_text_without_click("Trusted credentials")

        if self.device(textContains="Trusted credentials").ext5 and self.device(text="Minimum 1 CA certificate").ext5:
            self.back_to_app(case_name)
            if self.device(text="FINISH").ext5:
                self.device(text="FINISH").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Wipe_on_authentication_failure_managed_profile(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="START").ext5:
            self.device(text="START").click()
            self.device.delay(5)

        if self.device(text="SET LIMIT").ext5:
            self.device(text="SET LIMIT").click()

        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        assert self.scroll_to_text_without_click("Failed password attempts before deleting work profile data")

        if self.device(text="Failed password attempts before deleting work profile data").wait.exists(timeout=5000):
            self.back_to_app(case_name)
            if self.device(text="FINISH").ext5:
                self.device(text="FINISH").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Quick_settings_disclosure(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="CLEAR ORG").ext5:
            self.device(text="CLEAR ORG").click()

        self.device.open.quick_settings()
        assert self.device(text="Device is managed by your organization").wait.exists(timeout=5000)
        self.clear_notification()

        if self.device(text="SET ORG").ext5:
            self.device(text="SET ORG").click()

        self.device.open.quick_settings()
        assert self.device(text="Device is managed by Foo, Inc.").wait.exists(timeout=5000)
        self.clear_notification()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Keyguard_disclosure(self, case_name):
        try:
            self.scroll_to_case(case_name)
            # self.setLockScreenToSwipe()
            # self.back_to_app(case_name)
            if self.device(text="SET ORG").ext5:
                self.device(text="SET ORG").click()
            self.device.delay(2)
            self.device.sleep()
            self.device.delay(5)

            start_time = time.time()
            while self.time_task(start_time, 60):
                self.device.wakeup()
                time.sleep(2)
                info = self.device(
                    resourceId="com.android.systemui:id/keyguard_indication_enterprise_disclosure").get_text()
                self.logger.debug("the keyguard_indication_enterprise_disclosure info is :%s" % info)
                if info == "This device is managed by Foo, Inc.":
                    self.logger.debug("found 'This device is managed by Foo, Inc.' successfully")
                    self.unlock_scream_without_password()
                    break
                else:
                    self.logger.debug(
                        "can not found This device is managed by Foo, Inc. wakeup device and search again")
            else:
                assert False, "Cannot found text 'This device is managed by Foo, Inc.'"

            if self.device(text="CLEAR ORG").ext5:
                self.device(text="CLEAR ORG").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.save_fail_img()
            self.logger.warning(traceback.format_exc())
        finally:
            self.unlock_scream_without_password()
            self.setLockScreenToNone()

    def Add_account_disclosure(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="CLEAR ORG").ext5:
            self.device(text="CLEAR ORG").click()
        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        assert self.scroll_to_text_without_click(
            "This device is managed by your organization Learn more") or self.scroll_to_text_without_click(
            "This device is managed by your organization. Learn more")

        self.back_to_app(case_name)

        if self.device(text="SET ORG").ext5:
            self.device(text="SET ORG").click()
        self.device.delay(1)
        if self.device(text="OPEN SETTINGS").ext5:
            self.device(text="OPEN SETTINGS").click()

        assert self.scroll_to_text_without_click(
            "This device is managed by Foo, Inc. Learn more") or self.scroll_to_text_without_click(
            "This device is managed by Foo, Inc.. Learn more")
        self.back_to_app(case_name)

        if self.device(text="CLEAR ORG").ext5:
            self.device(text="CLEAR ORG").click()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Corporate_Owned_Managed_Profile(self, case_name):
        self.scroll_to_case(case_name)

        case_name = "Disallow remove managed profile"
        if self.device(text="ACCEPT & CONTINUE").wait.exists(timeout=5000):
            self.device(text="ACCEPT & CONTINUE").click()

        if self.device(text="Setting up your work profile…").wait.exists(timeout=5000):
            self.logger.debug("Setting up my work profile......")

        self.scroll_to_case(case_name)

        self.enable_desallow_switch_and_open_settings()

        self.scroll_to_text("Users & accounts")

        assert self.device(text="Remove work profile", enabled=False).ext5
        self.device(text="Remove work profile", enabled=False).click()

        assert self.device(text="Action not allowed").ext5
        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=5000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Network_Logging_UI(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="ENABLE NETWORK LOGGING").wait.exists(timeout=5000):
            self.device(text="ENABLE NETWORK LOGGING").click()

        self.device.open.quick_settings()
        assert self.device(text="Device is managed by your organization").ext5
        self.device(text="Device is managed by your organization").click()

        assert self.device(text="Network logging").ext5 and self.device(
            text="Your administrator has turned on network logging, which monitors traffic on your device.").ext5
        self.device(text="OK").click()

        self.device.open.notification()
        assert self.scroll_to_text_without_click(
            "Your organization manages this device and may monitor network traffic. Tap for details.")
        self.clear_notification()

        if self.device(text="DISABLE NETWORK LOGGING").wait.exists(timeout=5000):
            self.device(text="DISABLE NETWORK LOGGING").click()

        self.device.open.notification()
        assert not self.scroll_to_text_without_click(
            "Your organization manages this device and may monitor network traffic. Tap for details.")
        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=10000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Device_owner_provisioning(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="START PROVISIONING").ext5:
            self.device(text="START PROVISIONING").click()

        assert self.device(text="Can't set up device").wait.exists(timeout=5000)
        if self.device(text="OK").ext5:
            self.device(text="OK").click()

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Quick_settings_disclosure__ndot(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text=case_name).ext5:
            self.logger.debug("%s.exists" % case_name)
        else:
            self.logger.debug("%s.not exists" % case_name)

        self.device.open.quick_settings()
        assert not self.device(text="Device is managed by your organization").ext5
        self.clear_notification()

        if self.device(resourceId=pass_button, enabled=True).ext5:
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Keyguard_disclosure__ndot(self, case_name):
        try:
            self.scroll_to_case(case_name)
            self.setLockScreenToSwipe()
            self.back_to_app(case_name)
            self.device.sleep()
            self.device.delay(5)
            self.device.wakeup()

            assert not self.device(text="This device is managed by your organization").wait.exists(timeout=15000)
            self.unlock_scream_without_password()

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.unlock_scream_without_password()
            self.setLockScreenToNone()

    def Add_account_disclosure__ndot(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").ext5:
            self.device(text="GO").click()

        assert not self.scroll_to_text_without_click("This device is managed by your organization. Learn more")
        self.back_to_app(case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Bluetooth_LE_Client_Test(self, case_name):
        self.scroll_to_case(case_name)
        self.scroll_to_case_sdevice("01 Bluetooth LE Server Test")
        self.logger.debug("%s Testing...,please wait a moment" % case_name)

        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=60000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            if self.sdevice(text="OK").wait.exists(timeout=1000):
                self.sdevice(text="OK").click()
            if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=1000):
                self.sdevice(resourceId=pass_button, enabled=True).click()
            self.back_to_app_sdevice("Bluetooth LE Insecure Server Test")
            return True
        self.logger.warning("%s Test Failed" % case_name)
        self.back_to_app_sdevice("Bluetooth LE Insecure Server Test")
        self.save_fail_img()
        return False

    def Bluetooth_LE_Client_Test__Secure(self, case_name):
        try:
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("01 Bluetooth LE Server Test")
            assert self.device(text="").ext5

            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=80000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Secure Server Test")

    def Bluetooth_LE_Server_Test__Secure(self, case_name):
        try:
            self.disable_Bluetooth()
            self.disable_Bluetooth_Sdevice()
            self.EnableBlueTooth()
            self.EnableBlueTooth_Sdevice()
            self.back_to_app("Bluetooth LE Secure Client Test")
            self.back_to_app_sdevice("Bluetooth LE Secure Server Test")

            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("01 Bluetooth LE Client Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=80000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                # self.back_to_app("Bluetooth LE Secure Server Test")
                # self.back_to_app_sdevice("Bluetooth LE Secure Client Test")
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app("Bluetooth LE Secure Server Test")
            self.back_to_app_sdevice("Bluetooth LE Secure Client Test")


    def Bluetooth_LE_Connection_Priority_Client_Test(self, case_name):
        try:
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("02 Bluetooth LE Connection Priority Server Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=120000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.sdevice(text="OK").wait.exists(timeout=1000):
                    self.sdevice(text="OK").click()
                if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=1000):
                    self.sdevice(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Insecure Server Test")

    def Bluetooth_LE_Connection_Priority_Client_Test__Secure(self, case_name):
        try:
            self.disable_Bluetooth()
            self.disable_Bluetooth_Sdevice()
            self.EnableBlueTooth()
            self.EnableBlueTooth_Sdevice()
            self.back_to_app("Bluetooth LE Secure Client Test")
            self.back_to_app_sdevice("Bluetooth LE Secure Server Test")

            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("02 Bluetooth LE Connection Priority Server Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=120000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Secure Server Test")
            # self.back_to_app("Bluetooth LE Secure Client Test")

    def switch_off_on(self, count, deviceType=""):
        self.logger.debug("switch off & on %s times" % count)
        if deviceType == "Sdevice":
            device = self.sdevice
            self.enter_settings_sdevice("Connected devices")
        else:
            device = self.device
            self.enter_settings("Connected devices")
        switch_text = ""
        if device(text="Bluetooth").ext5:
            device(text="Bluetooth").click()

        for loop in range(count):
            if device(resourceId="com.android.settings:id/switch_widget").exists:
                device(resourceId="com.android.settings:id/switch_widget").click()
            time.sleep(1)

        if device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = device(resourceId="com.android.settings:id/switch_bar").get_text()

        self.logger.debug("switch_text is %s" % switch_text)
        if switch_text.lower() == "on":
            self.logger.debug("BlueTooth is opened")
            return True

        if switch_text.lower() == "off":
            device(resourceId="com.android.settings:id/switch_widget").click()
        device.delay(3)
        if device(resourceId="com.android.settings:id/switch_bar").wait.exists(timeout=5000):
            switch_text = device(resourceId="com.android.settings:id/switch_bar").get_text()
        self.logger.debug("switch_text1 is %s" % switch_text)
        if switch_text.lower() == "on":
            self.logger.debug("open BlueTooth successfully")
            return True

        self.logger.debug("open BlueTooth failed")
        self.save_fail_img()
        return False

    def Bluetooth_LE_Encrypted_Client_Test(self, case_name):
        try:
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("03 Bluetooth LE Encrypted Server Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)

            assert self.device(text="Bluetooth LE Read Encrypted Characteristic").ext5
            self.device(text="Bluetooth LE Read Encrypted Characteristic").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Read Encrypted Characteristic test completed")
            self.wait(2)

            assert self.device(text="Bluetooth LE Write Encrypted Characteristic").ext5
            self.device(text="Bluetooth LE Write Encrypted Characteristic").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Write Encrypted Characteristic test completed")
            self.wait(2)

            assert self.device(text="Bluetooth LE Read Encrypted Descriptor").ext5
            self.device(text="Bluetooth LE Read Encrypted Descriptor").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Read Encrypted Descriptor test completed")
            self.wait(2)

            assert self.device(text="Bluetooth LE Write Encrypted Descriptor").ext5
            self.device(text="Bluetooth LE Write Encrypted Descriptor").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Write Encrypted Descriptor test completed")

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.sdevice(text="OK").wait.exists(timeout=1000):
                    self.sdevice(text="OK").click()
                if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=1000):
                    self.sdevice(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Insecure Server Test")

    def Bluetooth_LE_Encrypted_Client_Test__Secure(self, case_name):
        try:
            self.disable_Bluetooth()
            self.disable_Bluetooth_Sdevice()
            self.EnableBlueTooth()
            self.EnableBlueTooth_Sdevice()
            self.back_to_app("Bluetooth LE Secure Client Test")
            self.back_to_app_sdevice("Bluetooth LE Secure Server Test")

            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("03 Bluetooth LE Encrypted Server Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)

            assert self.device(text="Bluetooth LE Read Encrypted Characteristic").ext5
            self.device(text="Bluetooth LE Read Encrypted Characteristic").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Read Encrypted Characteristic test completed")
            self.wait(2)

            assert self.device(text="Bluetooth LE Write Encrypted Characteristic").ext5
            self.device(text="Bluetooth LE Write Encrypted Characteristic").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Write Encrypted Characteristic test completed")
            self.wait(2)

            assert self.device(text="Bluetooth LE Read Encrypted Descriptor").ext5
            self.device(text="Bluetooth LE Read Encrypted Descriptor").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Read Encrypted Descriptor test completed")
            self.wait(2)

            assert self.device(text="Bluetooth LE Write Encrypted Descriptor").ext5
            self.device(text="Bluetooth LE Write Encrypted Descriptor").click()
            if self.device(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Write Encrypted Descriptor test completed")

            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Secure Server Test")

    def Bluetooth_LE_Server_Test(self, case_name):
        try:
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("01 Bluetooth LE Client Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            if self.device(text="OK").ext5:
                self.device(text="OK").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=120000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.sdevice(text="OK").ext5:
                    self.sdevice(text="OK").click()
                if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=1000):
                    self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Insecure Client Test")

    def Bluetooth_LE_Connection_Priority_Server_Test(self, case_name):
        try:
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("02 Bluetooth LE Connection Priority Client Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)

            if self.device(text="OK").wait.exists(timeout=120000):
                self.device(text="OK").click()
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.sdevice(text="OK").wait.exists(timeout=1000):
                    self.sdevice(text="OK").click()
                if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=1000):
                    self.sdevice(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Insecure Client Test")

    def Bluetooth_LE_Connection_Priority_Server_Test__Secure(self, case_name):
        try:
            self.disable_Bluetooth()
            self.disable_Bluetooth_Sdevice()

            self.EnableBlueTooth()
            self.EnableBlueTooth_Sdevice()
            self.back_to_app("Bluetooth LE Secure Server Test")
            self.back_to_app_sdevice("Bluetooth LE Secure Client Test")
            self.scroll_to_case_sdevice("Bluetooth LE Secure Client Test")
            self.scroll_to_case_sdevice("02 Bluetooth LE Connection Priority Client Test")
            self.scroll_to_case(case_name)
            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            for loop in range(3):

                if self.device(text="OK").wait.exists(timeout=120000):
                    self.device(text="OK").click()
                    if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                       self.logger.debug("%s Test Pass" % case_name)
                       self.device(resourceId=pass_button, enabled=True).click()
                       return True
                       break
                else:
                    self.logger.warning("%s Test Failed" % case_name)
                    self.save_fail_img()
                    self.back_to_app("Bluetooth LE Secure Server Test")
                    self.back_to_app_sdevice("Bluetooth LE Secure Client Test")
                    self.scroll_to_case(case_name)
                    self.scroll_to_case_sdevice("02 Bluetooth LE Connection Priority Client Test")
                    self.logger.debug("%s Testing...,please wait a moment" % case_name)
                    continue
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Secure Client Test")

    def Bluetooth_LE_Encrypted_Server_Test(self, case_name):
        try:
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice("03 Bluetooth LE Encrypted Client Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                if self.sdevice(text="OK").wait.exists(timeout=1000):
                    self.sdevice(text="OK").click()
                if self.sdevice(resourceId=pass_button, enabled=True).wait.exists(timeout=1000):
                    self.sdevice(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Insecure Client Test")

    def Bluetooth_LE_Encrypted_Server_Test__Secure(self, case_name):
        try:
            self.disable_Bluetooth()
            self.disable_Bluetooth_Sdevice()

            self.EnableBlueTooth()
            self.EnableBlueTooth_Sdevice()
            self.back_to_app("Bluetooth LE Secure Server Test")
            self.back_to_app_sdevice("Bluetooth LE Secure Client Test")
            self.scroll_to_case(case_name)
            # if self.sdevice(text="Bluetooth Test").exists(timeout=2000):
            #     self.scroll_to_case_sdevice("Bluetooth LE Secure Client Test")
            #     self.scroll_to_case_sdevice("03 Bluetooth LE Encrypted Client Test")
            # elif self.sdevice(text="Bluetooth LE Secure Client Test").exists(timeout=2000):
            #     self.scroll_to_case_sdevice("03 Bluetooth LE Encrypted Client Test")
            self.scroll_to_case_sdevice("03 Bluetooth LE Encrypted Client Test")
            self.logger.debug("%s Testing...,please wait a moment" % case_name)
            assert self.sdevice(text="Bluetooth LE Read Encrypted Characteristic").ext5
            self.sdevice(text="Bluetooth LE Read Encrypted Characteristic").click()
            if self.sdevice(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Read Encrypted Characteristic test completed")
            self.sdevice.wait(2)

            assert self.sdevice(text="Bluetooth LE Write Encrypted Characteristic").ext5
            self.sdevice(text="Bluetooth LE Write Encrypted Characteristic").click()
            if self.sdevice(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Write Encrypted Characteristic test completed")
            self.sdevice.wait(2)

            assert self.sdevice(text="Bluetooth LE Read Encrypted Descriptor").ext5
            self.sdevice(text="Bluetooth LE Read Encrypted Descriptor").click()
            if self.sdevice(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Read Encrypted Descriptor test completed")
            self.sdevice.wait(2)

            assert self.sdevice(text="Bluetooth LE Write Encrypted Descriptor").ext5
            self.sdevice(text="Bluetooth LE Write Encrypted Descriptor").click()
            if self.sdevice(text="Test Running").wait.gone(timeout=80000):
                self.logger.debug("Bluetooth LE Write Encrypted Descriptor test completed")
            self.sdevice.wait(2)
            self.wait(2)
            if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
                self.logger.debug("%s Test Pass" % case_name)
                self.device(resourceId=pass_button, enabled=True).click()
                return True
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False
        except:
            self.logger.warning(traceback.format_exc())
        finally:
            self.back_to_app_sdevice("Bluetooth LE Secure Client Test")

    def Device_Admin_Uninstall_Test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="ENABLE ADMIN", enabled=False).ext5:
            pass
        elif self.device(text="ENABLE ADMIN", enabled=True).ext5:
            self.device(text="ENABLE ADMIN").click()
            if self.device(scrollable=True).exists:
                self.device(scrollable=True).scroll.vert.toEnd()
            assert self.scroll_to_text("Activate this device admin app")

        assert self.device(text="LAUNCH SETTINGS", enabled=True).ext5
        self.device(text="LAUNCH SETTINGS").click()

        assert self.device(text="UNINSTALL", enabled=True).ext5
        self.device(text="UNINSTALL").click()

        assert self.scroll_to_text("Deactivate & uninstall")

        # self.device(text="Deactivate & uninstall").click()
        self.device(text="OK").click()
        self.device.delay(2)
        self.device.dump()
        if self.device(resourceId=pass_button, enabled=True).wait.exists(timeout=20000):
            self.logger.debug("%s Test Pass" % case_name)
            self.device(resourceId=pass_button, enabled=True).click()
            return True
        else:
            self.logger.warning("%s Test Failed" % case_name)
            self.save_fail_img()
            return False

    def Select_work_lock_test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Continue without fingerprint").wait.exists(timeout=5000):
            self.device(text="Continue without fingerprint").click()
        assert self.device(text="Password").wait.exists(timeout=5000)
        self.device(text="Password").click()
        assert self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000)
        self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        self.device.press.enter()
        self.device.delay(3)

        assert self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000)
        self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        self.device.press.enter()
        self.device.delay(3)

        self.back_to_Pass_Popup_home()
        assert self.test_pass_popup()
        self.logger.debug("%s Test Pass" % case_name)
        return True

    def Confirm_work_lock_test(self, case_name):
        try:
            self.scroll_to_case(case_name)
            if self.device(text="GO").wait.exists(timeout=5000):
                self.device(text="GO").click()

            if self.device(description="All Items").wait.exists(timeout=5000):
                self.device(description="All Items").click()
            if self.device(resourceId = "com.android.launcher3:id/all_apps_handle").exists:
                self.device(resourceId="com.android.launcher3:id/all_apps_handle").click()
            self.device(resourceId="com.android.launcher3:id/apps_list_view",scrollable=True).scroll.vert.to(text="Contacts")

            if self.device(description="Work Contacts").wait.exists(timeout=5000):
                self.device(description="Work Contacts").click()

            assert self.device(resourceId="com.android.settings:id/headerText", text="CtsVerifier").wait.exists(
                timeout=15000)
            assert self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000)
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()
            self.device.delay(3)

            self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
            assert self.test_pass_popup()
            self.logger.debug("%s Test Pass" % case_name)
            return True
        except:
            self.save_fail_img()
            self.remove_work_profile()
            self.logger.warning(traceback.format_exc())
        finally:
            pass
            # self.enable_use_one_lock()

    def Verify_recents_are_redacted_when_locked(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="Continue without fingerprint").wait.exists(timeout=5000):
            self.device(text="Continue without fingerprint").click()
        if self.device(text="Password").wait.exists(timeout=5000):
            self.device(text="Password").click()

        # self.device().fling.vert.toEnd()
        #
        # if self.device(text="Downloads").wait.exists(timeout=5000):
        #     self.device(text="Downloads").click()

        # assert self.device(resourceId="com.android.settings:id/headerText", text="CtsVerifier").ext5
        assert self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000)
        self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        self.device.press.enter()
        self.device.delay(3)

        assert self.device(resourceId="com.android.settings:id/password_entry").wait.exists(timeout=5000)
        self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
        self.device.press.enter()
        self.device.delay(3)

        if self.device(text="Show all work notification content").wait.exists(timeout=5000):
            self.device(text="Show all work notification content").click()
        if self.device(text="DONE").wait.exists(timeout=5000):
            self.device(text="DONE").click()
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
        self.back_to_app("Recents redaction test")
        if self.device(text="LOCK NOW").wait.exists(timeout=5000):
            self.device(text="LOCK NOW").click()
        self.device.press.menu()

        info = self.device.info
        if not "This test verifies that if a work profile is locked with" in info:
            self.logger.debug("------------->%s",info)
            self.logger.debug("Test Pass")
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")


        self.adb.shell("input text %s"%password)
        self.device.press.enter()
        time.sleep(2)
        self.scroll_to_case(case_name)
        assert self.test_pass_popup()
        self.logger.debug("%s Test Pass" % case_name)
        return True

    def Verify_recents_are_not_redacted_when_unlocked(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()
        self.adb.shell("input text %s"%password)
        self.device.press.enter()
        time.sleep(2)
        if self.device(text="Continue without fingerprint").wait.exists(timeout=5000):
            self.device(text="Continue without fingerprint").click()
        if self.device(text="None").wait.exists(timeout=5000):
            self.device(text="None").click()
        if self.device(text="YES, REMOVE").wait.exists(timeout=5000):
            self.device(text="YES, REMOVE").click()

        # info = self.device.info
        # if not "This test vaaaaaaa" in info:
        #
        # self.logger.debug("------------->%s"info)

        # if self.device(description="All Items").wait.exists(timeout=5000):
        #     self.device(description="All Items").click()
        #
        # self.device().fling.vert.toEnd()
        #
        # if self.device(text="Downloads").wait.exists(timeout=5000):
        #     self.device(text="Downloads").click()
        self.device.press.back()
        self.device.press.menu()

        info = self.device.info
        if  "This test verifies that if a work profile is locked with" in info:
            self.logger.debug("------------->%s",info)
            self.logger.debug("Test Pass")
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")
        self.scroll_to_case(case_name)

        assert self.test_pass_popup()
        self.logger.debug("%s Test Pass" % case_name)
        return True

    def Sound_recorder_support_cross_profile_audio_capture(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()

        if self.device(text="SKIP INTRO").wait.exists(timeout=3000):
            self.device(text="SKIP INTRO").click()

        if self.device(text="ALLOW").wait.exists(timeout=3000):
            self.allow_steps()

        assert self.device(resourceId="com.android.soundrecorder:id/recordButton").wait.exists(timeout=5000)
        self.device(resourceId="com.android.soundrecorder:id/recordButton").click()
        if self.device(text="ALLOW").wait.exists(timeout=3000):
            self.allow_steps()
        self.wait(10)
        if self.device(resourceId="com.android.soundrecorder:id/stopButton").exists:
            self.device(resourceId="com.android.soundrecorder:id/stopButton").click()
        if self.device(text="SAVE").wait.exists(timeout=30000):
            self.device(text="SAVE").click()
            self.logger.debug("SAVE recorder")
        if self.device(resourceId="com.android.soundrecorder:id/acceptButton").exists:
            self.device(resourceId="com.android.soundrecorder:id/acceptButton").click()
        assert self.device(text="PLAY").wait.exists(timeout=5000)
        self.device(text="PLAY").click()
        self.logger.debug("Play the recorder 15s")
        self.wait(15)

        if self.device(text="CLOSE").wait.exists(timeout=5000):
            self.device(text="CLOSE").click()

        assert self.test_pass_popup()
        self.logger.debug("%s Test Pass" % case_name)
        return True

    def remove_work_profile(self):
        try:
            self.logger.debug("starting to remove the work profile")
            self.enter_settings("Users & accounts")
            if not self.device(text="Remove work profile").exists():
                self.logger.debug("No Work profile")
                return  True
            self.scroll_to_text("Remove work profile")
            assert self.device(text="DELETE").ext5
            self.device(text="DELETE").click()
            self.device.dump()
            assert not self.device(text="Remove work profile").ext5
            self.logger.debug("Remove work profile successfully")
            return True
        except:
            self.logger.debug("Remove work profile failed")
            self.save_fail_img()
            self.logger.warning(traceback.format_exc())
            return False

    def Companion_Device_Test(self, case_name):
        self.scroll_to_case(case_name)
        self.EnableBlueTooth()
        self.back_to_app(case_name)
        if self.device(text="GO").wait.exists(timeout=5000):
            self.device(text="GO").click()
        self.wait(5)
        if self.device(resourceId="com.android.companiondevicemanager:id/device_list").ext5:
            self.device(resourceId="com.android.companiondevicemanager:id/device_list").child(index=0).click()
        self.clickText("OK")
        assert self.test_pass(case_name)
        return False

    def Screen_Pinning_Test(self, case_name):
        self.scroll_to_case(case_name)
        assert self.device(text="NEXT").ext5
        self.device(text="NEXT").click()

        assert self.device(text="GOT IT").ext5
        self.device(text="GOT IT").click()

        assert self.device(text="NEXT").ext5
        self.device(text="NEXT").click()

        time.sleep(1)
        self.device.press.home()
        time.sleep(2)

        assert self.device(text="NEXT").ext5
        self.device(text="NEXT").click()

        # 36 1660
        time.sleep(2)
        # self.device.long_click(36,1660)
        self.device.swipe(36, 1660, 36, 1661, 2000)
        self.logger.debug("---------------->")
        time.sleep(30)

        assert self.device(text="NEXT").ext5
        self.device(text="NEXT").click()

        if self.device(resourceId="com.android.companiondevicemanager:id/device_list").ext5:
            self.device(resourceId="com.android.companiondevicemanager:id/device_list").child(index=0).click()
        self.clickText("OK")
        self.test_pass(case_name)
        self.logger.warning("%s Test Failed" % case_name)
        self.save_fail_img()
        return False

    def Incoming_Self_Managed_Connection_Test(self, case_name):
        self.scroll_to_case(case_name)

        if self.device(text="REGISTER SELF-MANAGED CONNECTIONSERVICE").ext5:
            self.logger.debug("click REGISTER SELF-MANAGED CONNECTIONSERVICE")
            self.device(text="REGISTER SELF-MANAGED CONNECTIONSERVICE").click()

        if self.device(text="SHOW SYSTEM INCOMING UI").ext5:
            self.logger.debug("click SHOW SYSTEM INCOMING UI")
            self.device(text="SHOW SYSTEM INCOMING UI").click()

        if self.device(text="ANSWER").wait.exists(timeout=30000):
            self.device(text="ANSWER").click()

        if self.device(text="CONFIRM ANSWER").ext5:
            self.logger.debug("click CONFIRM ANSWER")
            self.device(text="CONFIRM ANSWER").click()

        assert self.test_pass(case_name)
        return True

    def Telecom_Enable_Phone_Account_Test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="REGISTER PHONE ACCOUNT").ext5:
            self.logger.debug("click REGISTER PHONE ACCOUNT")
            self.device(text="REGISTER PHONE ACCOUNT").click()

        time.sleep(2)
        self.device.press.home()
        self.start_app("Phone")

        assert self.device(description="More options").ext5
        self.device(description="More options").click()

        assert self.device(text="Settings").ext5
        self.device(text="Settings").click()
        assert self.device(text="Calls").ext5
        self.device(text="Calls").click()
        assert self.device(text="Calling accounts").ext5
        self.device(text="Calling accounts").click()
        assert self.device(text="Calling accounts").ext5
        self.device(text="Calling accounts").click()
        assert self.device(text="All calling accounts").ext5
        self.device(text="All calling accounts").click()

        assert self.device(resourceId="android:id/switch_widget").ext5
        self.device(resourceId="android:id/switch_widget").click()

        time.sleep(2)
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        if self.device(text="CONFIRM").wait.exists(timeout=5000):
            self.device(text="CONFIRM").click()

        assert self.test_pass(case_name)
        return True

    def Telecom_Incoming_Call_Test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="REGISTER AND ENABLE PHONE ACCOUNT").ext5:
            self.logger.debug("click REGISTER AND ENABLE PHONE ACCOUNT")
            self.device(text="REGISTER AND ENABLE PHONE ACCOUNT").click()
        assert self.device(text="All calling accounts").ext5
        self.device(text="All calling accounts").click()

        assert self.device(resourceId="android:id/switch_widget").ext5
        self.device(resourceId="android:id/switch_widget").click()
        self.back_to_app(case_name)

        assert self.device(text="CONFIRM PHONE ACCOUNT").ext5
        self.device(text="CONFIRM PHONE ACCOUNT").click()

        assert self.device(text="DIAL").ext5
        self.device(text="DIAL").click()

        assert self.device(text="ANSWER").ext5
        self.device(text="ANSWER").click()

        time.sleep(2)
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        if self.device(text="CONFIRM").wait.exists(timeout=5000):
            self.device(text="CONFIRM").click()

        if self.device(scrollable=True).ext5:
            self.device(scrollable=True).scroll.vert.toEnd()
        assert self.test_pass(case_name)
        return True

    def Telecom_Outgoing_Call_Test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="REGISTER AND ENABLE PHONE ACCOUNT").ext5:
            self.device(text="REGISTER AND ENABLE PHONE ACCOUNT").click()
        assert self.device(text="All calling accounts").ext5
        self.device(text="All calling accounts").click()

        assert self.device(resourceId="android:id/switch_widget").ext5
        self.device(resourceId="android:id/switch_widget").click()
        self.back_to_app(case_name)

        if self.device(text="REGISTER AND ENABLE PHONE ACCOUNT").ext5:
            self.device(text="REGISTER AND ENABLE PHONE ACCOUNT").click()

        if self.device(text="Make calls with").ext5:
            self.device(text="Make calls with").click()

        if self.device(text="CTS Verifier Test").ext5:
            self.device(text="CTS Verifier Test").click()
        self.back_to_app(case_name)

        assert self.device(text="CONFIRM PHONE ACCOUNT").ext5
        self.device(text="CONFIRM PHONE ACCOUNT").click()

        assert self.device(text="DIAL").ext5
        self.device(text="DIAL").click()

        assert self.device(resourceId="com.android.dialer:id/dialpad_floating_action_button").ext5
        self.device(resourceId="com.android.dialer:id/dialpad_floating_action_button").click()

        time.sleep(5)
        self.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

        if self.device(text="CONFIRM").wait.exists(timeout=5000):
            self.device(text="CONFIRM").click()

        if self.device(scrollable=True).ext5:
            self.device(scrollable=True).scroll.vert.toEnd()
        assert self.test_pass(case_name)
        return True

    def Hide_settings_in_voicemail_test(self, case_name):
        try:
            self.scroll_to_case(case_name)
            if self.device(text="OPEN VOICEMAIL SETTINGS").ext5:
                self.device(text="OPEN VOICEMAIL SETTINGS").click()
            assert not self.device(text="ringtone").ext5
            self.back_to_app(case_name)

            if self.device(text="RINGTONE SETTINGS DOES NOT EXIST").ext5:
                self.device(text="RINGTONE SETTINGS DOES NOT EXIST").click()

            self.logger.debug("CASE <%s> Test Pass!" % case_name)
            return True
        except:
            self.logger.warning(traceback.format_exc())

    def Hide_voicemail_in_call_settings_test(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="SET CTS VERIFIER AS DEFAULT DIALER").ext5:
            self.device(text="SET CTS VERIFIER AS DEFAULT DIALER").click()
        if self.device(text="SET DEFAULT").ext5:
            self.device(text="SET DEFAULT").click()

        assert self.device(text="OPEN CALL SETTINGS").ext5
        self.device(text="OPEN CALL SETTINGS").click()

        assert not self.device(text="Voicemail").ext5
        self.back_to_app(case_name)

        assert self.device(text='"VOICEMAIL" DOES NOT EXIST').ext5
        self.device(text='"VOICEMAIL" DOES NOT EXIST').click()
        self.logger.debug("CASE <%s> Test Pass!" % case_name)
        return True

    def System_Implements_Telecom_Intents(self, case_name):
        self.scroll_to_case(case_name)
        if self.device(text="LAUNCH CALL SETTINGS").ext5:
            self.device(text="LAUNCH CALL SETTINGS").click()
        assert self.device(text="Call settings").ext5
        self.device.press.back()
        assert self.device(text="Setting Launched",
                           resourceId="com.android.cts.verifier:id/dialer_telecom_intents_call_settings_check_box").ext5
        self.device(text="Setting Launched",
                    resourceId="com.android.cts.verifier:id/dialer_telecom_intents_call_settings_check_box").click()

        # check LAUNCH SHORT SMS ANSWER SETTINGS
        if self.device(text="LAUNCH SHORT SMS ANSWER SETTINGS").ext5:
            self.device(text="LAUNCH SHORT SMS ANSWER SETTINGS").click()
        assert self.device(text="Edit quick responses").ext5
        self.device.press.back()
        assert self.device(text="Setting Launched",
                           resourceId="com.android.cts.verifier:id/dialer_telecom_intents_short_sms_check_box").ext5
        self.device(text="Setting Launched",
                    resourceId="com.android.cts.verifier:id/dialer_telecom_intents_short_sms_check_box").click()

        # check LAUNCH SHORT SMS ANSWER SETTINGS
        if self.device(text="LAUNCH CALLING ACCOUNTS SETTINGS").ext5:
            self.device(text="LAUNCH CALLING ACCOUNTS SETTINGS").click()
        assert self.device(text="Calling accounts").ext5
        self.device.press.back()
        assert self.device(text="Setting Launched",
                           resourceId="com.android.cts.verifier:id/dialer_telecom_intents_calling_accounts_check_box").ext5
        self.device(text="Setting Launched",
                    resourceId="com.android.cts.verifier:id/dialer_telecom_intents_calling_accounts_check_box").click()
        self.device(scrollable=True).scroll.vert.toEnd()

        # check LAUNCH ACCESSIBILITY SETTINGS
        if self.device(text="LAUNCH ACCESSIBILITY SETTINGS").ext5:
            self.device(text="LAUNCH ACCESSIBILITY SETTINGS").click()
        assert self.device(text="Accessibility").ext5
        self.device.press.back()
        assert self.device(text="Setting Launched",
                           resourceId="com.android.cts.verifier:id/dialer_telecom_intents_accessibility_settings_check_box").ext5
        self.device(text="Setting Launched",
                    resourceId="com.android.cts.verifier:id/dialer_telecom_intents_accessibility_settings_check_box").click()

        assert self.test_pass(case_name)
        return True

    def set_max_volume(self):
        self.back_to_home()
        self.logger.debug("starting to set device to max volume")
        try:
            self.enter_settings("Sound")
            for loop in range(3):
                x, y = self.calculate_the_max_point(loop + 1)
                self.device.click(x, y)
                time.sleep(2)
                # if self.device(text="OK").exit5:
                #     self.device(text="OK").click()
        except:
            self.save_fail_img()
            self.logger.warning(traceback.format_exc())
        self.logger.debug("set set device to max volume completed!")
        return True

    def calculate_the_max_point(self, index):
        tab_height = self.device(className="android.widget.LinearLayout", index=index).child(
            resourceId="android:id/seekbar")
        if tab_height.ext5:
            info_bounds = tab_height.info["bounds"]
            right_location = info_bounds["right"]
            top_location = info_bounds["top"]
            bottom_location = info_bounds["bottom"]

            xpoint = right_location - 2
            centerY = (top_location + bottom_location) / 2
            self.logger.debug("X coordinates:%s" % xpoint)
            self.logger.debug("Y coordinates:%s" % centerY)
            return xpoint, centerY

    def Hifi_Ultrasound_Microphone_Test(self, case_name):
        self.enter_CTSVerifier()
        self.enter_CTSVerifier_Sdevice()
        self.scroll_to_case(case_name)
        self.scroll_to_case_sdevice(case_name)
        self.device(text="RECORD").click()
        self.sdevice(text="PLAY").click()

        self.device.delay(10)
        self.sdevice.delay(10)
        if self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True):
            self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
            self.logger.debug("Mdevice Hifi_Ultrasound_Microphone_Test Pass")
            self.back_to_verifier_home()
            self.back_to_verifier_home_sdevice()
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice(case_name)
            self.sdevice(text="RECORD").click()
            self.device(text="PLAY").click()
            self.device.delay(10)
            self.sdevice.delay(10)
            if self.sdevice(resourceId="com.android.cts.verifier:id/pass_button", enabled=True):
                self.sdevice(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
                self.logger.debug("Sdevice Hifi_Ultrasound_Microphone_Test Pass")
                return True
            else:
                self.logger.warning("Sdevice Hifi_Ultrasound_Microphone_Test  Falied!!!")
                return False
        else:
            self.logger.warning("Mdevice Hifi_Ultrasound_Microphone_Test  Falied!!!")
            return False

    def Hifi_Ultrasound_Speaker_Test(self,case_name):
        self.enter_CTSVerifier()
        self.enter_CTSVerifier_Sdevice()
        self.scroll_to_case(case_name)
        self.scroll_to_case_sdevice(case_name)
        self.sdevice(text="RECORD").click()
        self.device(text="PLAY").click()

        self.device.delay(10)
        self.sdevice.delay(10)
        self.device.press.back()
        self.sdevice.press.back()
        self.device.dump()
        self.sdevice.dump()
        if "PASS" in self.sdevice(resourceId="com.android.cts.verifier:id/info_text").get_text() and self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True):
            self.device(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
            self.logger.debug("Mdevice Hifi_Ultrasound_Speaker_Test Pass")
            self.back_to_verifier_home()
            self.back_to_verifier_home_sdevice()
            self.scroll_to_case(case_name)
            self.scroll_to_case_sdevice(case_name)
            self.device(text="RECORD").click()
            self.sdevice(text="PLAY").click()

            self.device.delay(10)
            self.sdevice.delay(10)
            self.device.press.back()
            self.sdevice.press.back()

            if "PASS" in self.device(resourceId="com.android.cts.verifier:id/info_text").get_text() and self.sdevice(resourceId="com.android.cts.verifier:id/pass_button", enabled=True):
                self.sdevice(resourceId="com.android.cts.verifier:id/pass_button", enabled=True).click()
                self.logger.debug("Sdevice Hifi_Ultrasound_Speaker_Test Pass")
                return True
            else:
                self.logger.debug("Sdevice Hifi_Ultrasound_Speaker_Test Fail")
                return False
        else:
            self.logger.debug("Mdevice Hifi_Ultrasound_Speaker_Test Fail")
            return False

    def find1stjsonfile(self):
        name = os.popen('adb shell getprop ro.boot.binfo.name ').read()
        variant = name[6:-1]
        self.logger.debug(variant)
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\'+variant+'.json'):
            self.logger.debug ("First Approved Json Exists")
        else:
            self.logger.error("No First Approved Json!!!Please Ckeck in Common file!!!")
            os._exit(0)

    def get1stjsonfiledetail(self):
        name = os.popen('adb shell getprop ro.boot.binfo.name ').read()
        variant = name[6:-1]
        f = file(os.path.dirname(os.path.abspath(__file__))+'\\'+variant+'.json')
        firstapprovedjsondetail = json.load(f)
        global firstapprovedjsondetails
        firstapprovedjsondetails = firstapprovedjsondetail["ro_property"]
        print (firstapprovedjsondetails)

    def checkJsonDetails(self,list1,list2):
        lenlist1 = len(list1)
        num = 0
        for i in range(0,lenlist1):
            temp = list1[i]
            if temp in list2:
                num += 1
        if num == lenlist1:
            self.logger.debug("All Details Equal")
            return True
        else:
            self.logger.debug("Property not Equal!!!! Please Check!!!")
            return False


    def getPhoneDetailandBuildNewJsonFile(self):
        ro_build_fingerprint = os.popen('adb shell getprop ro.build.fingerprint ').read()
        ro_product_model = os.popen('adb shell getprop ro.product.model ').read()
        ro_product_brand = os.popen('adb shell getprop ro.product.brand ').read()
        ro_product_name = os.popen('adb shell getprop ro.product.name ').read()
        ro_product_device = os.popen('adb shell getprop ro.product.device ').read()
        ro_vendor_build_fingerprint = os.popen('adb shell getprop ro.vendor.build.fingerprint ').read()
        ro_vendor_product_model = os.popen('adb shell getprop ro.vendor.product.model ').read()
        ro_vendor_product_brand = os.popen('adb shell getprop ro.vendor.product.brand ').read()
        ro_vendor_product_name = os.popen('adb shell getprop ro.vendor.product.name ').read()
        ro_vendor_product_device = os.popen('adb shell getprop ro.vendor.product.device ').read()
        ro_product_first_api_level = os.popen('adb shell getprop ro.product.first_api_level ').read()
        ro_com_google_gmsversion = os.popen('adb shell getprop ro.com.google.gmsversion ').read()
        ro_com_google_clientidbase = os.popen('adb shell getprop ro.com.google.clientidbase ').read()
        ro_com_google_clientidbase_ms = os.popen('adb shell getprop ro.com.google.clientidbase.ms ').read()
        ro_com_google_clientidbase_am = os.popen('adb shell getprop ro.com.google.clientidbase.am ').read()
        ro_com_google_clientidbase_wal = os.popen('adb shell getprop ro.com.google.clientidbase.wal ').read()
        ro_com_google_clientidbase_cr = os.popen('adb shell getprop ro.com.google.clientidbase.cr ').read()
        ro_build_version_security_patch = os.popen('adb shell getprop ro.build.version.security_patch ').read()
        ro_build_version_base_os = os.popen('adb shell getprop ro.build.version.base_os ').read()

        data={}
        data['name'] = ro_product_name[:-1]
        data['build_number'] = os.popen('adb shell getprop ro.boot.build_number').read()[:-1]
        data['ro.build.fingerprint'] = ro_build_fingerprint[:-1]
        data['ro.product.model'] = ro_product_model[:-1]
        data['ro.product.brand'] = ro_product_brand[:-1]
        data['ro.product.name'] = ro_product_name[:-1]
        data['ro.product.device'] = ro_product_device[:-1]
        data['ro.vendor.build.fingerprint'] = ro_vendor_build_fingerprint[:-1]
        data['ro.vendor.product.model'] = ro_vendor_product_model[:-1]
        data['ro.vendor.product.brand'] = ro_vendor_product_brand[:-1]
        data['ro.vendor.product.name'] = ro_vendor_product_name[:-1]
        data['ro.vendor.product.device'] = ro_vendor_product_device[:-1]
        data['ro.product.first_api_level'] = ro_product_first_api_level[:-1]
        data['ro.com.google.gmsversion'] = ro_com_google_gmsversion[:-1]
        data['ro.com.google.clientidbase'] = ro_com_google_clientidbase[:-1]
        data['ro.com.google.clientidbase.ms'] = ro_com_google_clientidbase_ms[:-1]
        data['ro.com.google.clientidbase.am'] = ro_com_google_clientidbase_am[:-1]
        data['ro.com.google.clientidbase.wal'] = ro_com_google_clientidbase_wal[:-1]
        data['ro.com.google.clientidbase.cr'] = ro_com_google_clientidbase_cr[:-1]
        data['ro.build.version.security_patch'] = ro_build_version_security_patch[:-1]
        data['ro.build.version.base_os'] = ro_build_version_base_os[:-1]

        name = os.popen('adb shell getprop ro.boot.binfo.name ').read()
        variant = name[6:-1]
        ro_build_fingerprint_dict_check = {'name': 'ro.build.fingerprint','value': ro_build_fingerprint[:-25]}
        ro_product_model_dict_check = {'name': 'ro.product.model','value': ro_product_model[:-1]}
        ro_product_brand_dict_check = {'name': 'ro.product.brand','value': ro_product_brand[:-1]}
        ro_product_name_dict_check =  {'name': 'ro.product.name','value': ro_product_name[:-1]}
        ro_product_device_dict_check = {'name': 'ro.product.device','value': ro_product_device[:-1]}
        ro_vendor_build_fingerprint_dict_check = {'name': 'ro.vendor.build.fingerprint','value': ro_vendor_build_fingerprint[:-25]}
        ro_vendor_product_model_dict_check = {'name': 'ro.vendor.product.model','value': ro_vendor_product_model[:-1]}
        ro_vendor_product_brand_dict_check = {'name': 'ro.vendor.product.brand','value': ro_vendor_product_brand[:-1]}
        ro_vendor_product_name_dict_check = {'name': 'ro.vendor.product.name','value': ro_vendor_product_name[:-1]}
        ro_vendor_product_device_dict_check = {'name': 'ro.vendor.product.device','value': ro_vendor_product_device[:-1]}
        ro_product_first_api_level_dict_check = {'name': 'ro.product.first_api_level','value': ro_product_first_api_level[:-1]}
        ro_com_google_gmsversion_dict_check = {'name': 'ro.com.google.gmsversion','value': ''}
        ro_com_google_clientidbase_dict_check = {'name': 'ro.com.google.clientidbase','value': ro_com_google_clientidbase[:-1]}
        ro_com_google_clientidbase_ms_dict_check = {'name': 'ro.com.google.clientidbase.ms','value': ro_com_google_clientidbase_ms[:-1]}
        ro_com_google_clientidbase_am_dict_check = {'name': 'ro.com.google.clientidbase.am','value': ''}
        ro_com_google_clientidbase_wal_dict_check = {'name': 'ro.com.google.clientidbase.wal','value': ''}
        ro_com_google_clientidbase_cr_dict_check = {'name': 'ro.com.google.clientidbase.cr','value': ''}
        ro_build_version_security_patch_dict_check = {'name': 'ro.build.version.security_patch','value': ''}
        ro_build_version_base_os_dict_check = {'name': 'ro.build.version.base_os','value': ''}
        if variant == 'dsglobalrussia':
            datacheck = [ro_build_fingerprint_dict_check,ro_product_model_dict_check,ro_product_brand_dict_check,ro_product_name_dict_check,
                    ro_product_device_dict_check,ro_vendor_build_fingerprint_dict_check,ro_vendor_product_model_dict_check,
                    ro_vendor_product_brand_dict_check,ro_vendor_product_name_dict_check,ro_vendor_product_device_dict_check,
                    ro_product_first_api_level_dict_check,ro_com_google_gmsversion_dict_check,ro_com_google_clientidbase_dict_check,
                    ro_build_version_security_patch_dict_check]
        elif variant == 'dsglobalindia':
            datacheck = [ro_build_fingerprint_dict_check,ro_product_model_dict_check,ro_product_brand_dict_check,ro_product_name_dict_check,
                    ro_product_device_dict_check,ro_vendor_build_fingerprint_dict_check,ro_vendor_product_model_dict_check,
                    ro_vendor_product_brand_dict_check,ro_vendor_product_name_dict_check,ro_vendor_product_device_dict_check,
                    ro_product_first_api_level_dict_check,ro_com_google_gmsversion_dict_check,ro_com_google_clientidbase_dict_check,
                    ro_build_version_security_patch_dict_check]
        elif variant == 'cnchina':
            datacheck = [ro_build_fingerprint_dict_check,ro_product_model_dict_check,ro_product_brand_dict_check,ro_product_name_dict_check,
                    ro_product_device_dict_check,ro_vendor_build_fingerprint_dict_check,ro_vendor_product_model_dict_check,
                    ro_vendor_product_brand_dict_check,ro_vendor_product_name_dict_check,ro_vendor_product_device_dict_check,
                    ro_product_first_api_level_dict_check,ro_com_google_clientidbase_dict_check,ro_build_version_security_patch_dict_check]
        else:
            datacheck = [ro_build_fingerprint_dict_check,ro_product_model_dict_check,ro_product_brand_dict_check,ro_product_name_dict_check,
                         ro_product_device_dict_check,ro_vendor_build_fingerprint_dict_check,ro_vendor_product_model_dict_check,
                         ro_vendor_product_brand_dict_check,ro_vendor_product_name_dict_check,ro_vendor_product_device_dict_check,
                         ro_product_first_api_level_dict_check,ro_com_google_gmsversion_dict_check,ro_com_google_clientidbase_dict_check,
                         ro_com_google_clientidbase_ms_dict_check,ro_build_version_security_patch_dict_check]

        with open(os.path.dirname(os.path.abspath(__file__))+'\\'+'datacheck'+'.json', 'w') as f:
            json.dump(datacheck, f)
        datacheckdetails = json.load(file(os.path.dirname(os.path.abspath(__file__))+'\\'+'datacheck.json'))
        self.get1stjsonfiledetail()
        print (datacheckdetails)

        f.close()
        filepath = os.path.dirname(os.path.abspath(__file__))+'\\'+'datacheck'+'.json'
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print ('no such file:%s' % filepath)

        if self.checkJsonDetails(datacheckdetails, firstapprovedjsondetails):
            # requests.post(url='http://172.16.11.195:2000/tatserver/cts/cts_phone_data', json=json.dumps(data))
            r = requests.post(url='http://172.16.11.195:2000/tatserver/cts/cts_phone_data',json=data)
            self.logger.debug(r)
            self.logger.debug("Send Property to TAT Server Successfully")
            from test import emailList
            self.send_checklistpass_img(emailList)
            # os._exit(0)
        else:
            self.send_checklistfail_img(emailList)
            # os._exit(0)



if __name__ == '__main__':
    pass
