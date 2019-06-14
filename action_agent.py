from state_machine import StateMachine
from detector import get_windows_logo, read_screen_neg, detector, multi_detector
import pyautogui
import time
from PIL import Image, ImageGrab
import random

class ActionAgent(object):

    def __init__(self):
        self.scr = ImageGrab.grab()
        self.enter_game()
        self.state_machine = StateMachine()

    def _refresh_screen(self):
        self.scr = ImageGrab.grab()

    def _click(self, point, delay=0.3):
        pyautogui.moveTo(point[0], point[1])
        time.sleep(delay)
        pyautogui.click(point[0], point[1])

    def activate_stripers(self, number):
        # Selection by mouse
        '''
        template = Image.open('img_templates/one_striper.jpg')
        self._refresh_screen()
        clicks = multi_detector(self.scr, template)
        clicks = clicks[:1] + [x for x in clicks if abs(x[0] - clicks[0][0]) > 4][:1]
        #print(clicks)
        for click in clicks:
            self._click(click)
        '''
        # selection by hotkeys
        hotkey = 'F{}'.format(number)
        pyautogui.keyDown(hotkey)
        pyautogui.keyUp(hotkey)
        time.sleep(0.2)
        self.aproach()


    def enter_game(self):
        template = Image.open('img_templates/ico_win_EVE.JPG')
        click = detector(self.scr, template)
        self._click(click)


    def warp_random_belt(self):
        self._refresh_screen()
        self.state_machine.get_objects(overview='Mining', n_obj=4)
        try:
            list_places = [x[2] for x in self.state_machine.objects if x[1][:4] == 'Auve']
            go_to = random.choice(list_places)
            self._click(go_to)
            self.warp_zero()
        except:
            pass

    def warp_zero(self):
        '''
        template = Image.open('img_templates/warp_zero.jpg')
        self._refresh_screen()
        clicks = multi_detector(self.scr, template)
        self._click(clicks[0])
        '''
        pyautogui.keyDown('s')
        pyautogui.keyUp('s')
        time.sleep(60)

    def dock(self):
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
        time.sleep(50)
        self.state_machine.change_state(1)

    def aproach(self):
        '''
        template = Image.open('img_templates/aproach.jpg')
        self._refresh_screen()
        clicks = multi_detector(self.scr, template)
        self._click(clicks[0])
        '''
        pyautogui.keyDown('q')
        pyautogui.keyUp('q')

    def target(self):
        '''
        template = Image.open('img_templates/target.jpg')
        self._refresh_screen()
        clicks = multi_detector(self.scr, template)
        self._click(clicks[0])
        '''
        pyautogui.keyDown('Ctrl')
        pyautogui.keyUp('Ctrl')

    def aproach_asteroid(self):
        self.state_machine.get_objects(overview='Mining')
        try:
            go_to = [x[2] for x in self.state_machine.objects if x[1] == 'Asteroid'][0]
            self._click(go_to)
            time.sleep(1)
            self.target()
            time.sleep(0.3)
            self.aproach()
        except:
            pass

    def dock_station(self):
        self.state_machine.get_objects(overview='General')
        try:
            go_to = [x[2] for x in self.state_machine.objects][0]
            self._click(go_to)
            time.sleep(1)
            self.dock()
            time.sleep(40)
        except:
            pass

    def undock(self):
        pyautogui.moveTo(1797, 190)
        time.sleep(0.1)
        pyautogui.click(1797, 190)
        time.sleep(30)
        pyautogui.moveTo(850, 967)
        time.sleep(0.1)
        pyautogui.click(850, 967)
        time.sleep(0.2)
        pyautogui.moveTo(924, 980)
        time.sleep(0.1)
        pyautogui.click(924, 980)

    def unload(self):
        # open inventory
        pyautogui.keyDown('Alt')
        pyautogui.keyDown('c')
        pyautogui.keyUp('c')
        pyautogui.keyUp('Alt')
        time.sleep(3)
        # click on ore hold
        pyautogui.moveTo(193, 320)
        time.sleep(0.2)
        pyautogui.click(193, 320)
        time.sleep(3)
        # click ore
        pyautogui.moveTo(337, 335)
        time.sleep(0.2)
        pyautogui.click(337, 335)
        time.sleep(3)
        # select all
        pyautogui.keyDown('Ctrl')
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
        pyautogui.keyUp('Ctrl')
        # drag to station
        pyautogui.mouseDown(337, 335)
        time.sleep(0.2)
        pyautogui.moveTo(187, 394)
        time.sleep(0.2)
        pyautogui.mouseUp(187, 394)
        time.sleep(2)
        # close inventory
        pyautogui.keyDown('Alt')
        pyautogui.keyDown('c')
        pyautogui.keyUp('c')
        pyautogui.keyUp('Alt')

        time.sleep(1)
        self.state_machine.cargo = 0



    def decision_tree(self):
        self._refresh_screen()
        if self.state_machine.test_docked(self.scr):
            if self.state_machine.cargo < 20:
                self.undock()
            else:
                self.unload()
        else:
            self.state_machine.check_cargo(self.scr)
            self.state_machine.read_location(self.scr)
            if self.state_machine.cargo > 95:
                self.dock_station()
            else:
                if 'Aste' not in self.state_machine.location:
                    self.warp_random_belt()
                else:
                    if self.state_machine.check_target(self.scr):
                        self.state_machine.check_stripers(self.scr)
                        self.state_machine.check_stripers_half(self.scr)
                        if not self.state_machine.stripers[0]:
                            self.activate_stripers(1)
                        else:
                            if self.state_machine.stripers_half[0]:
                                self.activate_stripers(1)
                        if not self.state_machine.stripers[1]:
                            self.activate_stripers(2)
                        else:
                            if self.state_machine.stripers_half[1]:
                                self.activate_stripers(2)
                    else:
                        self.aproach_asteroid()
                        if not [x for x in self.state_machine.objects if 'Aste' in x[1]]:
                            self.warp_random_belt()


    def run(self):
        while True:
            self.decision_tree()
            pyautogui.moveTo(500, 500)
            time.sleep(5)
