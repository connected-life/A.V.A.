#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: t_system
    :platform: Unix
    :synopsis: the top-level submodule of A.V.A.'s.augmented that contains the classes related to A.V.A.'s simple if-else struct of Augmented abilities.

.. moduleauthors:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import time
from multiprocessing import Process
from random import choice

import youtube_dl  # Command-line program to download videos from YouTube.com and other video sites
from pykeyboard import PyKeyboard   # A simple, cross-platform Python module for providing keyboard control

from ava.utilities import nostdout, nostderr  # Submodule of Dragonfire to provide various utilities


def check(doc, h, mqtt_receimitter, user_answering, userin, user_prefix):
    """Method to ava's command structures of controlling ability of remote object tracking system.

    Args:
        doc:                       doc of com from __init__.py
        h:                         doc helper from __init__.py
        mqtt_receimitter:          transmit and receive data function for mqtt communication
        user_answering:            User answering string array.
        userin:                    :class:`ava.utilities.TextToAction` instance.

    Keyword Args:
        user_prefix:               user's preferred titles.
    """
    # If the user has an option for running commands, the following lines will catch the options from the user's answer.
    if user_answering['status'] and user_answering['for'] == 'augmented':
        if h.check_text("whatever") or (h.check_text("give") and h.check_text("up")) or (h.check_text("not") and h.check_text("now")) or (h.check_text("forget") and h.check_text("it")):  # for writing interrupt while taking notes and creating reminders.
            user_answering['status'] = False
            return userin.say(choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([".", ", " + user_prefix + "."]))
        if user_answering['reason'] == 'activate':
            user_answering['status'] = False
            if h.check_text("yes") or (h.check_text("do") and h.check_text("it")) or h.check_text("yep") or h.check_text("okay"):
                activate(mqtt_receimitter, userin, user_prefix)
                if user_answering['options'] == 'tracking':
                    userin.say("Activating tracking mode.")
                    flag = {'msg': {'command': 'change_mode', 'options': 'learn'}, 'system_name': 'Tracking Mode'}
                    return change_mode(mqtt_receimitter, flag, userin, user_prefix)

                if user_answering['options'] == 'security':
                    userin.say("Activating security mode.")
                    flag = {'msg': {'command': 'change_mode', 'options': 'security'}, 'system_name': 'Security Mode'}
                    return change_mode(mqtt_receimitter, flag, userin, user_prefix)

                if user_answering['options'] == 'learning':
                    userin.say("Activating learning mode.")
                    flag = {'msg': {'command': 'change_mode', 'options': 'learn'}, 'system_name': 'Learning Mode'}
                    return change_mode(mqtt_receimitter, flag, userin, user_prefix)
            else:
                return userin.say("I won't connect" + choice([".", ", " + user_prefix + "."]))
    if (h.check_verb_lemma("activate") or h.check_verb_lemma("start") or h.check_verb_lemma("connect")) and (h.check_text("tracking") and h.check_text("system")):
        return activate(mqtt_receimitter, userin, user_prefix)

    if h.check_verb_lemma("activate") or h.check_verb_lemma("start") or h.check_verb_lemma("run"):
        if h.check_text("tracking") and h.check_text("mode"):
            check = connection_check(mqtt_receimitter, 'augmented', 'activate', 'tracking', user_answering, userin, user_prefix)
            if check:
                return check
            flag = {'msg': {'command': 'change_mode', 'options': 'track'}, 'system_name': 'Tracking Mode'}
            return change_mode(mqtt_receimitter, flag, userin, user_prefix)

        if h.check_text("security") and h.check_text("mode"):
            check = connection_check(mqtt_receimitter, 'augmented', 'activate', 'security', user_answering, userin, user_prefix)
            if check:
                return check
            flag = {'msg': {'command': 'change_mode', 'options': 'security'}, 'system_name': 'Security Mode'}
            return change_mode(mqtt_receimitter, flag, userin, user_prefix)

        if h.check_text("learning") and h.check_text("mode"):
            check = connection_check(mqtt_receimitter, 'augmented', 'activate', 'learning', user_answering, userin, user_prefix)
            if check:
                return check
            flag = {'msg': {'command': 'change_mode', 'options': 'learn'}, 'system_name': 'Learning Mode'}
            return change_mode(mqtt_receimitter, flag, userin, user_prefix)
    if h.check_verb_lemma("watch") or h.check_verb_lemma("track") or h.check_verb_lemma("follow"):
        thing = ""
        for token in doc:
            if not (
                    token.lemma_ == "watch" or token.lemma_ == "track" or token.lemma_ == "follow" or token.is_stop):
                thing += ' ' + token.text
        thing = thing.strip()
        if thing:
            flag = {'command': 'change_target', 'options': thing}
            return change_tracking_thing(mqtt_receimitter, flag, userin, user_prefix)

    return None


