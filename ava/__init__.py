#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level module of Dragonfire that contains the entry point and handles built-in commands.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import argparse  # Parser for command-line options, arguments and sub-commands
import datetime  # Basic date and time types
import inspect  # Inspect live objects
import os  # Miscellaneous operating system interfaces
import subprocess  # Subprocess managements
import sys  # System-specific parameters and functions
try:
    import thread  # Low-level threading API (Python 2.7)
except ImportError:
    import _thread as thread  # Low-level threading API (Python 3.x)
import time  # Time access and conversions
import uuid  # UUID objects according to RFC 4122
from multiprocessing import Event, Process  # Process-based “threading” interface
from os.path import expanduser  # Common pathname manipulations
from random import choice  # Generate pseudo-random numbers
import shutil  # High-level file operations
import readline #GNU readline Interface

from ava.learn import Learner  # Submodule of Dragonfire that forms her learning ability
from ava.takenote import NoteTaker  # Submodule of Dragonfire that forms her taking note ability
from ava.reminder import Reminder  # Submodule of Dragonfire that forms her reminde note ability
from ava.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks
from ava.omniscient import Omniscient  # Submodule of Dragonfire that serves as a Question Answering Engine
from ava.stray import SystemTrayExitListenerSet, SystemTrayInit  # Submodule of Dragonfire for System Tray Icon related functionalities
from ava.utilities import TextToAction, nostdout, nostderr  # Submodule of Dragonfire to provide various utilities
from ava.arithmetic import arithmetic_parse  # Submodule of Dragonfire to analyze arithmetic expressions
from ava.deepconv import DeepConversation  # Submodule of Dragonfire to answer questions directly using an Artificial Neural Network
from ava.coref import NeuralCoref  # Submodule of Dragonfire that aims to create corefference based dialogs
from ava.config import Config  # Submodule of Dragonfire to store configurations
from ava.database import Base  # Submodule of Dragonfire module that contains the database schema

from ava.commands.takenote import TakeNoteCommand
from ava.commands.find_in_wikipedia import FindInWikiCommand
from ava.commands.direct_cli_execute import CliExecuteCommands
from ava.commands.find_in_youtube import FindInYoutubeCommand
from ava.commands.find_in_browser import FindInBrowserCommand
from ava.commands.keyboard import KeyboardCommands
from ava.commands.set_user_title import SetUserTitleCommands

import spacy  # Industrial-strength Natural Language Processing in Python
import pyowm  # A Python wrapper around the OpenWeatherMap API
from tinydb import Query, TinyDB  # TinyDB is a lightweight document oriented database optimized for your happiness
from sqlalchemy import create_engine  # the Python SQL toolkit and Object Relational Mapper
from sqlalchemy.orm import sessionmaker  # ORM submodule of SQLAlchemy


__version__ = '1.0.0'

DRAGONFIRE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
GENDER_PREFIX = {'male': 'Sir', 'female': 'My Lady'}
CONVERSATION_ID = uuid.uuid4()
userin = None
nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model
learner = Learner(nlp)
note_taker = NoteTaker()
reminder = Reminder()
omniscient = Omniscient(nlp)
dc = DeepConversation()
coref = NeuralCoref()
e = Event()

take_note_command = TakeNoteCommand()
find_in_wiki_command = FindInWikiCommand()
find_in_youtube_command = FindInYoutubeCommand()
find_in_browser_command = FindInBrowserCommand()
cli_execute_commands = CliExecuteCommands()
keyboard_commands = KeyboardCommands()
set_user_title_commands = SetUserTitleCommands()

USER_ANSWERING = {      # user answering for wikipedia search
    'status': False,
    'for': None,
    'reason': None,
    'options': None
}

USER_ANSWERING_NOTE = {     # user answering for taking notes.
    'status': False,
    'is_remind': False,
    'is_todo': False,          # using taking and getting notes both.
    'todo_listname': None,
    'todo_listcount': 0,
    'note_keeper': None,
    'has_listname': True,
    'is_again': False,
    'is_active': True     # for increasing reminder performans with checking this.
}

try:
    raw_input  # Python 2
except NameError:
    raw_input = input  # Python 3


