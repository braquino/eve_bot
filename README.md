# eve_bot
An EVE Online bot in python  
  
This bot is fully functional, only tested at Auvergne solar system in 1920 x 1080 resolution.  
It works reading the screen so, configuring it isn't a easy task. You have to get some special points and box from your EVE screen and congifure the methods bellow:  
  
## state_machine.py  
Undock button text when inside station
``` python
    def test_docked(self, scr):
        return read_screen_neg(scr, (1743, 174, 1837, 196), 180) == 'UNDOCK'
```
  
Locatin name text at space
``` python
    def read_location(self, scr):
        self.location = read_screen_neg(scr, (77, 135, 344, 154), 200)
```

Overview box with objects in space. Is important that the second overview tab be a mining one, that must contain only asterids and asteroid belts.
``` python
    def get_objects(self, overview, n_obj=5):
        self.select_overview(overview=overview)
        time.sleep(0.2)
        scr = ImageGrab.grab()
        obj_area = scr.crop((1673, 185, 1834, 617))
```

Configure the tab location for selecting the overviews. Is is extremely important that the "General" be a tab only with the statin to back.
``` python
    def select_overview(self, overview):
        if overview == 'General':
            x = 1768
        else:
            x = 1723
        print(x)
        pyautogui.moveTo(x, 153)
        time.sleep(0.1)
        pyautogui.click(x, 153)
```
The next are hard to get, they ar points to test if the activtion white bar around the strip miners are activated and are at half position. This is a RGB test for white, indicating tha the bar passed to this points, for the two miners.
``` python
    def check_stripers(self, scr):
        im = np.asarray(scr)
        striper1 = im[958, 1080, :].mean() > 90
        striper2 = im[958, 1130, :].mean() > 90
        self.stripers = [striper1, striper2]
        # TODO: Improve the way it works, avoiding read pixels, maybe reading memory

    def check_stripers_half(self, scr):
        im = np.asarray(scr)
        striper1 = im[911, 1080, :].mean() > 90
        striper2 = im[911, 1130, :].mean() > 90
        self.stripers_half = [striper1, striper2]
        # TODO: Improve the way it works, avoiding read pixels, maybe reading memory
```

And for last, get a point of the red cross at a targeted object to see if there is a target already:
``` python
    def check_target(self, scr):
        #### Not working well
        # target_text = self.read_targeted(scr)
        # return 'm' in target_text
        r, g, b = np.asarray(scr)[94, 1764, :]
        print(r, g, b)
        return int(r) > (int(g) + int(b))
```
## action_agent.py  

Configure the two methods: undock and unload

and configure this line with the first letters of you system:  
``` python
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
```

## Running the bot  

1. just open EVE Online, select you character.  
2. Alt-tab.  
3. Run the mining_run.py file.
