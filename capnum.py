import asyncio
import gi
import signal
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell, GLib

class VisKeys():

    def __init__(self):
        self.indicators = {
            'numlock': '/sys/class/leds/input21::numlock/brightness',
            'capslock': '/sys/class/leds/input21::capslock/brightness'
        }
        self.states = {'numlock': None, 'capslock': None}
        self.window = None
        # Read in initial states
        try:
            for indicator in self.indicators:
                self.states[indicator] = int(open(self.indicators[indicator], 'r').read().strip())
        except FileNotFoundError:
            print('Unable to locate the files set in the script. please update this part in the script:')
            print(str(self.indicators))
            sys.exit(1)


    async def run(self) -> None:
        while True:
            for indicator in self.indicators:
                newstate = int(open(self.indicators[indicator], 'r').read().strip())
                if newstate != self.states[indicator]:
                    self.states[indicator] = newstate
                    text = "   " + indicator.upper() + " is "
                    text += "ON " if newstate == 1 else "OFF "
                    await asyncio.create_task(self.Overlay(text))
            await asyncio.sleep(0.1)


    async def Overlay(self, message) -> None:
        ''' Uses Pythons GDK bindings to overlay the data on the screen'''
        self.window = Gtk.Window()
        label = Gtk.Label(label=message)
        self.window.add(label)

        GtkLayerShell.init_for_window(self.window)
        GtkLayerShell.auto_exclusive_zone_enable(self.window)

        self.window.show_all()
        self.window.connect('destroy', Gtk.main_quit)
        GLib.timeout_add_seconds(1, self.window.destroy)
        Gtk.main()

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