def start(args, userin):
    """Function that starts the virtual assistant with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
        userin:     :class:`ava.utilities.TextToAction` instance.
    """

    if 'TRAVIS' in os.environ or args["db"] == "mysql":
        engine = create_engine('mysql+pymysql://' + Config.MYSQL_USER + ':' + Config.MYSQL_PASS + '@' + Config.MYSQL_HOST + '/' + Config.MYSQL_DB)
    else:
        engine = create_engine('sqlite:///ava.db', connect_args={'check_same_thread': False}, echo=True)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    learner.db_session = db_session

    if args["server"]:
        import ava.api as API  # API of Dragonfire
        import tweepy  # An easy-to-use Python library for accessing the Twitter API
        from tweepy import OAuthHandler
        from tweepy import Stream
        from ava.twitter import MentionListener

        if Config.TWITTER_CONSUMER_KEY != 'CONSUMER_KEY':
            auth = OAuthHandler(Config.TWITTER_CONSUMER_KEY, Config.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(Config.TWITTER_ACCESS_KEY, Config.TWITTER_ACCESS_SECRET)
            userin.twitter_api = tweepy.API(auth)

            print("Listening Twitter mentions...")
            l = MentionListener(args, userin)
            stream = Stream(auth, l)
            stream.filter(track=['DragonfireAI'], async=True)
        API.Run(nlp, learner, omniscient, dc, coref, userin, args["server"], args["port"], db_session)
    else:
        global user_full_name
        global user_prefix
        global ava_name
        if args["cli"]:
            her = VirtualAssistant(args, userin, user_full_name, user_prefix, ava_name)
            while (True):
                com = raw_input("Enter your command: ")
                thread.start_new_thread(her.command, (com,))
                time.sleep(0.5)
        elif args["gspeech"]:
            from ava.sr.gspeech import GspeechRecognizer

            her = VirtualAssistant(args, userin, user_full_name, user_prefix, ava_name)
            recognizer = GspeechRecognizer()
            recognizer.recognize(her)
        else:
            from ava.sr.deepspeech import DeepSpeechRecognizer

            her = VirtualAssistant(args, userin, user_full_name, user_prefix, ava_name)
            recognizer = DeepSpeechRecognizer()
            recognizer.recognize(her)


class VirtualAssistant():
    """Class to define a virtual assistant.

    This class provides necessary initiations and a function named :func:`ava.VirtualAssistant.command`
    as the entry point for each one of the user commands.

    .. note::

        This class is not used in the API.

    """

    def __init__(self, args, userin, user_full_name="John Doe", user_prefix="sir", ava_name="A.V.A.", tw_user=None, testing=False):
        """Initialization method of :class:`ava.VirtualAssistant` class.

        Args:
            args:       Command-line arguments.
            userin:     :class:`ava.utilities.TextToAction` instance.

        Keyword Args:
            user_full_name (str):       User's full name  to answer some basic questions
            user_prefix (str):          Prefix to address/call user when answering
            tw_user (str):              Twitter username of the person querying DragonfireAI Twitter account with a mention
        """

        self.args = args
        self.userin = userin
        self.user_full_name = user_full_name
        self.user_prefix = user_prefix
        self.ava_name = ava_name
        self.userin.twitter_user = tw_user
        self.testing = testing
        self.inactive = False
        if not self.args["server"]:
            self.inactive = True
        if self.testing:
            home = expanduser("~")
            self.config_file = TinyDB(home + '/.dragonfire_config.json')

        thread.start_new_thread(reminder.remind, (note_taker, userin, user_prefix, USER_ANSWERING_NOTE))

    def command(self, com):
        """Function that serves as the entry point for each one of the user commands.

        This function goes through these steps for each one of user's commands, respectively:

         - Search across the built-in commands via a simple if-else control flow.
         - Try to get a response from :func:`ava.arithmetic.arithmetic_parse` function.
         - Try to get a response from :func:`ava.learn.Learner.respond` method.
         - Try to get a answer from :func:`ava.omniscient.Omniscient.respond` method.
         - Try to get a response from :func:`ava.deepconv.DeepConversation.respond` method.

        Args:
            com (str):  User's command.

        Returns:
            str:  Response.
        """

        if not self.args["server"]:
            global config_file
            global e
            if (e.is_set()):  # System Tray Icon exit must trigger this
                exit(0)
        args = self.args
        userin = self.userin
        user_full_name = self.user_full_name
        user_prefix = self.user_prefix
        ava_name = self.ava_name
        if self.testing:
            config_file = self.config_file

        if isinstance(com, str) and com:
            com = com.strip()
        else:
            return False

        print("You: " + com.upper())
        doc = nlp(com)
        h = Helper(doc)

        if args["verbose"]:
            userin.pretty_print_nlp_parsing_results(doc)

        if self.inactive and not (h.directly_equal(["ava", "hey", ava_name]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up"))):
            return ""
        # if USER_ANSWERING['for'] == 'assistant_rename':
        #     config_file.update({'name': com}, Query().datatype == 'name')
        if USER_ANSWERING['status'] and USER_ANSWERING['for'] == 'execute':
            if h.check_text("whatever") or (h.check_text("give") and h.check_text("up")) or (h.check_text("not") and h.check_text("now")) or (h.check_text("forget") and h.check_text("it")):  # for writing interrupt while taking notes and creating reminders.
                USER_ANSWERING['status'] = False
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([".", ", " + user_prefix + "."]))
            if USER_ANSWERING['reason'] == 'install':
                USER_ANSWERING['status'] = False
                if h.check_text("yes") or (h.check_text("do") and h.check_text("it")) or h.check_text("yep") or h.check_text("okay"):
                    cmds = [{'distro': 'All', 'name': ["gksudo", "apt-get install " + USER_ANSWERING['options'][0]]}]
                    userin.say("Installing " + USER_ANSWERING['options'][1] + "...")
                    return userin.execute(cmds, "install**" + USER_ANSWERING['options'][1])
                else:
                    return userin.say("Okay, I won't install!")

        response = take_note_command.takenote_second_compare(com, doc, h, note_taker, USER_ANSWERING_NOTE, userin, user_prefix)   # take note command.
        if response:
            return response

        response = take_note_command.getnote_second_compare(com, h, note_taker, USER_ANSWERING_NOTE, userin, user_prefix)
        if response:
            return response

        response = find_in_wiki_command.second_compare(com, USER_ANSWERING, userin, user_prefix)
        if response:
            return response

        if h.directly_equal(["ava", "hey", ava_name]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up")):
            self.inactive = False
            return userin.say(choice([
                "Yes, " + user_prefix + ".",
                "Yes. I'm waiting.",
                "What is your order?",
                "Ready for the orders!",
                user_prefix.capitalize() + ", tell me your wish."
            ]))
        if (h.check_verb_lemma("go") and h.check_noun_lemma("sleep")) or (h.check_verb_lemma("stop") and h.check_verb_lemma("listen")) or h.directly_equal(["quiet"]):
            self.inactive = True
            cmds = [{'distro': 'All', 'name': ["echo"]}]
            userin.execute(cmds, ava_name + " deactivated. To reactivate say '" + ava_name + "' or 'Wake Up!'")
            return userin.say("I'm going to sleep")
        if h.directly_equal(["enough", "mute"]) or (h.check_verb_lemma("shut") and h.check_nth_lemma(-1, "up")):
            tts_kill()
            msg = ava_name + " quiets."
            print(msg)
            return msg
        if h.check_wh_lemma("what") and h.check_deps_contains("your name"):
            cmds = [{'distro': 'All', 'name': [" "]}]
            return userin.execute(cmds, "My name is " + ava_name + ".", True)
        if h.check_wh_lemma("what") and h.check_deps_contains("your gender"):
            return userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
        if (h.check_wh_lemma("who") and h.check_text("I")) or (h.check_verb_lemma("say") and h.check_text("my") and h.check_lemma("name")):
            cmds = [{'distro': 'All', 'name': [" "]}]
            userin.execute(cmds, user_full_name)
            return userin.say("Your name is " + user_full_name + ", " + user_prefix + ".")

        if (h.check_wh_lemma("what") and h.check_verb_lemma("be") and h.check_text("time")) or h.check_only_dep_is("time") or ((h.check_verb_lemma("give") or h.check_verb_lemma("tell")) and h.check_text("time")) or (
                h.check_wh_lemma("what") and h.check_noun_lemma("time") and h.check_verb_lemma("be") and h.check_text("it")):
            return userin.say(datetime.datetime.now().strftime("%H:%M") + choice([", "+user_prefix + ".", "."]))

        response = take_note_command.deletenote_(h, note_taker, userin)
        if response:
            return response

        response = take_note_command.getnote_first_compare(com, doc, h, note_taker, USER_ANSWERING_NOTE, userin, user_prefix)
        if response:
            return response

        response = cli_execute_commands.compare(h, userin, USER_ANSWERING)
        if response:
            return response

        response = take_note_command.takenote_first_compare(com, doc, h, note_taker, USER_ANSWERING_NOTE, userin, user_prefix)  # take note command
        if response:
            return response
        if ((h.check_verb_lemma("change") or h.check_verb_lemma("register")) and (h.check_text("your") and h.check_noun_lemma("name"))) or (h.check_text("your") and h.check_noun_lemma("name") and h.check_verb_lemma("be") and h.check_text("now")):
            response = com.replace("change your name ", "")
            response = response.replace("register your name ", "")
            response = response.replace("your name is now ", "")
            if not response == "":
                config_file.update({'name': response}, Query().datatype == 'name')
                self.ava_name = response
                return userin.say("From now on my name is " + response + ".")

        response = set_user_title_commands.compare(doc, h, args, userin, config_file)
        if response:
            return response

        if h.is_wh_question() and h.check_lemma("temperature"):
            city = ""
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    city += ' ' + ent.text
            city = city.strip()
            if city:
                cmds = [{'distro': 'All', 'name': [" "]}]
                owm = pyowm.OWM("16d66c84e82424f0f8e62c3e3b27b574")
                reg = owm.city_id_registry()
                try:
                    weather = owm.weather_at_id(reg.ids_for(city)[0][0]).get_weather()
                    fmt = "The temperature in {} is {} degrees celsius"
                    msg = fmt.format(city, weather.get_temperature('celsius')['temp'])
                    userin.execute(cmds, msg)
                    return userin.say(msg)
                except IndexError:
                    msg = "Sorry, " + user_prefix + " but I couldn't find a city named " + city + " on the internet."
                    userin.execute(cmds, msg)
                    return userin.say(msg)

        response = keyboard_commands.compare(com, doc, h, args, self.testing)
        if response:
            return response

        if ((h.check_text("shut") and h.check_text("down")) or (h.check_text("power") and h.check_text("off"))) and h.check_text("computer") and not args["server"]:
            cmds = [{'distro': 'All', 'name': ["gksudo", "poweroff"]}]
            return userin.execute(cmds, "Shutting down", True, 3)
        if h.check_nth_lemma(0, "goodbye") or h.check_nth_lemma(0, "bye") or (h.check_verb_lemma("see") and h.check_text("you") and h.check_adv_lemma("later")):
            response = userin.say("Goodbye, " + user_prefix)
            if not args["server"] and not self.testing:
                # raise KeyboardInterrupt
                thread.interrupt_main()
            return response

        response = find_in_wiki_command.first_compare(doc, h, USER_ANSWERING, userin, user_prefix)
        if response:
            return response

        response = find_in_youtube_command.compare(doc, h, args, self.testing, userin, user_prefix)
        if response:
            return response

        response = find_in_browser_command.compare_content(doc, h, userin)
        if response:
            return response

        response = find_in_browser_command.compare_image(doc, h, userin)
        if response:
            return response

        original_com = com
        com = coref.resolve(com)
        if args["verbose"]:
            print("After Coref Resolution: " + com)
        arithmetic_response = arithmetic_parse(com)
        if arithmetic_response:
            return userin.say(arithmetic_response)
        else:
            learner_response = learner.respond(com)
            if learner_response:
                return userin.say(learner_response)
            else:
                omniscient_response = omniscient.respond(com, not args["silent"], userin, user_prefix, args["server"])
                if omniscient_response:
                    return omniscient_response
                else:
                    dc_response = dc.respond(original_com, user_prefix)
                    if dc_response:
                        return userin.say(dc_response)


def tts_kill():
    """The top-level method to kill/end the text-to-speech output immediately.
    """

    subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)


def greet(userin):
    """The top-level method to greet the user with message like "*Good morning, sir.*".

    Args:
        userin:  :class:`ava.utilities.TextToAction` instance.

    Returns:
        str:  Response.
    """

    (columns, lines) = shutil.get_terminal_size()
    print(columns * "_" + "\n")
    time = datetime.datetime.now().time()

    global user_full_name
    global user_prefix
    global config_file
    global ava_name

    command = "getent passwd $LOGNAME | cut -d: -f5 | cut -d, -f1"
    user_full_name = os.popen(command).read()
    user_full_name = user_full_name[:-1]  # .decode("utf8")
    home = expanduser("~")
    config_file = TinyDB(home + '/.dragonfire_config.json')
    callme_config = config_file.search(Query().datatype == 'callme')
    name_config = config_file.search(Query().datatype == 'name')
    if callme_config:
        user_prefix = callme_config[0]['title']
    else:
        gender_config = config_file.search(Query().datatype == 'gender')
        if gender_config:
            user_prefix = GENDER_PREFIX[gender_config[0]['gender']]
        else:
            gender = Classifier.gender(user_full_name.split(' ', 1)[0])
            config_file.insert({'datatype': 'gender', 'gender': gender})
            user_prefix = GENDER_PREFIX[gender]
    if name_config:
        ava_name = name_config[0]['name']
    else:
        config_file.insert({'datatype': 'name', 'name': "A.V.A."})
        ava_name = "A.V.A."

    if datetime.time(4) < time < datetime.time(12):
        time_of_day = "morning"
    elif datetime.time(12) < time < datetime.time(18):
        time_of_day = "afternoon"
    elif datetime.time(18) < time < datetime.time(22):
        time_of_day = "evening"
    else:
        time_of_day = "night"
    cmds = [{'distro': 'All', 'name': ["echo"]}]
    userin.execute(cmds, "To activate say 'Dragonfire!' or 'Wake Up!'")
    return userin.say(" ".join(["Good", time_of_day, user_prefix]))


def speech_error():
    """The top-level method to indicate that there is a speech recognition error occurred.

    Returns:
        str:  Response.
    """
    cmds = [{'distro': 'All', 'name': ["echo"]}]
    userin.execute(cmds, "An error occurred")
    return userin.say("I couldn't understand, please repeat again.")


def initiate():
    """The top-level method to serve as the entry point of Dragonfire.

    This method is the entry point defined in `setup.py` for the `ava` executable that
    placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cli", help="Command-line interface mode. Give commands to Dragonfire via command-line inputs (keyboard) instead of audio inputs (microphone).", action="store_true")
    ap.add_argument("-s", "--silent", help="Silent mode. Disable Text-to-Speech output. Dragonfire won't generate any audio output.", action="store_true")
    ap.add_argument("-j", "--headless", help="Headless mode. Do not display an avatar animation on the screen. Disable the female head model.", action="store_true")
    ap.add_argument("-v", "--verbose", help="Increase verbosity of log output.", action="store_true")
    ap.add_argument("-g", "--gspeech", help="Instead of using the default speech recognition method(Mozilla DeepSpeech), use Google Speech Recognition service. (more accurate results)", action="store_true")
    ap.add_argument("--server", help="Server mode. Disable any audio functionality, serve a RESTful spaCy API and become a Twitter integrated chatbot.", metavar="REG_KEY")
    ap.add_argument("-p", "--port", help="Port number for server mode.", default="3301", metavar="PORT")
    ap.add_argument("--version", help="Display the version number of Dragonfire.", action="store_true")
    ap.add_argument("--db", help="Specificy the database engine for the knowledge base of learning feature. Values: 'mysql' for MySQL, 'sqlite' for SQLite. Default database engine is SQLite.", action="store", type=str)
    args = vars(ap.parse_args())
    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("ava").version)
        sys.exit(1)
    try:
        global dc
        userin = TextToAction(args)
        if not args["server"]:
            SystemTrayExitListenerSet(e)
            stray_proc = Process(target=SystemTrayInit)
            stray_proc.start()
            greet(userin)
        start(args, userin)
    except KeyboardInterrupt:
        if not args["server"]:
            stray_proc.terminate()
        sys.exit(1)


if __name__ == '__main__':
    initiate()
