from state_machine import StateMachine
from detector import get_windows_logo, read_screen_neg, detector, multi_detector
import pyautogui
import time
from PIL import Image, ImageGrab

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


    def enter_game(self):
        template = Image.open('img_templates/ico_win_EVE.JPG')
        click = detector(self.scr, template)
        self._click(click)

    def warp_random_belt(self):
        self._refresh_screen()
        self.state_machine.get_objects(self.scr)
        go_to = [x[2] for x in self.state_machine.objects if x[1][:4] == 'Auve'][0]
        self._click(go_to)
        self.warp_zero()

    def warp_zero(self):
        '''
        template = Image.open('img_templates/warp_zero.jpg')
        self._refresh_screen()
        clicks = multi_detector(self.scr, template)
        self._click(clicks[0])
        '''
        pyautogui.keyDown('s')
        pyautogui.keyUp('s')

    def dock(self):
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')

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
        self.state_machine.get_objects('Mining')
        go_to = [x[2] for x in self.state_machine.objects if x[1] == 'Asteroid'][0]
        self._click(go_to)
        time.sleep(1)
        self.target()
        time.sleep(0.1)
        self.aproach()

    def dock_station(self):
        self.state_machine.get_objects('General')
        go_to = [x[2] for x in self.state_machine.objects if x[1] == 'Asteroid'][0]
        self._click(go_to)
        time.sleep(1)
        self.dock()