def change_tracking_thing(mqtt_receimitter, flag, userin, user_prefix):
    """Method to change tracking object for ava's controlling ability of remote object tracking system.

    Args:
        mqtt_receimitter:          transmit and receive data function for mqtt communication
        flag:                      The object, which will been tracking via remote object tracking system
        userin:                    :class:`ava.utilities.TextToAction` instance.

    Keyword Args:
        user_prefix:               user's preferred titles.
    """

    mqtt_receimitter.publish('Augmented/T_System', flag)
    time.sleep(5)  # some check for waiting the result code will be here.

    msg = mqtt_receimitter.get_incoming_message()
    if not msg == {}:
        if msg['options'] == 'realized':
            return userin.say("System started the " + choice(["watching ", "tracking " + "following"]) + "for" + flag['options'])

        elif msg['options'] == 'already_tracking':
            return userin.say("System already running on " + flag['options'] + choice([".", ", " + user_prefix + "."]))

        else:
            return userin.say("Changing of tracking thing is failed!")
    else:
        return userin.say("Communication failed" + choice(["!", ", " + user_prefix + "!"]))


def change_mode(mqtt_receimitter, flag, userin, user_prefix):
    """Method to change working mode for ava's controlling ability of remote object tracking system.

    Args:
        mqtt_receimitter:          transmit and receive data function for mqtt communication
        flag(dictionary):          flag of mode.
        userin:                    :class:`ava.utilities.TextToAction` instance.

    Keyword Args:
        user_prefix:               user's preferred titles.
    """
    mqtt_receimitter.publish('Augmented/T_System', flag['msg'])
    time.sleep(1)  # some check for waiting the result code will be here.

    msg = mqtt_receimitter.get_incoming_message()
    if not msg == {}:
        if msg['options'] == 'realized':
            return userin.say("The Object Tracking System is running on " + flag['system_name'] + choice([".", ", " + user_prefix + "."]))

        elif msg['options'] == 'already_running':
            return userin.say("System already running on " + flag['system_name'] + choice([".", ", " + user_prefix + "."]))

        else:
            return userin.say(flag['system_name'] + " activation is failed!")
    else:
        return userin.say("Communication failed" + choice(["!", ", " + user_prefix + "!"]))


def activate(mqtt_receimitter, userin, user_prefix):
    """Method to activating mqtt connection for ava's controlling ability of remote object tracking system.

    Args:
        mqtt_receimitter:          transmit and receive data function for mqtt communication
        userin:                    :class:`ava.utilities.TextToAction` instance.

    Keyword Args:
        user_prefix:               user's preferred titles.
    """
    mqtt_proc = Process(target=mqtt_receimitter.subscribe('T_System/Augmented'))
    mqtt_proc.start()

    while not mqtt_receimitter.get_is_connected():
        pass

    return userin.say("Connection established!")


def connection_check(mqtt_receimitter, forr, reason, options, user_answering, userin, user_prefix):
    """Method to checking the connection of mqtt communication for ava's controlling ability of remote object tracking system.

    Args:
        mqtt_receimitter:          transmit and receive data function for mqtt communication
        user_answering:            User answering string array.
        userin:                    :class:`ava.utilities.TextToAction` instance.



    Keyword Args:
        forr:                      purpose of the user's answer.
        reason:                    reason of the user's answer.
        options:                   options of the user's answer.
        user_prefix:               user's preferred titles.
    """
    if not mqtt_receimitter.get_is_connected():
        user_answering['status'] = True
        user_answering['for'] = forr
        user_answering['reason'] = reason
        user_answering['options'] = options
        return userin.say("Object Tracking System is not Active. You want me to activate?")
    return None
