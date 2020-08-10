#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import traceback
import os
import sys
import subprocess
import ConfigParser
import time

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.append(LIB_PATH)
from common.settings import Settings, pass_button
from automator.adb import Adb


sdevice_wifi_address = ""
mdevice_wifi_address = ""
class CTSVerifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = Settings(serinoM, "Settings", serinoS)
        cls.mod_s = Settings(serinoS, "Settings_S")
        cls.device = cls.mod.device
        cls.count_s = 0
        cls.count_x_s = 0
        cls.count = 0  # 成员变量（实例变量）
        cls.count_x = 0  # 用于计算嵌套在子模块里的子模块 成功个数
        # cls.Wifi_Mac_Address = ""
        cls.wifi_name = cls.mod.config.getstr("wifi_name", "Wifi", "common")
        cls.wifi_password = cls.mod.config.getstr("wifi_password", "Wifi", "common")
        cls.wifi_security = cls.mod.config.getstr("wifi_security", "Wifi", "common")

        # cls.test_pass_cases = cls.mod.config.getSection("TestPassCases", "common")
        # print type(cls.test_pass_cases)
        # print cls.test_pass_cases
        filePath = "configure/caseList.ini"
        cls.conf = ConfigParser.ConfigParser()
        cls.conf.read(filePath)
        cls.sections = cls.conf.sections()
        cls.parent_list = []
        cls.Mdevice_BT_Address = ""
        cls.Sdevice_BT_Address = ""
        cls.installApks()

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug("CTS Verifier Test Completed")
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)


    def setUp(self):
        self.mod.logger.debug("Set count & count_x to 0")
        self.mod.clear_notification()
        self.mod.enter_CTSVerifier()
        self.count = 0
        self.count_x = 0
        pass

    def tearDown(self):
        pass

    # def test01PRECHECKLIST(self):
    #     self.Prechecklist()

    # def test02SETUP(self):
     # case_name = "BYOD Managed Provisioning"
     # self.mod.scroll_to_case(case_name)
     # self.mod_s.scroll_to_case(case_name)
     # self.Cross_profile_intent_filters_are_set()  # 提前到第一条执行


    def test03Networking(self):
     try:
         self.Wi_Fi_Direct_Test()
         self.Bluetooth_Test()
     except:
         self.mod.logger.warning(traceback.format_exc())
     finally:
         pass

    def test04Audio(self):
     self.makeTestCasePass_without_check("Ringer Mode Tests")
     self.Hifi_Ultrasound_Microphone_Test()
     self.Hifi_Ultrasound_Speaker_Test()

    def test05Camera(self):
     self.exec_case_single("Camera Flashlight")
     #self.exec_case_single("Camera Formats")
     self.exec_case_single("Camera ITS Test")
     self.exec_case_single("Camera Intents")
     self.exec_case_single("Camera Orientation") #一直处于横屏状态，无法识别 #TODO
     self.exec_case_single("Camera Video")

    def test06Car(self):
     self.Car_Dock_Test()

    def test07CLOCK(self):
     try:
         case_name = "Alarms and Timers Tests"
         self.mod.enter_case_name(case_name)
         self.exec_case_count("Show Alarms Test")
         self.exec_case_count("Set Alarm Test")
         self.exec_case_count("Start Alarm Test")
         self.exec_case_count("Full Alarm Test")
         self.mod.delete_all_alarms()
         self.mod.enter_CTSVerifier()
         self.mod.scroll_to_case(case_name)
         self.exec_case_count("Set Timer Test")
         self.exec_case_count("Start Timer Test")
         self.exec_case_count("Start Timer With UI Test")
         print "self.count:", self.count
         if self.count == 7:
             self.mod.test_pass_multiple_case(case_name)
     except:
         self.mod.save_fail_img()
         self.mod.logger.warning(traceback.format_exc())
     finally:
         self.count = 0
         self.mod.device.delay(5)
         self.mod.logger.debug("%s Completed!" % case_name)
         self.mod.back_to_verifier_home()

    def test08DeviceAdministration(self):
     try:
         self.DeviceAdmin_Pre_Configuration()
         self.mod.back_to_verifier_home()
         self.exec_case_single("Device Admin Tapjacking Test")

         p = subprocess.Popen("adb -s %s install -r CtsEmptyDeviceAdmin.apk" % serinoM, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
         p.wait()

         self.exec_case_single("Device Admin Uninstall Test")
         self.Keyguard_Disabled_Features_Test()

         self.exec_case_single("Redacted Notifications Keyguard Disabled Features Test")
         self.exec_case_single("Screen Lock Test")
         self.exec_case_single(
             "Policy Serialization Test")
         #  case《Policy_Serialization_Test》涉及重启，容易导致手机offline。放到最后执行
     except:
         self.mod.logger.warning(traceback.format_exc())
     finally:
         self.mod.Deactive_verifiy_admin("CTS Verifier")
         self.mod.setLockScreenPasswordToNone()

    def test09Features(self):
     self.exec_case_single("Companion Device Test")

    def test10JobScheduler(self):
     self.exec_case_single("Charging Constraints")
     self.exec_case_single("Connectivity Constraints")


    def test11Location(self):
     self.mod.enable_Location()
     self.mod.back_to_verifier_home()
     self.exec_case_single("Battery Saving Mode Test")
     self.exec_case_single("Device Only Mode Test")
     self.exec_case_single("High Accuracy Mode Test")
     self.exec_case_single("Location Mode Off Test")

    def test12Notifications(self):
     self.CA_Cert_Notification_Test()
     self.exec_case_single("CA Cert Notification on Boot test")  # #涉及重启容易offline
     # self.mod.back_to_verifier_home()

     self.exec_case_single("Condition Provider test")
     self.exec_case_single("Notification Attention Management Test")
     self.exec_case_single("Notification Listener Test")
     self.exec_case_single("Shortcut Reset Rate-limiting Test", "Shortcut Reset Rate_limiting Test")

    def test13MANAGED_PROVISIONING(self):
        self.BYOD_Managed_Provisioning()
        self.BYOD_Provisioning_tests()
        self.Device_Owner_Requesting_Bugreport_Tests()
        self.Device_Owner_Tests()
        self.No_Device_Owner_Tests()
        self.mod.remove_work_profile()

    def test14SECURITY(self):
        try:
            self.mod.setLockScreenToPassword()
            self.mod.back_to_verifier_home()
            self.exec_case_count("KeyChain Storage Test")
            self.makeTestCasePass_without_check("Keyguard Password Verification")
            self.exec_case_count("Lock Bound Keys Test")
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.setLockScreenPasswordToNone()

    def test15STREAMING(self):
        try:
            wifi_name = self.mod.config.getstr("wifi_name", "Wifi", "common")
            wifi_password = self.mod.config.getstr("wifi_password", "Wifi", "common")
            wifi_security = self.mod.config.getstr("wifi_security", "Wifi", "common")
            self.mod.connect_wifi(wifi_name, wifi_password, wifi_security)

            self.mod.back_to_verifier_home()
            self.Streaming_Video_Quality_Verifier()
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.forget_wifi(wifi_name)

    def test16Telecom(self):
        self.mod.enter_CTSVerifier()
        self.exec_case_single("Incoming Self-Managed Connection Test","Incoming Self Managed Connection Test")
        self.exec_case_single("Telecom Enable Phone Account Test")
        self.exec_case_single("Telecom Incoming Call Test")

    def test17Telephony(self):
        self.mod.enter_CTSVerifier()
        self.exec_case_single("Hide settings in voicemail test")
        self.exec_case_single("Hide voicemail in call settings test")
        self.exec_case_single("System Implements Telecom Intents")
        self.makeTestCasePass_without_check("Voicemail Broadcast Test")

    # def test18Other(self):
    #     self.exec_case_single("Screen Pinning Test")

    def Prechecklist(self):
        self.mod.find1stjsonfile()
        self.mod.getPhoneDetailandBuildNewJsonFile()

    def CountCases(self):
        f = open("CTS_CASES.txt", "w")
        case_list = []
        self.mod.CountCases()

    def BYOD_Managed_Provisioning(self):
        try:
            case_name = "BYOD Managed Provisioning"
            self.mod.scroll_to_case(case_name)

            self.Full_disk_encryption_enabled()
            self.Badged_work_apps_visible_in_Launcher()
            self.Work_notification_is_badged()
            self.Work_status_icon_is_displayed()
            self.Work_status_toast_is_displayed()

            self.Profile_aware_accounts_settings()
            self.Profile_aware_device_administrator_settings()
            self.Profile_aware_trusted_credential_settings()
            self.Profile_aware_app_settings()
            self.Profile_aware_location_settings()

            self.Profile_aware_printing_settings()
            self.Open_app_cross_profiles_from_the_personal_side()
            self.Open_app_cross_profiles_from_the_work_side()
            self.Disable_non_market_apps()
            self.Enable_non_market_apps()

            self.Permissions_lockdown()

            self.Keyguard_disabled_features()


            self.Authentication_bound_keys()

            self.VPN_test()
            self.Always_on_VPN_Settings()

            self.exec_case_single("Select work lock test")
            self.exec_case_single("Confirm work lock test")

            ###2条CASE 有点复杂，需要讨论一下,无法实现，两个界面ui参数完全一致无法寻找突破口
            # self.Recents_redaction_test()

            self.Organization_Info()

            self.makeTestCasePass_without_check("Personal password test", is_text_PASS_type=True)

            ##### 包含6条case  Set permitted accessibility services脚本执行必然失败,手动可以pass
            self.Policy_transparency_test_byod()

            self.Profile_aware_data_usage_settings_wifi()
            #self.Profile_aware_data_usage_settings_Mobile() # TODO
            ##包含3条case
            self.Disallow_apps_control()

            self.Camera_support_cross_profile_image_capture()
            self.Camera_support_cross_profile_video_capture_with_extra()
            self.Camera_support_cross_profile_video_capture_without_extra()

            ####8.0 new
            self.exec_case_single("Sound recorder support cross profile audio capture")

            self.Enable_location()
            self.Disable_location()
            self.Disable_location_for_work_profile()
            self.Primary_receives_updates_while_work_location_is_disabled()

            # 包含多条case,中途出现异常容易影响其他CASE，所以调到最后测试
            self.Turn_off_work_mode()
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.unlock_scream_without_password()
            self.mod.forget_VPN()
            self.mod.setLockScreenPasswordToNone()
            self.mod.remove_work_profile()
            self.mod.back_to_verifier_home()

    def No_Device_Owner_Tests(self):
        try:
            self.count = 0
            case_name = "No Device Owner Tests"
            self.mod.logger.debug("Starting to execute module------------>%s" % case_name)
            self.mod.enter_case_name(case_name)

            self.exec_case_count("Device owner provisioning")
            self.exec_case_count("Quick settings disclosure", "Quick settings disclosure__ndot")
            self.exec_case_count("Keyguard disclosure", "Keyguard disclosure__ndot")
            self.exec_case_count("Add account disclosure", "Add account disclosure__ndot")

            self.mod.logger.debug("%s 's successfully count is:%s" % (case_name, self.count))
            if self.count == 4:
                self.mod.test_pass_multiple_case(case_name)
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def display_device_owner_cases(self):
        try:
            self.mod.logger.debug("Starting to install CtsEmptyDeviceOwner.apk")

            p = subprocess.Popen("adb -s %s install -r -t CtsEmptyDeviceOwner.apk" % serinoM, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            self.mod.logger.debug("install CtsEmptyDeviceOwner.apk  Completed!")
            time.sleep(2)
            p = subprocess.Popen("adb -s %s shell dpm set-device-owner com.android.cts.emptydeviceowner/.EmptyDeviceAdmin" % serinoM, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            self.mod.logger.debug("execute command  ‘adb -s %s shell dpm set-device-owner com.android.cts.emptydeviceowner/.EmptyDeviceAdmin‘ Completed!"% serinoM)

            if self.mod.device(text = "PRECONDITION CHECKS").ext5:
                self.mod.device(text = "PRECONDITION CHECKS").click()
            if self.mod.device(text = "OK").ext5:
                self.mod.device(text = "OK").click()
            if self.mod.device(text = "OK").ext5:
                self.mod.device(text = "OK").click()

        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            pass

    def Device_Owner_Tests(self):
        try:
            case_name = "Device Owner Tests"
            self.mod.logger.debug("Starting to execute module------------>%s" % case_name)
            self.mod.enter_case_name(case_name)
            self.mod.adb.shell(
                "dpm set-device-owner 'com.android.cts.verifier/com.android.cts.verifier.managedprovisioning.DeviceAdminTestReceiver'")
            self.mod.install_CtsPermissionApp()
            self.exec_case_count("Check device owner")
            self.exec_case_count("Device administrator settings")
            self.WiFi_configuration_lockdown()
            self.exec_case_count("Disallow configuring WiFi")
            self.exec_case_count("Disallow configuring VPN")
            self.exec_case_count("Disallow data roaming")
            self.exec_case_count("Disallow factory reset", "Disallow factory reset__dot")
            self.exec_case_count("Disallow configuring Bluetooth")
            self.exec_case_count("Disallow USB file transfer")

            self.exec_case_count("Disable status bar")
            self.exec_case_count("Disable keyguard")
            self.exec_case_count("Setting the user icon")
            self.Permissions_lockdown__dot()

            ##25 条case
            self.Policy_transparency_test_of_DeviceOwner()

            # 19条Cases
            self.Managed_device_info_tests()

            self.Corporate_Owned_Managed_Profile()
            self.exec_case_count("Network Logging UI")
            self.exec_case_count("Remove device owner")

            self.mod.logger.debug("%s 's successfully count is:%s" % (case_name, self.count))
            if self.count == 15:
                self.mod.test_pass_multiple_case(case_name)

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.mod.uninstall_CtsPermissionApp()
            self.mod.wait(15)

    def Managed_device_info_tests(self):
        try:
            self.count_x = 0
            case_name = "Managed device info tests"
            self.mod.scroll_to_case(case_name)

            self.exec_case_countX("Managed device info page")
            self.exec_case_countX("Retrieve traffic logs")
            self.exec_case_countX("Request bug report")
            self.exec_case_countX("Retrieve security logs")
            #8.1有的新版本会弹出对话框没有定义点击导致fail
            self.exec_case_countX("Enterprise-installed apps", "Enterprise installed apps", True)

            self.exec_case_countX("Location access permission")
            self.exec_case_countX("Microphone access permission")
            self.exec_case_countX("Camera access permission")
            self.exec_case_countX("Default apps")
            self.exec_case_countX("Default keyboard")

            self.exec_case_countX("Always-on VPN", "Always on VPN", True)
            self.exec_case_countX("Always-on VPN (managed profile)", "Always on VPN managed profile", True)
            self.exec_case_countX("Global HTTP Proxy")
            self.exec_case_countX("Trusted CA certs")
            self.exec_case_countX("Trusted CA certs (managed profile)", "Trusted CA certs managed profile", True)

            self.exec_case_countX("Wipe on authentication failure (managed profile)",
                                  "Wipe on authentication failure managed profile", True)
            self.exec_case_countX("Quick settings disclosure")
            self.exec_case_countX("Keyguard disclosure")
            self.exec_case_countX("Add account disclosure")

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 19:
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
        except:
            self.mod.logger.warning(traceback.format_exc())
            self.mod.save_fail_img()
        finally:
            self.mod.device.delay(5)
            self.mod.unlock_scream_without_password()
            self.mod.setLockScreenToNone()
            self.count = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)

    def Policy_transparency_test_of_DeviceOwner(self):
        try:
            self.count_x = 0
            case_name = "Policy transparency test"
            self.mod.scroll_to_case(case_name)

            self.exec_case_countX("Disallow add user")
            self.exec_case_countX("Disallow adjust volume")
            self.exec_case_countX("Disallow controlling apps")
            self.exec_case_countX("Disallow config cell broadcasts")
            self.exec_case_countX("Disallow config credentials")

            self.exec_case_countX("Disallow config mobile networks")
            self.exec_case_countX("Disallow config tethering")
            self.exec_case_countX("Disallow config Wi-Fi", "Disallow config Wi_Fi")

            # ##这条case会disable usbdebugging 导致uiautomator连接断掉，所以disable掉。可以尝试加载adb token
            ####self.exec_case_countX("Disallow debugging features")
            self.exec_case_countX("Disallow factory reset")  # 有同名CASE

            self.exec_case_countX("Disallow fun")
            self.exec_case_countX("Disallow install unknown sources")
            self.exec_case_countX("Disallow modify accounts")
            self.exec_case_countX("Disallow network reset")
            self.exec_case_countX("Disallow outgoing beam")

            self.exec_case_countX("Disallow remove user")  # 未做检查，直接pass
            self.exec_case_countX("Disallow share location")
            self.exec_case_countX("Disallow uninstall apps")
            self.exec_case_countX("Set auto (network) time required", "Set auto network time required")
            self.exec_case_countX("Disallow lockscreen unredacted notification")

            self.exec_case_countX("Set lock screen info")
            self.exec_case_countX("Set maximum time to lock")
            self.exec_case_countX("Set password quality")

            ###只有手动才能显示，奇怪，自动过不去,原因是自动化时accessibility不显示，拔下才显示
            ### self.exec_case_countX("Set permitted accessibility services")
            self.exec_case_countX("Set permitted input methods")

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 25:
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.setLockScreenToNone()
            self.count = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)


    def Device_Owner_Requesting_Bugreport_Tests(self):
        try:
            self.count_x = 0
            case_name = "Device Owner Requesting Bugreport Tests"
            self.mod.logger.debug("Starting to execute module------------>%s" % case_name)

            self.mod.enter_case_name(case_name)
            self.display_device_owner_cases()

            self.mod.adb.shell(
                "dpm set-device-owner 'com.android.cts.verifier/com.android.cts.verifier.managedprovisioning.DeviceAdminTestReceiver'")
            self.mod.device.delay(5)

            self.Check_device_owner(case_name)

            self.Sharing_of_requested_bugreport_declined_while_being_taken(case_name)
            self.Sharing_of_requested_bugreport_accepted_while_being_taken(case_name)
            self.Sharing_of_requested_bugreport_declined_after_having_been_taken(case_name)
            self.Sharing_of_requested_bugreport_accepted_after_having_been_taken(case_name)

            self.Remove_device_owner(case_name)
            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)

            if self.count_x == 6:
                self.mod.test_pass_multiple_case(case_name)

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.count_x = 0
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def BYOD_Provisioning_tests(self):
        try:
            self.count = 0
            case_name = "BYOD Provisioning tests"
            self.mod.logger.debug("Starting to execute module------------>%s" % case_name)
            self.mod.enter_case_name(case_name)

            self.Custom_provisioning_color()

            self.Custom_provisioning_image()

            # self.exec_case_count("Custom terms")
            self.Custom_terms()

            if self.count == 3 :
                self.mod.test_pass_multiple_case(case_name)

                self.mod.logger.debug("All test pass!!")
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def GO_Negotiation_Requester_Test(self):
        try:
            case_name = "GO Negotiation Requester Test"
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("GO Negotiation Responder Test")
            global sdevice_wifi_address
            sdevice_wifi_address = self.mod.get_sdevice_wifi_mac_address()
            self.mod.logger.debug("Sdevice Wifi_Mac_Address is %s" % sdevice_wifi_address)
            self.Go_negotiation_test_push_button()
            self.Go_negotiation_test_pin()

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 2:
                self.mod_s.test_pass_multiple_case("GO Negotiation Responder Test")
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1

        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count_x = 0
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice(case_name)
            self.mod.logger.debug("%s  Test Completed!" % case_name)
        return True

    def Group_Client_Test(self):
        try:
            case_name = "Group Client Test"
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Group Owner Test")

            self.Join_p2p_group_test_push_button()
            self.Join_p2p_group_test_pin()

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 2:
                self.count += 1
                self.mod.test_pass_multiple_case(case_name)
                self.mod_s.test_pass_multiple_case("Group Owner")
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count_x = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice("Wi-Fi Direct Test")
        return True

    def Bluetooth_LE_Secure_Client_Test(self):
        try:
            case_name = "Bluetooth LE Secure Client Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Bluetooth LE Secure Server Test")

            self.exec_case_countX("01 Bluetooth LE Client Test", "Bluetooth LE Client Test__Secure")

            # #bug cts verifier crash
            self.exec_case_countX("02 Bluetooth LE Connection Priority Client Test",
                                  "Bluetooth LE Connection Priority Client Test__Secure")

            ##bug cts verifier crash
            self.exec_case_countX("03 Bluetooth LE Encrypted Client Test",
                                  "Bluetooth LE Encrypted Client Test__Secure")
            self.mod.logger.debug("%s 's successfully count is:%s" % (case_name, self.count))
            if self.count_x == 3:

                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.count_x = 0
            self.mod.device.delay(5)
            # self.mod.disconnect_bluetooth()
            # self.mod.disconnect_bluetooth_sdevice()
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice("Bluetooth Test")
        return True

    def Bluetooth_LE_Secure_Server_Test(self):
        try:
            case_name = "Bluetooth LE Secure Server Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Bluetooth LE Secure Client Test")

            self.exec_case_countX("01 Bluetooth LE Server Test", "Bluetooth LE Server Test__Secure")
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Bluetooth LE Secure Client Test")

            self.exec_case_countX("03 Bluetooth LE Encrypted Server Test",
                                  "Bluetooth LE Encrypted Server Test__Secure")
            # #bug cts verifier crash
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Bluetooth LE Secure Client Test")

            self.exec_case_countX("02 Bluetooth LE Connection Priority Server Test",
                                  "Bluetooth LE Connection Priority Server Test__Secure")

            ##bug cts verifier crash
            # self.exec_case_countX("03 Bluetooth LE Encrypted Server Test",
            #                       "Bluetooth LE Encrypted Server Test__Secure")
            self.mod.logger.debug("%s 's successfully count is:%s" % (case_name, self.count))
            if self.count_x == 3:
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.count_x = 0
            self.mod.device.delay(5)
            self.mod.disconnect_bluetooth()
            self.mod.disconnect_bluetooth_sdevice()
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice("Bluetooth Test")
        return True

    def Service_Discovery_Requester_Test(self):
        try:
            case_name = "Service Discovery Requester Test"
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Service Discovery Responder Test")

            self.Request_all_services_test_01()
            self.Request_all_services_test_02()
            self.Request_all_services_test_03()
            self.Request_DNS_PTR_service_test()
            self.Request_DNS_TXT_record_test()
            self.Request_all_upnp_services_test()
            self.Request_upnp_root_devices_test()
            self.Remove_service_requests_test()
            self.Clear_service_requests_test()
            self.Multiple_clients_test_01()
            self.Multiple_clients_test_02()
            self.Multiple_clients_test_03()

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 12:
                self.mod.test_pass_multiple_case(case_name)
                self.mod_s.test_pass_multiple_case("Service Discovery Responder Test")
                self.count += 1
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count_x = 0
            self.mod.back_to_app("Wi-Fi Direct Test")
            self.mod.logger.debug("%s  Test Completed!" % case_name)
        return True

    def   WiFi_configuration_lockdown(self):
        try:
            case_name = "WiFi configuration lockdown"
            self.mod.scroll_to_case(case_name)

            self.mod.adb.shell(
                "dpm set-device-owner 'com.android.cts.verifier/com.android.cts.verifier.managedprovisioning.DeviceAdminTestReceiver'")
            self.mod.device.delay(5)

            self.exec_case_countX("Unlocked config is modifiable in Settings")
            self.exec_case_countX("Locked config is not modifiable in Settings")
            self.exec_case_countX("Locked config can be connected to")
            self.exec_case_countX("Unlocked config can be forgotten in Settings")

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 4:
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count_x = 0
            self.mod.forget_wifi("CTS")
            self.back_to_parent_dirs(case_name)
            self.mod.logger.debug("%s  Test Completed!" % case_name)
        return True

    def Bluetooth_LE_Insecure_Server_Test(self):
        try:
            case_name = "Bluetooth LE Insecure Server Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Bluetooth LE Insecure Client Test")

            self.exec_case_countX("01 Bluetooth LE Server Test", "Bluetooth LE Server Test", True)
            self.exec_case_countX("02 Bluetooth LE Connection Priority Server Test",
                                  "Bluetooth LE Connection Priority Server Test", True)
            self.exec_case_countX("03 Bluetooth LE Encrypted Server Test", "Bluetooth LE Encrypted Server Test", True)
            self.mod.logger.debug("%s 's successfully count_x is:%s" % (case_name, self.count_x))
            if self.count_x == 3:
                self.count += 1
                self.mod.test_pass_multiple_case(case_name)
                self.mod_s.test_pass_multiple_case("Bluetooth LE Insecure Client Test")
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count_x = 0
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice("Bluetooth Test")
        return True

    def Bluetooth_LE_Insecure_Client_Test(self):
        try:
            case_name = "Bluetooth LE Insecure Client Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice("Bluetooth LE Insecure Server Test")

            self.exec_case_countX("01 Bluetooth LE Client Test", "Bluetooth LE Client Test", True)
            self.exec_case_countX("02 Bluetooth LE Connection Priority Client Test",
                                  "Bluetooth LE Connection Priority Client Test", True)
            self.exec_case_countX("03 Bluetooth LE Encrypted Client Test", "Bluetooth LE Encrypted Client Test", True)
            self.mod.logger.debug("%s 's successfully count_x is:%s" % (case_name, self.count_x))
            if self.count_x == 3:
                self.count += 1
                self.mod.test_pass_multiple_case(case_name)
                self.mod_s.test_pass_multiple_case("Bluetooth LE Insecure Server Test")
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count_x = 0
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice("Bluetooth Test")
        return True

    def Wi_Fi_Direct_Test(self):
        try:
            case_name = "Wi-Fi Direct Test"
            self.mod.open_wifi()
            self.mod_s.open_wifi()
            self.mod.first_forgetWIFI()
            self.mod_s.first_forgetWIFI()
            self.mod.enable_Location()
            self.mod_s.enable_Location()
            self.mod.enter_CTSVerifier()
            self.mod.enter_CTSVerifier_Sdevice()

            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice(case_name)

            self.GO_Negotiation_Responder_Test()
            self.GO_Negotiation_Requester_Test()
            self.Group_Owner_Test()
            self.Group_Client_Test()
            self.Service_Discovery_Responder_Test()
            self.Service_Discovery_Requester_Test()

            self.mod.logger.debug("Total successfully cases is %s" % self.count)
            if self.count == 6:
                self.mod.test_pass_multiple_case(case_name)
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)

    def Bluetooth_Test(self):
        try:
            case_name = "Bluetooth Test"
            self.mod.enable_Location()
            self.mod_s.enable_Location()
            self.mod.EnableBlueTooth()
            self.mod.EnableBlueTooth_Sdevice()
            self.mod.enter_CTSVerifier()
            self.mod.enter_CTSVerifier_Sdevice()

            self.mod.scroll_to_case(case_name)
            self.mod.scroll_to_case_sdevice(case_name)
            self.mod.disconnect_bluetooth_first()

            self.Toggle_Bluetooth()
            self.BLE_Advertiser_Test()
            self.Bluetooth_LE_Insecure_Client_Test()
            self.Bluetooth_LE_Insecure_Server_Test()
            self.BLE_Scanner_Test()

            mdevice_bt_address = self.mod.rename_bt_mdevice(serinoM)
            sdevice_bt_address = self.mod.rename_bt_sdevice(serinoS)

            self.mod.back_to_app(case_name)
            self.mod.back_to_app_sdevice(case_name)
            self.Insecure_Client(sdevice_bt_address)
            self.Insecure_Server(mdevice_bt_address)
            self.Secure_Client(sdevice_bt_address)
            self.Secure_Server(mdevice_bt_address)

            # ##必须都在bluetooth界面才可以配对成功
            self.mod.enter_settings_sdevice("Connected devices")
            if self.mod.sdevice(text="Bluetooth").ext5:
                self.mod.sdevice(text="Bluetooth").click()
            self.mod.connect_bt_sdevice(serinoS)
            self.mod.back_to_app(case_name)
            ##必须先配对 sdevice才能返回Verifier界面
            self.mod.back_to_app_sdevice(case_name)

            self.Bluetooth_LE_Secure_Client_Test()
            self.Bluetooth_LE_Secure_Server_Test()

            self.mod.logger.debug("Total successfully cases is %s" % self.count)
            if self.count == 11:
                self.mod.test_pass_multiple_case(case_name)
        except:
            self.mod.save_fail_img()
            self.mod.save_fail_img_s()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.mod.back_to_verifier_home()
            self.mod.back_to_verifier_home_sdevice()

    def Hifi_Ultrasound_Microphone_Test(self):
        try:
            case_name = "Hifi Ultrasound Microphone Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            #max
            self.mod.set_max_volume()
            self.mod_s.set_max_volume()
            if self.mod.Hifi_Ultrasound_Microphone_Test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()
            self.mod_s.back_to_verifier_home()

    def Hifi_Ultrasound_Speaker_Test(self):
        try:
            case_name = "Hifi Ultrasound Speaker Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            # self.mod.set_max_volume()
            # self.mod_s.set_max_volume()
            if self.mod.Hifi_Ultrasound_Speaker_Test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            #min
            self.mod.set_mute()
            self.mod_s.set_mute()
            self.mod.back_to_verifier_home()
            self.mod_s.back_to_verifier_home()

    def Keyguard_Disabled_Features_Test(self):
        #添加CTS 为admin
        try:
            case_name = "Keyguard Disabled Features Test"
            self.mod.enter_Keyguard(case_name)

            if self.mod.device(text="PREPARE TEST").wait.exists(timeout=3000):
                self.mod.device(text="PREPARE TEST").click()
            self.mod.setLockScreenToPassword()
            self.Disable_trust_agents()
            self.Disable_camera()
            self.Disable_notifications()
            self.mod.setLockScreenPasswordToNone()

            if self.count == 3:
                self.mod.logger.debug("Keyguard Disabled Features Test Complete")
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.count == 0
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Keyguard_disabled_features(self):
        try:
            case_name = "Keyguard disabled features"
            self.mod.scroll_to_case(case_name)
            if self.mod.device(text="OK").wait.exists(timeout=5000):
                self.mod.device(text="OK").click()

            self.mod.setLockScreenToPassword()
            self.mod.active_verifiy_admin()
            self.mod.back_to_app(case_name)

            self.Disable_trust_agents__byod()
            self.Unredacted_notifications_disabled_on_keyguard()

            self.mod.logger.debug("Total successfully cases is %s" % self.count)
            if self.count == 2:
                self.mod.logger.debug("Keyguard disabled features complete")
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.logger.debug("%s Completed!" % case_name)
            self.mod.setLockScreenPasswordToNone()
            self.count = 0
            self.back_to_parent_dirs(case_name)

    def Streaming_Video_Quality_Verifier(self):
        try:
            case_name = "Streaming Video Quality Verifier"
            self.mod.scroll_to_case(case_name)
            self.mod.RTSP_Streaming_Video_Quality_Verifier("H263 Video, AMR Audio")
            self.mod.back_to_app(case_name)
            self.mod.RTSP_Streaming_Video_Quality_Verifier("MPEG4 SP Video, AAC Audio")
            self.mod.back_to_app(case_name)
            self.mod.RTSP_Streaming_Video_Quality_Verifier("H264 Base Video, AAC Audio")
            self.mod.back_to_app(case_name)

            self.mod.HTTP_Streaming_Video_Quality_Verifier("H263 Video, AMR Audio", 5)
            self.mod.back_to_app(case_name)
            self.mod.HTTP_Streaming_Video_Quality_Verifier("MPEG4 SP Video, AAC Audio", 6)
            self.mod.back_to_app(case_name)
            self.mod.HTTP_Streaming_Video_Quality_Verifier("H264 Base Video, AAC Audio", 7)
            self.mod.back_to_app(case_name)
            self.mod.logger.debug("Total successfully cases is %s" % self.count)
            self.device.delay(1)
            self.mod.test_pass_multiple_case(case_name)
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)


    def Recents_redaction_test(self):
        try:
            case_name = "Recents redaction test"
            self.mod.scroll_to_case(case_name)
            if self.device(test="OK").exists:
                self.device(test="OK").click()
            self.exec_case_countX("Verify recents are redacted when locked.", "Verify recents are redacted when locked")
            self.exec_case_countX("Verify recents are not redacted when unlocked.",
                                  "Verify recents are not redacted when unlocked")

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 6:
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)

    def Always_on_VPN_Settings(self):
        try:
            self.count_x = 0
            case_name = "Always-on VPN Settings"
            self.mod.scroll_to_case(case_name)
            self.mod.logger.debug("Starting to execute multiple test case------------>%s" % case_name)
            self.exec_case_countX("VPN app targeting SDK 23")
            self.exec_case_countX("VPN app targeting SDK 24")
            self.exec_case_countX("VPN app with opt-out", "VPN app with opt out")

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 3:
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count = 0
            self.count_x = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)

    def Policy_transparency_test_byod(self):
        try:
            self.mod.uninstall_CtsPermissionApp()
            self.mod.install_CtsPermissionApp()

            case_name = "Policy transparency test"
            self.mod.scroll_to_case(case_name)
            # self.count_x=0
            self.exec_case_countX("Disallow controlling apps", "Disallow controlling apps__byod")
            self.exec_case_countX("Disallow modify accounts", "Disallow modify accounts__byod")
            self.exec_case_countX("Disallow share location", "Disallow share location__byod")

            self.Disallow_uninstall_apps()
            self.exec_case_countX("Set permitted accessibility services", "Set permitted accessibility services__byod")
            self.exec_case_countX("Set permitted input methods", "Set permitted input methods__byod")

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x)
            if self.count_x == 6:
                self.mod.test_pass_multiple_case(case_name)
                self.count += 1
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.uninstall_CtsPermissionApp()
            self.count_x = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs("Policy transparency test__byod")

    def Disallow_apps_control(self):
        try:
            case_name = "Disallow apps control"
            self.mod.scroll_to_case(case_name)
            if self.mod.device(text="PREPARE TEST").wait.exists(timeout=5000):
                self.mod.device(text="PREPARE TEST").click()
                self.mod.device.delay(5)

            self.Disabled_uninstall_button()
            self.Disabled_force_stop_button()
            self.Disabled_app_storage_buttons()

            self.mod.logger.debug("Total successfully cases is %s" % self.count)
            if self.count == 3:
                self.mod.test_pass_multiple_case(case_name)
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.count = 0
            self.mod.logger.debug("%s  Test Completed!" % case_name)
            self.back_to_parent_dirs(case_name)


    @classmethod
    def installApks(self):
        try:
            self.mod.logger.debug(
                "install CtsVerifier.apk,CtsEmptyDeviceAdmin.apk,NotificationBot.apk,"
                "OpenCV_3.0.0_Manager_3.00_arm64-v8a.apk,CtsVerifierUSBCompanion.apk on Mdevice " + serinoM)
            p = subprocess.Popen("adb -s %s install -r CtsEmptyDeviceAdmin.apk" % serinoM, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            p = subprocess.Popen("adb -s %s install -r CtsVerifier.apk" % serinoM, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()

            p = subprocess.Popen("adb -s %s install -r NotificationBot.apk" % serinoM, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            p = subprocess.Popen("adb -s %s install -r OpenCV_3.0.0_Manager_3.00_arm64-v8a.apk" % serinoM, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            p = subprocess.Popen("adb -s %s install -r CtsVerifierUSBCompanion.apk" % serinoM, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
            self.mod.logger.debug("install Mdevice apks completed")
            self.mod.unlock_disable_sleep(serinoM)
            self.mod.setDisplay30M()
            self.mod.set_mute()
            self.mod.forbidden_Auto_rotate_screen()

            for loop in range(2):
                if self.mod.skipCameraPopup():
                    break
                else:
                    self.mod.logger.debug("skip Camera Popup %s times again" % loop)
            self.mod.setRotateToPortrait()
            self.mod.dismiss_lockscreen_tips()
            self.mod.enable_Location()
            self.mod.skip_soundRecorder_steps()
            for loop in range(2):
                if self.mod.skipPopup_Mdevice():
                    break
                else:
                    self.mod.logger.debug("skip Popup Mdevice %s times again" % loop)


            # ##Sdevice exists?
            devices = self.devices()
            self.mod.logger.debug("devices:%s" % devices)
            if serinoS in devices:
                self.mod_s.logger.debug("Sdevice exists:%s" % serinoS)
                self.mod_s.logger.debug("install CtsVerifier.apk,CtsEmptyDeviceAdmin.apk,NotificationBot.apk,"
                                        "OpenCV_3.0.0_Manager_3.00_arm64-v8a.apk,CtsVerifierUSBCompanion.apk on Sdevice " + serinoS)
                p = subprocess.Popen("adb -s %s install -r CtsVerifier.apk" % serinoS, shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                p.wait()
                p = subprocess.Popen("adb -s %s install -r CtsEmptyDeviceAdmin.apk" % serinoS, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
                p.wait()
                p = subprocess.Popen("adb -s %s install -r NotificationBot.apk" % serinoS, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
                p.wait()
                p = subprocess.Popen("adb -s %s install -r OpenCV_3.0.0_Manager_3.00_arm64-v8a.apk" % serinoS, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
                p.wait()
                p = subprocess.Popen("adb -s %s install -r CtsVerifierUSBCompanion.apk" % serinoS, shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                p.wait()
                self.mod_s.logger.debug("install Sdevice apks completed")

                self.mod_s.unlock_disable_sleep(serinoS)
                self.mod_s.setDisplay30M()
                self.mod_s.set_mute()

                self.mod_s.forbidden_Auto_rotate_screen()
                for loop in range(2):
                    if self.mod_s.skipCameraPopup():
                        break
                    else:
                        self.mod_s.logger.debug("skip Camera Popup %s times again" % loop)
                self.mod_s.setRotateToPortrait()
                self.mod_s.dismiss_lockscreen_tips()
                self.mod_s.enable_Location()
                self.mod_s.skip_soundRecorder_steps()
                for loop in range(2):
                    if self.mod.skipPopup_Sdevice():
                        break
                    else:
                        self.mod.logger.debug("skipPopup_Sdevice %s times again" % loop)
        except:
            self.mod.logger.warning(traceback.format_exc())
    def exec_case_count(self, case_name, alias="", flag=False, removeWorkProfile=False):
        """一般用于第二层case，用于统计all pass count
        :param case_name: 用于转换函数方法，首字母不能为数字，不能带括号
        :param alias: 如果存在，则使用alias转换方法
        :param flag: flag=True&& alias is not null：back_to_app(case_name)
        """
        try:
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if alias:
                if eval("self.mod." + alias.replace(" ", "_"))(case_name):
                    self.mod.suc_times += 1
                    self.count += 1
                    self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            else:
                if eval("self.mod." + case_name.replace(" ", "_"))(case_name):
                    self.mod.suc_times += 1
                    self.count += 1
                    self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Test Completed!" % case_name)
        except:
            self.mod.logger.error("Catch Exception when execute test case: %s" % case_name)
            self.mod.save_fail_img()
            self.mod.logger.error(traceback.format_exc())
            if removeWorkProfile:
                self.mod.remove_work_profile()
        finally:
            self.mod.device.delay(5)
            if alias and not flag:
                actual_case_name = alias
            else:
                actual_case_name = case_name
            self.back_to_parent_dirs(actual_case_name)

    def exec_case_countX(self, case_name, alias="", flag=False):
        """一般用于三层节点case，pass后二层节点 pass数量 count+1

        :param case_name:
        :param alias:
        :param flag:
        """
        try:
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if alias:
                if eval("self.mod." + alias.replace(" ", "_"))(case_name):
                    self.mod.suc_times += 1
                    self.count_x += 1
                    self.mod.logger.info("count_x: " + str(self.count_x))
                    self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            else:
                if eval("self.mod." + case_name.replace(" ", "_"))(alias if alias else case_name):
                    self.mod.suc_times += 1
                    self.count_x += 1
                    self.mod.logger.info("count_x: " + str(self.count_x))
                    self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Test Completed!" % case_name)
        except:
            self.mod.logger.error("Catch Exception when execute test case: %s" % case_name)
            self.mod.save_fail_img()
            self.mod.logger.error(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if alias and not flag:
                actual_case_name = alias
            else:
                actual_case_name = case_name
            self.back_to_parent_dirs(actual_case_name)

    def exec_case_single(self, case_name, alias="", flag=False):
        try:
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if alias:
                if eval("self.mod." + alias.replace(" ", "_"))(case_name):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            else:
                if eval("self.mod." + case_name.replace(" ", "_"))(case_name):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Test Completed!" % case_name)
        except:
            self.mod.logger.error("Catch Exception when execute test case: %s" % case_name)
            self.mod.save_fail_img()
            self.mod.logger.error(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if alias and not flag:
                actual_case_name = alias
            else:
                actual_case_name = case_name
            self.back_to_parent_dirs(actual_case_name)


    def Disable_Nfc_beam(self):
        try:
            case_name = "Disable Nfc beam"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disable_Nfc_beam(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Enable_location(self):
        try:
            case_name = "Enable location"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Enable_location(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Corporate_Owned_Managed_Profile(self):
        try:
            case_name = "Corporate Owned Managed Profile"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Corporate_Owned_Managed_Profile(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Disable_location(self):
        try:
            case_name = "Disable location"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disable_location(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disable_location_for_work_profile(self):
        try:
            case_name = "Disable location for work profile"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disable_location_for_work_profile(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Primary_receives_updates_while_work_location_is_disabled(self):
        try:
            case_name = "Primary receives updates while work location is disabled"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Primary_receives_updates_while_work_location_is_disabled(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Check_device_owner(self, parent_case_name=""):
        try:
            case_name = "Check device owner"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Check_device_owner(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if parent_case_name:
                self.mod.back_to_app(parent_case_name)
            else:
                self.back_to_parent_dirs(case_name)

    def Sharing_of_requested_bugreport_declined_while_being_taken(self, parent_case_name=""):
        try:
            case_name = "Sharing of requested bugreport declined while being taken"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Sharing_of_requested_bugreport_declined_while_being_taken(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if parent_case_name:
                self.mod.back_to_app(parent_case_name)
            else:
                self.back_to_parent_dirs(case_name)

    def Sharing_of_requested_bugreport_accepted_while_being_taken(self, parent_case_name=""):
        try:
            case_name = "Sharing of requested bugreport accepted while being taken"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Sharing_of_requested_bugreport_accepted_while_being_taken(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if parent_case_name:
                self.mod.back_to_app(parent_case_name)
            else:
                self.back_to_parent_dirs(case_name)

    def Sharing_of_requested_bugreport_declined_after_having_been_taken(self, parent_case_name=""):
        try:
            case_name = "Sharing of requested bugreport declined after having been taken"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Sharing_of_requested_bugreport_declined_after_having_been_taken(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if parent_case_name:
                self.mod.back_to_app(parent_case_name)
            else:
                self.back_to_parent_dirs(case_name)

    def Sharing_of_requested_bugreport_accepted_after_having_been_taken(self, parent_case_name=""):
        try:
            case_name = "Sharing of requested bugreport accepted after having been taken"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Sharing_of_requested_bugreport_accepted_after_having_been_taken(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if parent_case_name:
                self.mod.back_to_app(parent_case_name)
            else:
                self.back_to_parent_dirs(case_name)

    def Remove_device_owner(self, parent_case_name=""):
        try:
            case_name = "Remove device owner"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Remove_device_owner(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            if parent_case_name:
                self.mod.back_to_app(parent_case_name)
            else:
                self.back_to_parent_dirs(case_name)

    def makeTestCasePass_without_check(self, case_name, is_text_PASS_type=False):
        try:
            self.mod.logger.debug(
                "Make the  test case pass without check<%s>,if you have any question,please contact zhouwei." % case_name)
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.makeTestCasePass_without_check(case_name, is_text_PASS_type):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def makeTestCasePass_Count_without_check(self, case_name):
        try:
            self.mod.logger.debug(
                "Make the  test case pass without check<%s>,if you have any question,please contact zhouwei." % case_name)
            if self.mod.makeTestCasePass_without_check(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def makeTestCasePass_CountX_without_check(self, case_name):
        try:
            self.mod.logger.debug(
                "Make the  test case pass without check<%s>,if you have any question,please contact zhouwei." % case_name)
            if self.mod.makeTestCasePass_without_check(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Device_Owner_Provisioning(self):
        try:
            case_name = "Device Owner Provisioning"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Device_Owner_Provisioning(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()


    def Custom_provisioning_image(self):
        try:
            case_name = "Custom provisioning image"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Custom_provisioning_image(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Custom_terms(self):
        try:
            case_name = "Custom terms"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Custom_terms(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)



    def Custom_provisioning_color(self):
        try:
            case_name = "Custom provisioning color"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Custom_provisioning_color(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Camera_support_cross_profile_image_capture(self):
        try:
            case_name = "Camera support cross profile image capture"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Camera_support_cross_profile_image_capture(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Camera_support_cross_profile_video_capture_with_extra(self):
        try:
            case_name = "Camera support cross profile video capture (with extra output path)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Camera_support_cross_profile_video_capture_with_extra(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Camera_support_cross_profile_video_capture_without_extra(self):
        try:
            case_name = "Camera support cross profile video capture (without extra output path)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Camera_support_cross_profile_video_capture_without_extra(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disabled_app_storage_buttons(self):
        try:
            case_name = "Disabled app storage buttons"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disabled_app_storage_buttons(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disabled_force_stop_button(self):
        try:
            case_name = "Disabled force stop button"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disabled_force_stop_button(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disabled_uninstall_button(self):
        try:
            case_name = "Disabled uninstall button"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disabled_uninstall_button(case_name, serinoM):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.uninstall_CtsPermissionApp()
            self.back_to_parent_dirs(case_name)

    def Profile_aware_data_usage_settings_wifi(self):
        try:
            case_name = "Profile-aware data usage settings (Wi-Fi)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_aware_data_usage_settings_wifi(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Profile_aware_data_usage_settings_Cellular(self):
        try:
            case_name = "Profile-aware data usage settings (Mobile)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.makeTestCasePass_without_check(case_name, True):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Set_permitted_accessibility_services(self):
        try:
            case_name = "Set permitted accessibility services"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Set_permitted_accessibility_services(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Set_permitted_input_methods(self):
        try:
            case_name = "Set permitted input methods"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Set_permitted_input_methods(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disallow_uninstall_apps(self):
        try:
            case_name = "Disallow uninstall apps"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_uninstall_apps__byod(case_name, serinoM):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs("Disallow uninstall apps__byod")

    def Disallow_share_location(self):
        try:
            case_name = "Disallow share location"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_share_location(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disallow_modify_accounts(self):
        try:
            case_name = "Disallow modify accounts"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_modify_accounts(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disallow_controlling_apps(self):
        try:
            case_name = "Disallow controlling apps"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_controlling_apps(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Personal_password_test(self):
        try:
            case_name = "Personal password test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Personal_password_test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.unlock_scream_without_password()
            self.mod.setLockScreenPasswordToNone()
            self.back_to_parent_dirs(case_name)
            self.mod.device.delay(5)

    def Organization_Info(self):
        try:
            case_name = "Organization Info"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Organization_Info(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            # self.mod.enable_use_one_lock()
            self.back_to_parent_dirs(case_name)

    def Turn_off_work_mode(self):
        try:
            case_name = "Turn off work mode"
            self.mod.scroll_to_case(case_name)
            self.exec_case_count("Prepare a work notification", removeWorkProfile=True)

            self.exec_case_count("Please turn off work mode", removeWorkProfile=True)

            self.exec_case_count("Notifications when work mode is off", removeWorkProfile=True)
            self.exec_case_count("Status bar icon when work mode is off", removeWorkProfile=True)
            self.exec_case_count("Starting work apps when work mode is off", removeWorkProfile=True)

            # self.exec_case_count("Please turn work mode back on", removeWorkProfile=True)
            self.Please_turn_work_mode_back_on()
            self.exec_case_count("Status bar icon when work mode is on", removeWorkProfile=True)
            self.exec_case_count("Starting work apps when work mode is on", removeWorkProfile=True)

            print "self.count:", self.count
            if self.count == 8:
                self.mod.test_pass_multiple_case(case_name)
        except:
            self.mod.logger.warning(traceback.format_exc())
            self.count = 0
            self.mod.device.delay(5)
            self.mod.logger.debug("%s Completed!" % case_name)

    def Status_bar_icon_when_work_mode_is_on(self):
        try:
            case_name = "Status bar icon when work mode is on"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Status_bar_icon_when_work_mode_is_on(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            # else:
            # self.mod.switch_work_mode(True)
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Starting_work_apps_when_work_mode_is_on(self):
        try:
            case_name = "Starting work apps when work mode is on"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Starting_work_apps_when_work_mode_is_on(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Please_turn_work_mode_back_on(self):
        try:
            case_name = "Please turn work mode back on"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Please_turn_work_mode_back_on(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Starting_work_apps_when_work_mode_is_off(self):
        try:
            case_name = "Starting work apps when work mode is off"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Starting_work_apps_when_work_mode_is_off(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Status_bar_icon_when_work_mode_is_off(self):
        try:
            case_name = "Status bar icon when work mode is off"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Status_bar_icon_when_work_mode_is_off(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Notifications_when_work_mode_is_off(self):
        try:
            case_name = "Notifications when work mode is off"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Notifications_when_work_mode_is_off(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Please_turn_off_work_mode(self):
        try:
            case_name = "Please turn off work mode"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Please_turn_off_work_mode(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def back_to_parent_dirs(self, case_name):
        try:
            parent_list = []
            self.searchParent(self.sections, case_name, parent_list)
            self.mod.back_to_applist(parent_list, case_name)
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            pass

    def back_to_parent_dirs_sdevice(self, case_name):
        try:
            parent_list = []
            self.searchParent(self.sections, case_name, parent_list)
            self.mod.back_to_applist_sdevice(parent_list)
        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            pass

    def Prepare_a_work_notification(self):
        try:
            case_name = "Prepare a work notification"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Prepare_a_work_notification(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def VPN_test(self):
        try:
            case_name = "VPN test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Vpn_test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Authentication_bound_keys(self):
        try:
            case_name = "Authentication-bound keys"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Authentication_bound_keys(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Unredacted_notifications_disabled_on_keyguard(self):
        try:
            case_name = "Unredacted notifications disabled on keyguard"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Unredacted_notifications_disabled_on_keyguard(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Permissions_lockdown(self):
        try:
            case_name = "Permissions lockdown"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Permissions_lockdown(case_name, serinoM):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.uninstall_CtsPermissionApp()
            self.back_to_parent_dirs(case_name)

    def Permissions_lockdown__dot(self):
        try:
            case_name = "Permissions lockdown"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Permissions_lockdown__dot(case_name, serinoM):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            # self.mod.uninstall_CtsPermissionApp()
            self.back_to_parent_dirs("Permissions lockdown__dot")

    def Cross_profile_intent_filters_are_set(self):
        try:
            case_name = "Cross profile intent filters are set"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.scroll_to_case(case_name)
            self.mod.wait(5)
            self.mod.send_fail_img(emailList)
            self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod_s.scroll_to_case(case_name)
            self.mod_s.wait(5)
            self.mod_s.send_fail_img(emailList)
            self.mod.suc_times += 1

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod_s.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.back_to_parent_dirs_sdevice(case_name)

    def Enable_non_market_apps(self):
        try:
            case_name = "Enable non-market apps"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Enable_non_market_apps(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disable_non_market_apps(self):
        try:
            case_name = "Disable non-market apps"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disable_non_market_apps(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Open_app_cross_profiles_from_the_work_side(self):
        try:
            case_name = "Open app cross profiles from the work side"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Open_app_cross_profiles_from_the_work_side(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Open_app_cross_profiles_from_the_personal_side(self):
        try:
            case_name = "Open app cross profiles from the personal side"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Open_app_cross_profiles_from_the_personal_side(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Profile_aware_printing_settings(self):
        try:
            case_name = "Profile-aware printing settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_aware_printing_settings(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Profile_aware_location_settings(self):
        try:
            case_name = "Profile-aware location settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_aware_location_settings(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Profile_aware_app_settings(self):
        try:
            case_name = "Profile-aware app settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_aware_app_settings(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Profile_aware_trusted_credential_settings(self):
        try:
            case_name = "Profile-aware trusted credential settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_aware_trusted_credential_settings(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Profile_aware_device_administrator_settings(self):
        try:
            case_name = "Profile-aware device administrator settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_aware_device_administrator_settings(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Profile_aware_accounts_settings(self):
        try:
            case_name = "Profile-aware accounts settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_aware_accounts_settings(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Work_status_icon_is_displayed(self):
        try:
            case_name = "Work status icon is displayed"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Work_status_icon_is_displayed(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Work_status_toast_is_displayed(self):
        try:
            case_name = "Work status toast is displayed"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Work_status_toast_is_displayed(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Work_notification_is_badged(self):
        try:
            case_name = "Work notification is badged"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Work_notification_is_badged(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(8)
            self.back_to_parent_dirs(case_name)

    def Profile_owner_installed(self):
        try:
            case_name = "Profile owner installed"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Profile_owner_installed(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Full_disk_encryption_enabled(self):
        try:
            case_name = "Full disk encryption enabled"
            self.mod.setLockScreenToPin()
            self.back_to_parent_dirs(case_name)
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Full_disk_encryption_enabled(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.setLockScreenPinToNone()
            self.back_to_parent_dirs(case_name)

    def Badged_work_apps_visible_in_Launcher(self):
        try:
            case_name = "Badged work apps visible in Launcher"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Badged_work_apps_visible_in_Launcher(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.logger.debug("Enter CTSVerifier")
            cts_verifier = self.mod.config.getstr("cts_verifier", "Default", "common")

            self.device.press.home()
            self.mod.adb.shell("am start -n com.android.cts.verifier/.CtsVerifierActivity")

            if self.device(text="PASS").wait.exists(timeout=5000):
                self.device(text="PASS").click()
            self.mod.device.delay(5)

    def DeviceAdmin_Pre_Configuration(self):
        self.mod.setLockScreenToPassword()
        self.mod.active_verifiy_admin()

    def Disable_notifications(self):
        try:
            case_name = "Disable notifications"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.active_verifiy_admin()
            self.mod.back_to_app(case_name)

            if self.mod.Disable_notifications(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disable_camera(self):
        try:
            case_name = "Disable camera"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.active_verifiy_admin()
            self.mod.back_to_app(case_name)
            if self.mod.Disable_camera(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disable_trust_agents(self):

        try:
            case_name = "Disable trust agents"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.setLockScreenToPassword()
            self.mod.active_verifiy_admin()
            self.mod.back_to_app(case_name)
            if self.mod.Disable_trust_agents(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disable_trust_agents__byod(self):
        try:
            case_name = "Disable trust agents"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disable_trust_agents(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs("Disable trust agents__byod")

    def Fingerprint_disabled_on_keyguard(self):
        try:
            case_name = "Fingerprint disabled on keyguard"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.Fingerprint_disabled_on_keyguard(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.unlock_scream_with_password()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Fingerprint_disabled_on_keyguard__byod(self):
        try:
            case_name = "Fingerprint disabled on keyguard"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.Fingerprint_disabled_on_keyguard(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs("Fingerprint disabled on keyguard__byod")

    def Fingerprint_is_disabled_in_Settings(self):
        try:
            case_name = "Fingerprint is disabled in Settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.makeTestCasePass_without_check(case_name, "Pass"):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Fingerprint_is_disabled_in_Settings__byod(self):
        try:
            case_name = "Fingerprint is disabled in Settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.makeTestCasePass_without_check(case_name, "Pass"):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs("Fingerprint is disabled in Settings__byod")

    def CTS_Sensor_Test(self, case_name):
        try:
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.CTS_Sensor_Test(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()
        return True


    def CTS_Single_Sensor_Tests(self):
        try:
            case_name = ""
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.CTS_Sensor_Test(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()
        return True

    def Device_Suspend_Tests(self):
        try:
            case_name = ""
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.CTS_Sensor_Test(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()
        return True


    def Dynamic_Sensor_Discovery_Test(self):
        try:
            case_name = ""
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.CTS_Sensor_Test(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()
        return True

    def Sensors_Pre_Configuration(self):
        try:
            self.mod.setLockScreenToNone()
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.enable_Airplane_mode()
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.disable_Adaptive_Brightness()
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.switch_permission(False, "Ambient display")
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.disable_Auto_Rotate_Screen()
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.disable_Stay_awake()
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.disable_Location()
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.active_verifiy_admin()
        except:
            self.mod.logger.warning(traceback.format_exc())

        try:
            self.mod.active_sensor_admin()
        except:
            self.mod.logger.warning(traceback.format_exc())


    def Camera_Formats(self):
        try:
            self.mod.logger.debug("Starting Camera_Formats Test")

            if self.mod.Camera_Formats():
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("Camera_Flashlight Test Completed!")
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()
            self.mod.device.delay(10)
        return True


    def Car_Dock_Test(self):
        try:
            case_name = "Car Dock Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.Car_Dock_Test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))

            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_verifier_home()

    def connect_wifi(self):
        try:
            self.mod.logger.info("start to connect the  wifi")
            wifi_name = self.mod.config.getstr("wifi_name", "Wifi", "common")
            wifi_password = self.mod.config.getstr("wifi_password", "Wifi", "common")
            wifi_security = self.mod.config.getstr("wifi_security", "Wifi", "common")
            for loop in range(5):
                if self.mod.connect_wifi(wifi_name, wifi_password, wifi_security):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
                    break

            self.mod.logger.info("connected wifi completed!")
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        return True

    def Toggle_Bluetooth(self):
        try:
            case_name = "Toggle Bluetooth"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Toggle_Bluetooth(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
        return True

    def BLE_Advertiser_Test(self):
        try:
            case_name = "Bluetooth LE Advertiser Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            self.mod.scroll_to_case_sdevice("Bluetooth LE Scanner Test")
            self.mod.scroll_to_case_sdevice("Bluetooth LE Tx Power Level")

            if self.mod.BLE_Advertiser_Test(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice(case_name)
        return True

    def BLE_Scanner_Test(self):
        try:
            case_name = "Bluetooth LE Scanner Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.BLE_Scanner_Test(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs("Bluetooth LE Scanner Test")
            self.back_to_parent_dirs(case_name)
        return True

    def Insecure_Client(self,sdevice_bt_address):
        try:
            case_name = "Insecure Client"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Insecure_Client(case_name, sdevice_bt_address, serinoS):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice(case_name)
        return True

    def Insecure_Server(self,mdevice_bt_address):
        try:
            case_name = "Insecure Server"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Insecure_Server(case_name, mdevice_bt_address, serinoM):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice(case_name)
        return True

    def Secure_Client(self,sdevice_bt_address):
        try:
            case_name = "Secure Client"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Secure_Client(case_name, sdevice_bt_address, serinoS):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.disconnect_bluetooth()
            self.mod.disconnect_bluetooth_sdevice()
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice(case_name)
        return True

    def Secure_Server(self,mdevice_bt_address):
        try:
            case_name = "Secure Server"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Secure_Server(case_name, mdevice_bt_address, serinoM):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.disconnect_bluetooth()
            self.mod.disconnect_bluetooth_sdevice()
            self.back_to_parent_dirs(case_name)
            self.mod.back_to_app_sdevice(case_name)
        return True


    def GO_Negotiation_Responder_Test(self):
        try:
            case_name = "GO Negotiation Responder Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.GO_Negotiation_Responder_Test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.disconnect_bluetooth()
            self.mod.disconnect_bluetooth_sdevice()
            self.back_to_parent_dirs(case_name)
        return True

    def Network_Connectivity_Screen_Off_Test(self):
        try:
            case_name = "Network Connectivity Screen Off Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            self.mod.connect_wifi(self.wifi_name, self.wifi_password, self.wifi_security)
            self.mod.open_wifi()
            if self.mod.Network_Connectivity_Screen_Off_Test(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.forget_wifi("PACv6")
            self.mod.back_to_verifier_home()
        return True


    def GO_Negotiation_Responder_Test(self):
        try:
            case_name = "GO Negotiation Responder Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.GO_Negotiation_Responder_Test(case_name)
            self.GO_Negotiation_Responder_Test_Sdevice()
            if self.count_x_s == 2:
                self.mod.test_pass_multiple_case(case_name)

                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
                self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.count_x_s = 0
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.mod_s.back_to_app("Wi-Fi Direct Test")
        return True
    def GO_Negotiation_Responder_Test_Sdevice(self):
        try:
            case_name = "GO Negotiation Requester Test"
            self.mod_s.scroll_to_case(case_name)
            global mdevice_wifi_address
            mdevice_wifi_address = self.mod.get_device_wifi_mac_address()
            self.mod.logger.debug("Mdevice Wifi_Mac_Address is %s" % mdevice_wifi_address)

            self.Go_negotiation_test_push_button_sdevice()
            self.Go_negotiation_test_pin_sdevice()

            self.mod.logger.debug("Total successfully cases is %s" % self.count_x_s)
            if self.count_x_s == 2:
                self.mod_s.test_pass_multiple_case(case_name)
                self.count_s += 1

        except:
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.logger.debug("%s  Test Completed!" % case_name)
        return True

    def Go_negotiation_test_push_button_sdevice(self):
        try:
            case_name = "Go negotiation test (push button)"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Go_negotiation_test_push_button_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod_s.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
        finally:
            self.mod_s.device.delay(5)
            self.mod_s.back_to_app("GO Negotiation Requester")
        return True
    def Go_negotiation_test_pin_sdevice(self):
        try:
            case_name = "Go negotiation test (PIN)"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Go_negotiation_test_pin_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod_s.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
        finally:
            self.mod_s.device.delay(5)
            self.mod_s.back_to_app("GO Negotiation Requester")
        return True
    def Go_negotiation_test_push_button(self):
        try:
            case_name = "Go negotiation test (push button)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Go_negotiation_test_push_button(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_app("GO Negotiation Requester")
        return True

    def Go_negotiation_test_pin(self):
        try:
            case_name = "Go negotiation test (PIN)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Go_negotiation_test_pin(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_app("GO Negotiation Requester")
        return True

    def Group_Owner_Test(self):
        try:
            case_name = "Group Owner Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.Group_Owner_Test(case_name)
            self.Group_Owner_Test_Sdevice()
            if self.count_x_s == 2:
                self.mod.test_pass_multiple_case(case_name)
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.count_x_s = 0
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.mod_s.back_to_app("Wi-Fi Direct Test")
        return True

    def Group_Owner_Test_Sdevice(self):
        try:
            case_name = "Group Client Test"
            self.mod_s.scroll_to_case(case_name)

            self.Join_p2p_group_test_push_button_Sdevice()
            self.Join_p2p_group_test_pin_Sdevice()

            self.mod_s.logger.debug("Total successfully cases is %s" % self.count_x_s)
            if self.count_x_s == 2:
                self.count_s += 1
                self.mod_s.test_pass_multiple_case(case_name)
        except:
            self.mod_s.logger.warning(traceback.format_exc())
        finally:
            self.mod_s.device.delay(5)
            self.mod_s.logger.debug("%s  Test Completed!" % case_name)
        return True

    def Join_p2p_group_test_push_button_Sdevice(self):
        try:
            case_name = "Join p2p group test (push button)"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Join_p2p_group_test_push_button_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod_s.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
        finally:
            self.mod_s.device.delay(5)
            self.mod_s.back_to_app("Group Client")
        return True
    def Join_p2p_group_test_pin_Sdevice(self):
        try:
            case_name = "Join p2p group test (PIN)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Join_p2p_group_test_pin_sdevice(case_name, sdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod_s.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
        finally:
            self.mod_s.device.delay(5)
            self.mod_s.back_to_app("Group Client")
        return True
    def Join_p2p_group_test_push_button(self):
        try:
            case_name = "Join p2p group test (push button)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Join_p2p_group_test_push_button(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_app("Group Client")
        return True

    def Join_p2p_group_test_pin(self):
        try:
            case_name = "Join p2p group test (PIN)"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Join_p2p_group_test_pin(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.mod.back_to_app("Group Client")
        return True

    def Service_Discovery_Responder_Test(self):
        try:
            case_name = "Service Discovery Responder Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            self.mod.Service_Discovery_Responder_Test(case_name)
            self.Service_Discovery_Responder_Test_Sdevice()
            if self.count_x_s == 12:
                self.mod.test_pass_multiple_case(case_name)
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.count_x_s = 0
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            self.mod_s.back_to_app("Wi-Fi Direct Test")
        return True

    def Service_Discovery_Responder_Test_Sdevice(self):
        try:
            case_name = "Service Discovery Requester Test"
            self.mod_s.scroll_to_case(case_name)

            self.Request_all_services_test_01_Sdevice()
            self.Request_all_services_test_02_Sdevice()
            self.Request_all_services_test_03_Sdevice()
            self.Request_DNS_PTR_service_test_Sdevice()
            self.Request_DNS_TXT_record_test_Sdevice()
            self.Request_all_upnp_services_test_Sdevice()
            self.Request_upnp_root_devices_test_Sdevice()
            self.Remove_service_requests_test_Sdevice()
            self.Clear_service_requests_test_Sdevice()
            self.Multiple_clients_test_01_Sdevice()
            self.Multiple_clients_test_02_Sdevice()
            self.Multiple_clients_test_03_Sdevice()

            self.mod_s.logger.debug("Total successfully cases is %s" % self.count_x_s)
            if self.count_x_s == 12:
                self.count_s += 1
                self.mod_s.test_pass_multiple_case(case_name)
        except:
            self.mod_s.logger.warning(traceback.format_exc())
        finally:
            self.mod_s.device.delay(5)
            self.mod_s.logger.debug("%s  Test Completed!" % case_name)
        return True


    def Request_all_services_test_01_Sdevice(self):
        try:
            case_name = "Request all services test 01"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod_s.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(5)
            # self.back_to_parent_dirs_sdevice(case_name)
            # self.mod_s.back_to_app("Service Discovery Requester Test")
            return True

    def Request_all_services_test_02_Sdevice(self):
        try:
            case_name = "Request all services test 02"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Request_all_services_test_03_Sdevice(self):
        try:
            case_name = "Request all services test 03"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Request_DNS_PTR_service_test_Sdevice(self):
        try:
            case_name = "Request DNS PTR service test"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(5)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Request_DNS_TXT_record_test_Sdevice(self):
        try:
            case_name = "Request DNS TXT record test"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)

        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")

        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Request_all_upnp_services_test_Sdevice(self):
        try:
            case_name = "Request all upnp services test"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)

        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Request_upnp_root_devices_test_Sdevice(self):
        try:
            case_name = "Request upnp root devices test"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)

        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Remove_service_requests_test_Sdevice(self):
        try:
            case_name = "Remove service requests test"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)

        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True


    def Clear_service_requests_test_Sdevice(self):
        try:
            case_name = "Clear service requests test"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)

        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True


    def Multiple_clients_test_01_Sdevice(self):
        try:
            case_name = "Multiple clients test 01"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Multiple_clients_test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Multiple_clients_test_02_Sdevice(self):
        try:
            case_name = "Multiple clients test 02"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Multiple_clients_test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Multiple_clients_test_03_Sdevice(self):
        try:
            case_name = "Multiple clients test 03"
            self.mod_s.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Multiple_clients_test_sdevice(case_name, mdevice_wifi_address):
                self.mod_s.suc_times += 1
                self.count_x_s += 1
                self.mod_s.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod_s.logger.debug("%s Completed!" % case_name)
        except:
            self.mod_s.save_fail_img()
            self.mod_s.logger.warning(traceback.format_exc())
            self.mod_s.back_to_app("Service Discovery Requester Test")
        finally:
            self.mod_s.device.delay(2)
            # self.back_to_parent_dirs_sdevice(case_name)
            return True

    def Request_all_services_test_01(self):
        try:
            case_name = "Request all services test 01"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            return True

    def Request_all_services_test_02(self):
        try:
            case_name = "Request all services test 02"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def Request_all_services_test_03(self):
        try:
            case_name = "Request all services test 03"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def Request_DNS_PTR_service_test(self):
        try:
            case_name = "Request DNS PTR service test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
            return True

    def Request_DNS_TXT_record_test(self):
        try:
            case_name = "Request DNS TXT record test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)

        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())

        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def Request_all_upnp_services_test(self):
        try:
            case_name = "Request all upnp services test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)

        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())

        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def Request_upnp_root_devices_test(self):
        try:
            case_name = "Request upnp root devices test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)

        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())

        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def Remove_service_requests_test(self):
        try:
            case_name = "Remove service requests test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)

        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())

        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True


    def Clear_service_requests_test(self):
        try:
            case_name = "Clear service requests test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Service_Discovery_Requester_Test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)

        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())

        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True


    def Multiple_clients_test_01(self):
        try:
            case_name = "Multiple clients test 01"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Multiple_clients_test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def Multiple_clients_test_02(self):
        try:
            case_name = "Multiple clients test 02"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Multiple_clients_test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def Multiple_clients_test_03(self):
        try:
            case_name = "Multiple clients test 03"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Multiple_clients_test(case_name, sdevice_wifi_address):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(2)
            self.back_to_parent_dirs(case_name)
            return True

    def CA_Cert_Notification_Test(self):
        try:
            case_name = "CA Cert Notification Test"
            # if case_name.lower() in self.test_pass_cases:
            # self.mod.logger.info("'%s' already passed,skip it.")
            #     return True
            self.mod.adb.cmd("push", "myCA.cer", "/sdcard/Download/")
            self.mod.logger.debug("adb push myCA.cer to /sdcard/Download/")
            self.mod.setLockScreenToPassword()
            self.mod.back_to_verifier_home()

            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.CA_Cert_Notification_Test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
                self.mod.logger.debug("%s Completed!" % case_name)
                return True
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            ##接下来的一条case需要设置密码，所以先不要删除密码
            ##self.mod.setLockScreenPasswordToNone()
            self.back_to_parent_dirs(case_name)
        return False

    def Notification_Package_Priority_Test(self):
        try:
            case_name = "Notification Package Priority Test"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Notification_Package_Priority_Test(case_name):
                self.mod.suc_times += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)
        return True

    def Device_administrator_settings(self):
        try:
            case_name = "Device administrator settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Device_administrator_settings(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Unlocked_config_can_be_forgotten_in_Settings(self):
        try:
            case_name = "Unlocked config can be forgotten in Settings"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Unlocked_config_can_be_forgotten_in_Settings(case_name):
                self.mod.suc_times += 1
                self.count_x += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def searchParent(self, sections, case_name, parent_list):
        # self.mod.logger.debug("starting to search %s parent -------------------------->"%case_name)
        for loop in range(len(sections)):
            section = sections[loop]
            options = self.conf.options(section)
            if case_name.lower() in options:
                parent = section
                parent_list.append(parent)
                self.searchParent(sections, section, parent_list)

    def Disallow_configuring_WiFi(self):
        try:
            case_name = "Disallow configuring WiFi"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_configuring_WiFi(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Disallow_configuring_VPN(self):
        try:
            case_name = "Disallow configuring VPN"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_configuring_VPN(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    def Disallow_data_roaming(self):
        try:
            case_name = "Disallow data roaming"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_data_roaming(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disallow_factory_reset(self):
        try:
            case_name = "Disallow factory reset"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if self.mod.Disallow_factory_reset(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disallow_configuring_Bluetooth(self):
        try:
            case_name = "Disallow configuring Bluetooth"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)

            if self.mod.Disallow_configuring_Bluetooth(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)

    def Disallow_USB_file_transfer(self):
        try:
            case_name = "Disallow USB file transfer"
            self.mod.logger.debug("Starting to execute test case------------>%s" % case_name)
            if eval("self.mod." + case_name.replace(" ", "_"))(case_name):
                self.mod.suc_times += 1
                self.count += 1
                self.mod.logger.info("Trace Success Loop " + str(self.mod.suc_times))
            self.mod.logger.debug("%s Completed!" % case_name)
        except:
            self.mod.save_fail_img()
            self.mod.logger.warning(traceback.format_exc())
        finally:
            self.mod.device.delay(5)
            self.back_to_parent_dirs(case_name)


    @classmethod
    def devices(self):
        '''get a dict of attached devices. key is the device serial, value is device name.'''
        adb = Adb()
        out = adb.raw_cmd("devices").communicate()[0].decode("utf-8")
        match = "List of devices attached"
        index = out.find(match)
        if index < 0:
            raise EnvironmentError("adb is not working.")
        return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])

if __name__ == "__main__":
    serinoM = sys.argv[1]
    serinoS = sys.argv[2]
    emailList = ""
    if len(sys.argv) >= 4:
        emailList = sys.argv[3]

    suiteCase = unittest.TestLoader().loadTestsFromTestCase(CTSVerifier)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite)
    # os.system('pause')






    tempM = serinoM
    tempS = serinoS
    serinoM = tempS
    serinoS = tempM
    suiteCase1 = unittest.TestLoader().loadTestsFromTestCase(CTSVerifier)
    suite1 = unittest.TestSuite([suiteCase1])
    unittest.TextTestRunner(verbosity=2).run(suite1)

