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

    def first_compare(self, h, userin):
        """Method to dragonfire's command structures of directly executed command for open the programs on command line ability

        Args:
            h:                         doc helper from __init__.py
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
        """

        if h.check_verb_lemma("open") or h.check_adj_lemma("open") or h.check_verb_lemma("run") or h.check_verb_lemma("start") or h.check_verb_lemma("show"):
            if h.check_text("blender"):
                userin.execute(["blender"], "Blender")
                return userin.say("Blender 3D computer graphics software")
            if h.check_text("draw"):
                userin.execute(["libreoffice", "--draw"], "LibreOffice Draw")
                return userin.say("Opening LibreOffice Draw")
            if h.check_text("impress"):
                userin.execute(["libreoffice", "--impress"], "LibreOffice Impress")
                return userin.say("Opening LibreOffice Impress")
            if h.check_text("math"):
                userin.execute(["libreoffice", "--math"], "LibreOffice Math")
                return userin.say("Opening LibreOffice Math")
            if h.check_text("writer"):
                userin.execute(["libreoffice", "--writer"], "LibreOffice Writer")
                return userin.say("Opening LibreOffice Writer")
            if h.check_text("gimp") or (
                    h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
                userin.execute(["gimp"], "GIMP")
                return userin.say("Opening the photo editor software.")
            if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (
                    h.check_text("vectorial") and h.check_text("drawing")):
                userin.execute(["inkscape"], "Inkscape")
                return userin.say("Opening the vectorial drawing software.")
            if h.check_noun_lemma("office") and h.check_noun_lemma("suite"):
                userin.execute(["libreoffice"], "LibreOffice")
                return userin.say("Opening LibreOffice")
            if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
                userin.execute(["kdenlive"], "Kdenlive")
                return userin.say("Opening the video editor software.")
            if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                userin.execute(["sensible-browser"], "Web Browser")
                return userin.say("Web browser")
            if h.check_text("steam"):
                userin.execute(["steam"], "Steam")
                return userin.say("Opening Steam Game Store")
            if h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
                userin.execute(["dolphin"], "File Manager")  # KDE neon
                userin.execute(["pantheon-files"], "File Manager")  # elementary OS
                userin.execute(["nautilus", "--browser"], "File Manager")  # Ubuntu
                userin.execute(["nemo"], "File Manager")  # Linux Mint
                return userin.say("File Manager")
            if h.check_noun_lemma("camera"):
                userin.execute(["kamoso"], "Camera")  # KDE neon
                userin.execute(["snap-photobooth"], "Camera")  # elementary OS
                userin.execute(["cheese"], "Camera")  # Ubuntu
                return userin.say("Camera")
            if h.check_noun_lemma("calendar"):
                userin.execute(["korganizer"], "Calendar")  # KDE neon
                userin.execute(["maya-calendar"], "Calendar")  # elementary OS
                userin.execute(["orage"], "Calendar")  # Ubuntu
                userin.execute(["gnome-calendar"], "Calendar")  # Ubuntu & Linux Mint
                return userin.say("Calendar")
            if h.check_noun_lemma("calculator"):
                userin.execute(["kcalc"], "Calculator")  # KDE neon
                userin.execute(["pantheon-calculator"], "Calculator")  # elementary OS
                userin.execute(["gnome-calculator"], "Calculator")  # Ubuntu
                return userin.say("Calculator")
            if h.check_noun_lemma("software") and (h.check_text("center") or h.check_text("manager")):
                userin.execute(["plasma-discover"], "Software Center")  # KDE neon
                userin.execute(["software-center"], "Software Center")  # elementary OS & Ubuntu
                userin.execute(["mintinstall"], "Software Manager")  # Linux Mint
                return userin.say("Software Center")
            if h.check_noun_lemma("console"):  # for openin terminal.
                userin.execute(["konsole"], "Terminal")  # KDE neon
                userin.execute(["gnome-terminal"], "Terminal")  # elementary OS & Ubuntu
                return userin.say("console")
        return None

    def second_compare(self, h, userin):
        """Method to dragonfire's command structures of directly executed command for close the open programs on command line ability

        Args:
            h:                         doc helper from __init__.py
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
        """

        if h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop"):
            if h.check_text("blender"):
                """
                blender:                 For All
                """
                cmds = [["blender"]]
                return self.executes(cmds, "Blender", userin)

            if h.check_text("draw") or h.check_text("impress") or h.check_text("math") or h.check_text("writer") or (h.check_noun_lemma("office") and h.check_noun_lemma("suite")):
                """
                soffice.bin:                   For All LibreOffice Process
                """
                cmds = [["soffice.bin"]]
                return self.executes(cmds, "LibreOffice", userin)

            if h.check_text("gimp") or (h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
                """
                gimp:                   For All
                """
                cmds = [["gimp"]]
                return self.executes(cmds, "Gimp", userin)

            if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (h.check_text("vectorial") and h.check_text("drawing")):
                """
                gimp:                   For All
                """
                cmds = [["inkscape"]]
                return self.executes(cmds, "Inkscape", userin)

            if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
                """
                kdenlive:               For All
                """
                cmds = [["kdenlive"]]
                return self.executes(cmds, "Kdenlive", userin)

            if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                """ All of them for all OS
                firefox:
                chromium:
                chrome:
                opera:
                safari:
                """
                cmds = [["firefox"], ["chromium"], ["chrome"], ["opera"], ["safari"]]
                return self.executes(cmds, "Browser", userin)

            if h.check_text("steam"):
                """
                steam:                  For All
                """
                cmds = [["steam"]]
                return self.executes(cmds, "Steam", userin)

            if h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
                """
                dolphin:                For KDE neon
                pantheon-files  :       For elementary OS
                nautilus:               For ubuntu
                nemo:                   For Linux Mint
                """
                cmds = [["dolphin"], ["pantheon-files"], ["nautilus"], ["nemo"]]
                return self.executes(cmds, "File Manager", userin)

            if h.check_noun_lemma("camera"):
                """
                kamoso:                 For KDE neon
                snap-photobooth:        For elementary OS
                cheese:                 For ubuntu
                """
                cmds = [["kamoso"], ["snap-photobooth"], ["cheese"]]
                return self.executes(cmds, "Camera", userin)

            if h.check_noun_lemma("calendar"):
                """
                korganizer:             For KDE neon
                maya-calendar:          For elementary OS
                orage:                  For ubuntu
                gnome-calendar:         For ubuntu & Linux Mint
                """
                cmds = [["korganizer"], ["maya-calendar"], ["orage"], ["gnome-calendar"]]
                return self.executes(cmds, "Calendar", userin)

            if h.check_noun_lemma("calculator"):
                """
                kcalc:                  For KDE neon
                pantheon-calculator:    For elementary OS
                gnome-calculator:       For Ubuntu
                """
                cmds = [["kcalc"], ["pantheon-calculator"], ["gnome-calculator"]]
                return self.executes(cmds, "Calculator", userin)

            if h.check_noun_lemma("software") and (h.check_text("center") or h.check_text("manager")):
                """
                plasma-discover:        For KDE neon
                software-center:        For elementary OS & Ubuntu
                mintinstall:            For Linux Mint
                """
                cmds = [["plasma-discover"], ["software-center"], ["mintinstall"]]
                return self.executes(cmds, "Software Center", userin)

            if h.check_noun_lemma("console"):  # for openin terminal.
                """
                konsole:               For KDE neon
                gnome-terminal:        For elementary OS & Ubuntu
                """
                cmds = [["konsole"], ["gnome-terminal"]]
                return self.executes(cmds, "Console", userin)
        return None

    def executes(self, cmds, msg, userin):
        closed_msg = msg + " is not open"  # if there is more than one program exist for the same job in local, this will keep.
        for a in cmds:
            response = userin.execute(a, msg, False, 0, True)  # KDE neon
            if response == msg + " closed":
                closed_msg = response
        return userin.say(closed_msg)
