#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: direct_cli_execute
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of directly executed command on command line ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""


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
        if h.check_verb_lemma("open") or h.check_adj_lemma("open") or h.check_verb_lemma("run") or h.check_verb_lemma("start") or h.check_verb_lemma("show") or h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop"):
            is_kill = False
            if h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop"):  # check for filter to program closing command
                is_kill = True
                # Input: OFFICE SUITE AND WEB BROWSER
            if not is_kill:  # following lines created for differences about opening and closing commands.
                if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                    cmds = [["sensible-browser"]]
                    return userin.say(userin.execute(cmds, "Web Browser", user_answering))
                if h.check_noun_lemma("office") and h.check_noun_lemma("suite"):
                    cmds = [["libreoffice"]]
                    return userin.say(userin.execute(cmds, "LibreOffice", user_answering))
                if h.check_text("draw"):
                    cmds = [["libreoffice", "--draw"]]
                    return userin.say(userin.execute(cmds, "LibreOffice Draw", user_answering))
                if h.check_text("impress"):
                    cmds = [["libreoffice", "--impress"]]
                    return userin.say(userin.execute(cmds, "LibreOffice Impress", user_answering))
                if h.check_text("math"):
                    cmds = [["libreoffice", "--math"]]
                    return userin.say(userin.execute(cmds, "LibreOffice Math", user_answering))
                if h.check_text("writer"):
                    cmds = [["libreoffice", "--writer"]]
                    return userin.say(userin.execute(cmds, "LibreOffice Writer", user_answering))
            else:
                if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                    """ All of them for all OS
                    firefox:
                    chromium:
                    chrome:
                    opera:
                    safari:
                    """
                    cmds = [["firefox"], ["chromium-browse"], ["chrome"], ["opera"], ["safari"]]
                    return userin.say(userin.execute(cmds, "Web Browser", False, 0, is_kill))
                if h.check_text("draw") or h.check_text("impress") or h.check_text("math") or h.check_text("writer") or (h.check_noun_lemma("office") and h.check_noun_lemma("suite")):
                    """
                    soffice.bin:                   For All LibreOffice Process
                    """
                    cmds = [["soffice.bin"]]
                    return userin.say(userin.execute(cmds, "LibreOffice", False, 0, is_kill))
            # Input: CAMERA, CALENDAR, CALCULATOR, STEAM, BLENDER, TERMINAL
            if h.check_noun_lemma("camera"):
                """
                kamoso:                 For KDE neon
                snap-photobooth:        For elementary OS
                cheese:                 For ubuntu
                """
                cmds = [["kamoso"], ["snap-photobooth"], ["cheese"]]
                return userin.say(userin.execute(cmds, "Camera", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("calendar"):
                """
                korganizer:             For KDE neon
                maya-calendar:          For elementary OS
                orage:                  For ubuntu
                gnome-calendar:         For ubuntu & Linux Mint
                """
                cmds = [["korganizer"], ["maya-calendar"], ["orage"], ["gnome-calendar"]]
                return userin.say(userin.execute(cmds, "Calendar", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("calculator"):
                """
                kcalc:                  For KDE neon
                pantheon-calculator:    For elementary OS
                gnome-calculator:       For Ubuntu
                """
                cmds = [["kcalc"], ["pantheon-calculator"], ["gnome-calculator"]]
                return userin.say(userin.execute(cmds, "Calculator", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("console"):  # for openin terminal.
                """
                konsole:               For KDE neon
                gnome-terminal:        For elementary OS & Ubuntu
                """
                cmds = [["konsole"], ["gnome-terminal"]]
                return userin.say(userin.execute(cmds, "Terminal", False, 0, is_kill, user_answering))
            if h.check_text("blender"):
                """
                blender:                 For All
                """
                cmds = [["blender"]]
                return userin.say(userin.execute(cmds, "3D computer graphics software", False, 0, is_kill, user_answering))
            if h.check_text("steam"):
                """
                steam:                  For All
                """
                cmds = [["steam"]]
                return userin.say(userin.execute(cmds, "Steam Game Store", False, 0, is_kill, user_answering))
            # Input: GIMP | PHOTOSHOP | PHOTO EDITOR
            if h.check_text("gimp") or (h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
                """
                gimp:                   For All
                """
                cmds = [["gimp"]]
                return userin.say(userin.execute(cmds, "The photo editor software", False, 0, is_kill, user_answering))
            # Input: INKSCAPE | VECTOR GRAPHICS
            if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (h.check_text("vectorial") and h.check_text("drawing")):
                """
                gimp:                   For All
                """
                cmds = [["inkscape"]]
                return userin.say(userin.execute(cmds, "The vectorial drawing software", False, 0, is_kill, user_answering))
            # Input: Kdenlive | VIDEO EDITOR
            if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
                """
                kdenlive:               For All
                """
                cmds = [["kdenlive"]]
                return userin.say(userin.execute(cmds, "The video editor software", False, 0, is_kill, user_answering))
            # Input FILE MANAGER | FILE EXPLORER
            if h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
                """
                dolphin:                For KDE neon
                pantheon-files  :       For elementary OS
                nautilus:               For ubuntu
                nemo:                   For Linux Mint
                """
                cmds = [["dolphin"], ["pantheon-files"], ["nautilus"], ["nemo"]]
                return userin.say(userin.execute(cmds, "File Manager", False, 0, is_kill, user_answering))

            # Input: SOFTWARE CENTER
            if h.check_noun_lemma("software") and (h.check_text("center") or h.check_text("manager")):
                """
                plasma-discover:        For KDE neon
                software-center:        For elementary OS & Ubuntu
                mintinstall:            For Linux Mint
                """
                cmds = [["plasma-discover"], ["software-center"], ["mintinstall"]]
                return userin.say(userin.execute(cmds, "Software Center", False, 0, is_kill, user_answering))
        return None
