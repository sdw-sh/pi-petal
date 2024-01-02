import logging
import os


class ControlElement:
    def __init__(self, name, display, button_1, button_2) -> None:
        self.name = name
        self.display = display
        self.button_1 = button_1
        self.button_2 = button_2


class ControlState:
    def __init__(self, controls) -> None:
        self.active_control = 0
        self.controls = controls
        self.output()

    def change_active_selection(self, *_):
        self.active_control += 1
        if self.active_control > len(self.controls) - 1:
            self.active_control = 0
        self.output()

    def output(self):
        # TODO add output manager object for print(), display etc.
        # os.system("clear")
        control = self.controls[self.active_control]
        logging.info(control.display())

    def button_1(self, *_):
        control = self.controls[self.active_control]
        control.button_1()
        self.output()

    def button_2(self, *_):
        control = self.controls[self.active_control]
        control.button_2()
        self.output()
