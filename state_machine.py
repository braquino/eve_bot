from detector import get_windows_logo, read_screen_neg, detector
from PIL import Image, ImageGrab
import numpy as np
import pyautogui
import time
numbers_replaces = {'S': '5', '?': '7', '!': '1'}

class StateMachine(object):

    def __init__(self):
        self.state_list = {0: 'out_of_eve',
                            1: 'docked',
                            2: 'undocked',
                            3: 'warping_to_belt',
                            4: 'at_belt',
                            5: 'mining',
                            6: 'full',
                            7: 'warping_to_station'}

        self.docked = False
        self.location = None
        self.previous_state = None
        self.state = 0
        self.objects = None
        self.cargo = 0
        self.stripers = [False, False]
        get_windows_logo(ImageGrab.grab()).save('img_templates/win_logo.jpg')

    def test_out_of_eve(self, scr):
        test_logo = np.asarray(get_windows_logo(scr))
        saved_logo = np.asarray(Image.open('img_templates/win_logo.jpg'))
        error = np.mean(test_logo - saved_logo)
        return 1 > error > -1

    def change_state(self, new_state):
        self.previous_state = self.state
        self.state = new_state

    def test_docked(self, scr):
        return read_screen_neg(scr, (1743, 174, 1837, 196), 180) == 'UNDOCK'

    def test_at_belt(self, scr):
        pass

    def read_location(self, scr):
        self.location = read_screen_neg(scr, (77, 135, 344, 154), 200)

    def get_objects(self, overview, n_obj=5):
        self.select_overview(overview=overview)
        time.sleep(0.2)
        scr = ImageGrab.grab()
        obj_area = scr.crop((1673, 185, 1834, 617))
        # TODO: Get this area automatic
        interval = 19
        objs = []
        for i in range(n_obj):
            start = i * interval
            temp_list = read_screen_neg(obj_area, (0, start, 430, start + interval), 100).split(' ')[:3]
            dist, um, obj = temp_list
            dist = dist.replace('.', '')
            try:
                dist = int(dist)
            except:
                for char in numbers_replaces:
                    dist = dist.replace(char, numbers_replaces[char])
                dist = int(dist)
            if um == 'm':
                dist = dist
            elif um == 'km':
                dist = dist * 1000
            else:
                dist = dist * 1000000
            click = (1750, start + 10 + 185)
            objs.append([dist, obj, click])

        self.objects = objs

    def check_cargo(self, scr):
        template = Image.open('img_templates/cargo.jpg')
        coords = detector(scr, template)
        pyautogui.moveTo(coords[0], coords[1])
        time.sleep(1)
        sc = ImageGrab.grab()
        text = read_screen_neg(sc, (coords[0] - 90, coords[1] - 130, coords[0] + 75, coords[1] - 15), 100)
        text = text.replace('%', '')
        idx = text.find('Ore Hold')
        try:
            self.cargo = float(text[idx + 8:idx + 8 + 6])
        except:
            self.cargo = 0

    def select_overview(self, overview):
        if overview == 'General':
            x = 1676
        else:
            x = 1723
        print(x)
        pyautogui.moveTo(x, 153)
        time.sleep(0.1)
        pyautogui.click(x, 153)

    def read_targeted(self, scr):
        texto = read_screen_neg(scr, (1541, 114, 1643, 170), 120)
        print(texto)
        return texto

    def check_stripers(self, scr):
        im = np.asarray(scr)
        striper1 = im[958, 1080, :].mean() > 90
        striper2 = im[958, 1130, :].mean() > 90
        self.stripers = [striper1, striper2]
        # TODO: Improve the way it works, avoiding read pixels, maybe reading memory

    def check_target(self, scr):
        target_text = self.read_targeted(scr)
        return 'm' in target_text
