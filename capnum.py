#!/usr/bin/python3
import asyncio
import gi
import signal
import sys
import os
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell, GLib

# This folder needs to exist, and this is the folder we use to check LED status.
LED_DIR = '/sys/class/leds/'

# This is the LED keys we want to look for. 
KEYS = ['numlock', 'capslock', 'kbd_backlight', 'compose', 'scrolllock']


class VisKeys():

    def __init__(self):
        self.indicators = self.findleds()
        self.states = {k:None for k in self.indicators}
        self.window = None
        self.e = None
        # Read in initial states
        try:
            for indicator in self.indicators:
                self.states[indicator] = int(open(self.indicators[indicator], 'r').read().strip())
        except FileNotFoundError:
            print('Error: Unable to open the LED indicator inputs. Make sure you are in "input" group.')
            sys.exit(1)

    def findleds(self) -> dict:
        ''' returns viable set of LEDs to watch.'''
        wanted = []
        for x in os.listdir(LED_DIR):
            for _ in KEYS:
                if x.endswith(_):
                    wanted.append(x)
        final = {}
        for x in wanted:
            x = x.split('::')
            if x[1] not in final:
                path = LED_DIR + x[0] + '::' + x[1] + '/brightness'
                if os.path.exists(path):
                    final[x[1]] = (path)
                else:
                    print(f'warn: skipped {x[1]} keys as it doesnt have a LED brightness indicator')
        print(f'Found these indicators: \n{[final[k] for k in final]}')
        return final

    async def run(self) -> None:
        while True:
            for indicator in self.indicators:
                newstate = int(open(self.indicators[indicator], 'r').read().strip())
                if newstate != self.states[indicator]:
                    self.states[indicator] = newstate
                    text = "   " + indicator.upper() + " is "
                    text += "ON " if newstate != 0 else "OFF "
                    await asyncio.create_task(
                        self.Overlay(text)
                    )
            await asyncio.sleep(0.1)

    async def Overlay(self, message) -> None:
        ''' Uses Pythons GDK bindings to overlay the data on the screen'''
        try:
            self.window = Gtk.Window()
            label = Gtk.Label(label=message)
            self.window.add(label)

            GtkLayerShell.init_for_window(self.window)
            GtkLayerShell.auto_exclusive_zone_enable(self.window)

            self.window.show_all()
            self.window.connect('destroy', Gtk.main_quit)
            GLib.timeout_add_seconds(1, self.window.destroy)
            Gtk.main()
        except RuntimeError:
            if self.e == None:
                print('ERROR: Unable to open Gtk in your X/wayland session. Using terminal output instead.')
                self.e = 1
            print(message)

    def signal_handler(self, sig, frame) -> None:
        ''' Handles kill signal..'''
        try:
            self.window.destroy()
        except Exception:
            pass
        print('thnx bye.')
        sys.exit(0)


if __name__ == "__main__":
    app = VisKeys()
    signal.signal(signal.SIGINT, app.signal_handler)
    asyncio.run(app.run())
