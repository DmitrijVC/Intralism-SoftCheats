__author__ = "FssAy"
__version__ = "1.0.0"
__url__ = "https://github.com/DmitrijVC/Intralism-SoftCheats"
__license__ = "https://github.com/DmitrijVC/Intralism-SoftCheats/blob/main/LICENSE"

import json
import logging
import os
import threading
import time as timer
from datetime import datetime

import keyboard
import psutil
import win32gui
import win32process

import keyboard_local


class Objects(object):
    SPAWN = "SpawnObj"

    UP = "[Up]"
    RIGHT = "[Right]"
    DOWN = "[Down]"
    RIGHT_LEFT = "[Right-Left]"
    LEFT = "[Left]"
    UP_RIGHT_LEFT = "[Up-Right-Left]"
    UP_DOWN_LEFT = "[Up-Down-Left]"
    RIGHT_DOWN_LEFT = "[Right-Down-Left]"
    UP_RIGHT_DOWN = "[Up-Right-Down]"
    UP_RIGHT_DOWN_LEFT = "[Up-Right-Down-Left]"
    UP_LEFT = "[Up-Left]"
    DOWN_LEFT = "[Down-Left]"
    RIGHT_DOWN = "[Right-Down]"
    UP_RIGHT = "[Up-Right]"
    UP_DOWN = "[Up-Down]"
    POWERUP = "[PowerUp]"


# class Keys:
#     @staticmethod
#     def get_key(obj: Objects()):
#         switch = {
#             Objects.UP: ["up"],
#             Objects.RIGHT: ["right"],
#             Objects.DOWN: ["down"],
#             Objects.RIGHT_LEFT: ["right", "left"],
#             Objects.LEFT: ["left"],
#             Objects.UP_RIGHT_LEFT: ["left", "right", "up"],
#             Objects.RIGHT_DOWN_LEFT: ["left", "right", "down"],
#         }


class Config:
    def __init__(self, file_name: str):
        self.config: dict
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as f:
                    self.config = json.loads(f.read())
                f.close()
            except Exception as e:
                logging.critical(f"Can't read the json file, {e}.")
            sub_by: float = 0.0
            for event in self.config["events"]:
                if sub_by == 0.0:
                    if event["data"][0] == Objects.SPAWN:
                        sub_by = event["time"]
                event["time"] = event["time"] - sub_by
        else:
            logging.critical("File doesn't exists.")

    # Debug method made to get data for Objects class
    def _get_all_objects(self):
        objects = []
        for event in self.config["events"]:
            if event["data"][0] == Objects.SPAWN:
                if event["data"][1] not in objects:
                    objects.append(event["data"][1])
        objectt: str
        for objectt in objects:
            variable = objectt.replace("-", "_").replace("[", "").replace("]", "").upper() + " = "
            print(f"{variable}\"{objectt}\"")
        return objects


class Bot:
    def __init__(self, key_start: str, key_stop: str, config: Config, wait: float = 0):
        self.key_start = key_start
        self.key_stop = key_stop
        self.config = config
        self.wait = wait

        self.start_timestamp = datetime.now().timestamp()
        self.index = 0
        self.running = False
        self.thread = None

        keyboard.add_hotkey(key_start, self.start)
        keyboard.add_hotkey(key_stop, self.stop)

        logging.info("[INFO] waiting for the start key...")

    def start(self):
        if self.running is False:
            logging.info("[KEYBOARD] starting the bot.")
            self.running = True
            if self.thread is None:
                self.thread = threading.Thread(target=self._run)
                self.thread.start()

    def stop(self):
        if self.running is True:
            logging.info("[KEYBOARD] closing the bot.")
            self.running = False
            self.thread = None

    @staticmethod
    def _simulate_object(obj: str):
        obj = obj.replace("[", "").replace("]", "").replace(",0", "")
        key: str
        for key in obj.split("-"):
            if key == "Up":
                keyboard_local.Keyboard.key(keyboard_local.Keyboard.VK_UP, 0.01)
            elif key == "Left":
                keyboard_local.Keyboard.key(keyboard_local.Keyboard.VK_LEFT, 0.01)
            elif key == "Right":
                keyboard_local.Keyboard.key(keyboard_local.Keyboard.VK_RIGHT, 0.01)
            elif key == "Down":
                keyboard_local.Keyboard.key(keyboard_local.Keyboard.VK_DOWN, 0.01)

    @staticmethod
    def _is_active_window_process(proc_name: str):
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        try:
            if psutil.Process(pid[-1]).name() == proc_name:
                return True
        except:
            return False
        return False

    def _run(self):

        events = self.config.config["events"]  # []
        # for event in self.config.config["events"]:
        #     events.append(event)

        self.index = 0
        self.start_timestamp = datetime.now().timestamp()

        # unnecessary
        if self.wait != 0:
            logging.info(f"[INFO] Waiting for {self.wait} seconds...")
            timer.sleep(self.wait)
            logging.info(f"[INFO] Done!")

        while self.running:

            if not self._is_active_window_process("Intralism.exe"):
                logging.error(f"[ERROR] Game window is not active!")
                self.stop()

            time = datetime.now().timestamp() - self.start_timestamp
            if events[self.index]["time"] <= time:

                if events[self.index]["data"][0] == Objects.SPAWN:
                    self._simulate_object(events[self.index]['data'][1])
                    logging.info(f"[EVENT] {events[self.index]['data'][1]} at {time}")
                else:
                    logging.info(f"[EVENT] <decor> at {time}")

                if self.index == events.__len__() - 1:
                    logging.info(f"[INFO] DONE!")
                    self.stop()
                    break
                self.index += 1
