#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: direct_cli_execute
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of directly executed command on command line ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import subprocess


class CliExecuteCommands():
    """Class to contains taking notes process with simply if-else struct.
    """

    def compare(self, h, userin, user_answering):
        """Method to ava's command structures of directly executed command for open the programs on command line ability

        Args:
            h:                         doc helper from __init__.py
            userin:                    :class:`ava.utilities.TextToAction` instance.
        """
        # Input OPEN || CLOSE
        is_kill = False
        if h.check_verb_lemma("open") or h.check_adj_lemma("open") or h.check_verb_lemma("run") or h.check_verb_lemma("start") or h.check_verb_lemma("show") or h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop") or h.check_verb_lemma("remove"):
            if h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop") or h.check_verb_lemma("remove"):  # check for filter to program closing command
                is_kill = True
            if not is_kill:  # following lines created for differences about opening and closing commands.
                # Input: OFFICE SUITE AND WEB BROWSER
                if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                    cmds = [{'distro': 'All', 'name': ["sensible-browser"]}]
                    return userin.say(userin.execute(cmds, "Web Browser", False, 0, is_kill, user_answering))
                if h.check_noun_lemma("office") and h.check_noun_lemma("suite"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice", False, 0, is_kill, user_answering))
                if h.check_text("draw"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--draw"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Draw", False, 0, is_kill, user_answering))
                if h.check_text("impress"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--impress"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Impress", False, 0, is_kill, user_answering))
                if h.check_text("math"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--math"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Math", False, 0, is_kill, user_answering))
                if h.check_text("writer"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--writer"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Writer", False, 0, is_kill, user_answering))
            else:
                if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                    # THESE LINES SPECIAL FOR DETECTING AND KILLING DEFAULT BROWSER.
                    browser_killer_cmds = ["firefox", "chromium-browse", "chrome", "opera", "safari"]
                    raw_result = subprocess.check_output(['xdg-settings', 'get', 'default-web-browser'], stderr=subprocess.DEVNULL)
                    default_browser = raw_result.decode().strip().split(".")[0]
                    cmds = [{'distro': 'All', 'name': []}]
                    for killer in browser_killer_cmds:
                        if killer in default_browser:
                            for cmd in cmds:
                                cmd['name'] = [default_browser]
                    return userin.say(userin.execute(cmds, "Web Browser", False, 0, is_kill))
                if h.check_text("draw") or h.check_text("impress") or h.check_text("math") or h.check_text("writer") or (h.check_noun_lemma("office") and h.check_noun_lemma("suite")):
                    cmds = [{'distro': 'All', 'name': ['soffice.bin']}]
                    return userin.say(userin.execute(cmds, "LibreOffice", False, 0, is_kill))

            # Input: CAMERA, CALENDAR, CALCULATOR, STEAM, BLENDER, TERMINAL, FILE MANAGER
            if h.check_noun_lemma("camera"):
                cmds = [{'distro': 'KDE neon', 'name': ['kamoso']},
                        {'distro': 'elementary OS', 'name': ['snap-photobooth']},
                        {'distro': 'Ubuntu', 'name': ['cheese']}]
                return userin.say(userin.execute(cmds, "Camera", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("calendar"):
                cmds = [{'distro': 'KDE neon', 'name': ['korganizer']},
                        {'distro': 'elementary OS', 'name': ['maya-calendar']},
                        {'distro': 'Ubuntu', 'name': ['orage']},
                        {'distro': 'Linux Mint', 'name': ['gnome-calendar']}]
                return userin.say(userin.execute(cmds, "Calendar", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("calculator"):
                cmds = [{'distro': 'KDE neon', 'name': ['kcalc']},
                        {'distro': 'elementary OS', 'name': ['pantheon-calculator']},
                        {'distro': 'Ubuntu', 'name': ['gnome-calculator']}]
                return userin.say(userin.execute(cmds, "Calculator", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("console"):  # for openin terminal.
                cmds = [{'distro': 'KDE neon', 'name': ['konsole']},
                        {'distro': 'Ubuntu', 'name': ['gnome-terminal']}]
                return userin.say(userin.execute(cmds, "Terminal", False, 0, is_kill, user_answering))
            if h.check_text("blender"):
                cmds = [{'distro': 'All', 'name': ['blender']}]
                return userin.say(userin.execute(cmds, "3D computer graphics software", False, 0, is_kill, user_answering))
            if h.check_text("steam"):
                cmds = [{'distro': 'All', 'name': ['steam']}]
                return userin.say(userin.execute(cmds, "Steam Game Store", False, 0, is_kill, user_answering))
            if h.check_text("files"):
                cmds = [{'distro': 'KDE neon', 'name': ['dolphin']},
                        {'distro': 'Ubuntu', 'name': ['nautilus']},
                        {'distro': 'Linux Mint', 'name': ['nemo']},
                        {'distro': 'elementary OS', 'name': ['pantheon-files']}]
                return userin.say(userin.execute(cmds, "File Manager", False, 0, is_kill, user_answering))

        # Input: GIMP | PHOTOSHOP | PHOTO EDITOR
        if h.check_text("gimp") or (h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
            cmds = [{'distro': 'All', 'name': ['gimp']}]
            return userin.say(userin.execute(cmds, "The photo editor software", False, 0, is_kill, user_answering))

        # Input: INKSCAPE | VECTOR GRAPHICS
        if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (h.check_text("vectorial") and h.check_text("drawing")):
            cmds = [{'distro': 'All', 'name': ['inkscape']}]
            return userin.say(userin.execute(cmds, "The vectorial drawing software", False, 0, is_kill, user_answering))

        # Input: Kdenlive | VIDEO EDITOR
        if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
            cmds = [{'distro': 'All', 'name': ['kdenlive']}]
            return userin.say(userin.execute(cmds, "The video editor software", False, 0, is_kill, user_answering))

        # Input FILE MANAGER | FILE EXPLORER
        if h.check_noun_lemma("file") and (h.check_noun_lemma("manager") or h.check_noun_lemma("explorer")):
            cmds = [{'distro': 'KDE neon', 'name': ['dolphin']},
                    {'distro': 'Ubuntu', 'name': ['nautilus']},
                    {'distro': 'Linux Mint', 'name': ['nemo']},
                    {'distro': 'elementary OS', 'name': ['pantheon-files']}]
            return userin.say(userin.execute(cmds, "File Manager", False, 0, is_kill, user_answering))

        # Input: SOFTWARE CENTER
        if h.check_noun_lemma("software") and (h.check_text("center") or h.check_text("manager")):
            cmds = [{'distro': 'KDE neon', 'name': ['plasma-discover']},
                    {'distro': 'Ubuntu', 'name': ['software-center']},
                    {'distro': 'Linux Mint', 'name': ['mintinstall']},
                    {'distro': 'elementary OS', 'name': ['software-center']}]
            return userin.say(userin.execute(cmds, "Software Center", False, 0, is_kill, user_answering))
        return None
