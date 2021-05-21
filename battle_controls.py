#!/usr/bin/env python

"""
GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
"""

import random
import easygopigo3 as easy
import threading
from time import sleep

class GoPiGo3WithKeyboard(object):
    """
    Class for interfacing with the GoPiGo3.
    It's functionality is to map different keys
    of the keyboard to different commands of the GoPiGo3.
    """

    KEY_DESCRIPTION = 0
    KEY_FUNC_SUFFIX = 1

    left_blinker_on = False
    right_blinker_on = False

    left_eye_on = False
    right_eye_on = False
    EYES_ON = False
    
    BASESPEED = 10000
    BASESPEEDTURN = 300

    def __init__(self):
        """
        Instantiates the key-bindings between the GoPiGo3 and the keyboard's keys.
        Sets the order of the keys in the menu.
        """
        self.gopigo3 = easy.EasyGoPiGo3()
        self.keybindings = {
        "w" : ["Move the GoPiGo3 forward", "forward"],
        "s" : ["Move the GoPiGo3 backward", "backward"],
        "a" : ["Turn the GoPiGo3 to the left", "left"],
        "d" : ["Turn the GoPiGo3 to the right", "right"],
        "z" : ["Escape Left!", "escapeleft"],
        "c" : ["Escape Righct!", "escaperight"],
        "q" : ["SERPENTINE DESTRUCTION!!!", "serpentine"],
        "e" : ["Venomous Pounce!", "pounce"],
        "<SPACE>" : ["Stop the GoPiGo3 from moving", "stop"],

        "<F1>" : ["Drive forward for 10 centimeters", "forward10cm"],
        "<F2>" : ["Drive forward for 10 inches", "forward10in"],
        "<F3>" : ["Drive forward for 360 degrees (aka 1 wheel rotation)", "forwardturn"],

        "1" : ["Turn ON/OFF left blinker of the GoPiGo3", "leftblinker"],
        "2" : ["Turn ON/OFF right blinker of the GoPiGo3", "rightblinker"],
        "3" : ["Turn ON/OFF both blinkers of the GoPiGo3", "blinkers"],

        "8" : ["Turn ON/OFF left eye of the GoPiGo3", "lefteye"],
        "9" : ["Turn ON/OFF right eye of the GoPiGo3", "righteye"],
        "0" : ["Turn ON/OFF both eyes of the GoPiGo3", "eyes"],

        "<INSERT>" : ["Change the eyes' color on the go", "eyescolor"],

        "<ESC>" : ["Exit", "exit"],
        }
        self.order_of_keys = ["w", "s", "a", "d",  "z", "c", "q", "e", "<SPACE>", "<F1>", "<F2>", "<F3>", "1", "2", "3", "8", "9", "0", "<INSERT>", "<ESC>"]

    def executeKeyboardJob(self, argument):
        """
        Argument can be any of the strings stored in self.keybindings list.

        For instance: if argument is "w", then the algorithm looks inside self.keybinds dict and finds
        the "forward" value, which in turn calls the "_gopigo3_command_forward" method
        for driving the gopigo3 forward.

        The return values are:
        * "nothing" - when no method could be found for the given argument.
        * "moving" - when the robot has to move forward, backward, to the left or to the right for indefinite time.
        * "path" - when the robot has to move in a direction for a certain amount of time/distance.
        * "static" - when the robot doesn't move in any direction, but instead does static things, such as turning the LEDs ON.
        * "exit" - when the key for exiting the program is pressed.
        """
        method_prefix = "_gopigo3_command_"
        try:
            method_suffix = str(self.keybindings[argument][self.KEY_FUNC_SUFFIX])
        except KeyError:
            method_suffix = ""
        method_name = method_prefix + method_suffix

        method = getattr(self, method_name, lambda : "nothing")

        return method()

    def drawLogo(self):
        """
        Draws the name of the GoPiGo3.
        """
        print("   _____       _____ _  _____         ____  ")
        print("  / ____|     |  __ (_)/ ____|       |___ \ ")
        print(" | |  __  ___ | |__) || |  __  ___     __) |")
        print(" | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < ")
        print(" | |__| | (_) | |   | | |__| | (_) |  ___) |")
        print("  \_____|\___/|_|   |_|\_____|\___/  |____/ ")
        print("                                            ")

    def drawDescription(self):
        """
        Prints details related on how to operate the GoPiGo3.
        """
        print("\nPress the following keys to run the features of the GoPiGo3.")
        print("To move the motors, make sure you have a fresh set of batteries powering the GoPiGo3.\n")

    def drawMenu(self):
        """
        Prints all the key-bindings between the keys and the GoPiGo3's commands on the screen.
        """
        try:
            for key in self.order_of_keys:
                print("\r[key {:8}] :  {}".format(key, self.keybindings[key][self.KEY_DESCRIPTION]))
        except KeyError:
            print("Error: Keys found GoPiGo3WithKeyboard.order_of_keys don't match with those in GoPiGo3WithKeyboard.keybindings.")

    def _gopigo3_command_forward(self):
        self.gopigo3.set_speed(self.BASESPEED)
        self.gopigo3.forward()

        return "moving"

    def _gopigo3_command_backward(self):
        self.gopigo3.set_speed(self.BASESPEED)
        self.gopigo3.backward()

        return "moving"

    def _gopigo3_command_left(self):
        self.gopigo3.set_speed(self.BASESPEEDTURN)
        #self.gopigo3.left()
        self.gopigo3.steer(-100, 100)
        
        return "moving"

    def _gopigo3_command_right(self):
        self.gopigo3.set_speed(self.BASESPEEDTURN)
        #self.gopigo3.right()
        self.gopigo3.steer(100, -100)
        
        return "moving"

    def _gopigo3_command_stop(self):
        self.gopigo3.stop()

        return "moving"

    def _gopigo3_command_forward10cm(self):
        self.gopigo3.drive_cm(10)

        return "path"

    def _gopigo3_command_forward10in(self):
        self.gopigo3.drive_inches(10)

        return "path"

    def _gopigo3_command_forwardturn(self):
        self.gopigo3.drive_degrees(360)

        return "path"

    def _gopigo3_command_leftblinker(self):
        if self.left_blinker_on is False:
            self.gopigo3.led_on(1)
            self.left_blinker_on = True
        else:
            self.gopigo3.led_off(1)
            self.left_blinker_on = False

        return "static"

    def _gopigo3_command_rightblinker(self):
        if self.right_blinker_on is False:
            self.gopigo3.led_on(0)
            self.right_blinker_on = True
        else:
            self.gopigo3.led_off(0)
            self.right_blinker_on = False

        return "static"

    def _gopigo3_command_blinkers(self):
        if self.left_blinker_on is False and self.right_blinker_on is False:
            self.gopigo3.led_on(0)
            self.gopigo3.led_on(1)
            self.left_blinker_on = self.right_blinker_on = True
        else:
            self.gopigo3.led_off(0)
            self.gopigo3.led_off(1)
            self.left_blinker_on = self.right_blinker_on = False

        return "static"

    def _gopigo3_command_lefteye(self):
        if self.left_eye_on is False:
            self.gopigo3.open_left_eye()
            self.left_eye_on = True
        else:
            self.gopigo3.close_left_eye()
            self.left_eye_on = False

        return "static"

    def _gopigo3_command_righteye(self):
        if self.right_eye_on is False:
            self.gopigo3.open_right_eye()
            self.right_eye_on = True
        else:
            self.gopigo3.close_right_eye()
            self.right_eye_on = False

        return "static"

    def _gopigo3_command_eyes(self):
        if self.left_eye_on is False and self.right_eye_on is False:
            self.gopigo3.open_eyes()
            self.left_eye_on = self.right_eye_on = True
        else:
            self.gopigo3.close_eyes()
            self.left_eye_on = self.right_eye_on = False

        return "static"

    def _gopigo3_command_eyescolor(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        self.gopigo3.set_eye_color((red, green, blue))
        if self.left_eye_on is True:
            self.gopigo3.open_left_eye()
        if self.right_eye_on is True:
            self.gopigo3.open_right_eye()

        return "static"

    #DRY principle! used for keeping track of driving state through color
    def lightOn(self):
        self.gopigo3.open_eyes()
        self.EYES_ON = True
    def lightOff(self):
        self.gopigo3.close_eyes()
        self.EYES_ON = False
    def lightFlash(self):
        if (self.EYES_ON):
            self.gopigo3.close_eyes()
            self.EYES_ON = False
        else:
            self.gopigo3.open_eyes()
            self.EYES_ON = True
    def lightColor(self, color):
        self.gopigo3.set_eye_color(color)
        self.lightOn()
        
    def _gopigo3_command_exit(self):
        self.lightOff()
        return "exit"
    
    def _gopigo3_command_serpentine(self):

    
        self.gopigo3.set_speed(500)
        
        self.lightColor((255,0,0))
        self.gopigo3.steer(0, 100)
        sleep(0.2)
        self.lightColor((255,255,0))
        self.gopigo3.steer(100, 0)
        #sleep(0.4)
        
        counter = 0
        while (counter < 8):
            self.lightColor((random.randint(0,255), random.randint(0,255),random.randint(0,255)))
            sleep (0.05)
            counter += 1
        
        self.lightColor((255,0,0))
        self.gopigo3.steer(0, 100)
        sleep(0.2)
        
        self.gopigo3.set_speed(300)
        self.gopigo3.steer(100, 100)
        return "moving"
    
    def _gopigo3_command_pounce(self):
        self.gopigo3.set_speed(100)
        self.gopigo3.steer(-100, -100)
        
        counter = 0
        while (counter < 6):
            self.lightColor((random.randint(0,255), random.randint(0,255),random.randint(0,255)))
            sleep (0.05)
            counter += 1
        self.gopigo3.set_speed(10000)
        self.gopigo3.steer(100, 100)
        return "moving"
    
    def _gopigo3_command_escapeleft(self):
        self.gopigo3.set_speed(self.BASESPEED)
        self.gopigo3.steer(-10, -100)
        #print("running left")
        #sleep(1)
        return "moving"
    
    def _gopigo3_command_escaperight(self):
        self.gopigo3.set_speed(self.BASESPEED)
        self.gopigo3.steer(-100, -10)
        #print("running right")
        #sleep(1)
        return "moving"
