import asyncio
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell, GLib

indicators = {
    'numlock': '/sys/class/leds/input34::numlock/brightness',
    'capslock': '/sys/class/leds/input34::capslock/brightness'
}

states = {'numlock': None, 'capslock': None}
window = None

# Read in initial states
for indicator in indicators:
    states[indicator] = int(open(indicators[indicator], 'r').read().strip())


async def main():
    while True:
        for indicator in indicators:
            newstate = int(open(indicators[indicator], 'r').read().strip())
            if newstate != states[indicator]:
                states[indicator] = newstate
                text = collate(indicator, newstate)
                await asyncio.create_task(Overlay(text))
        await asyncio.sleep(0.1)


async def Overlay(message):
    window = Gtk.Window()
    label = Gtk.Label(label=message)
    window.add(label)

    GtkLayerShell.init_for_window(window)
    GtkLayerShell.auto_exclusive_zone_enable(window)

    window.show_all()
    window.connect('destroy', Gtk.main_quit)
    GLib.timeout_add_seconds(1, window.destroy)
    Gtk.main()

def collate(indicator, newstate) -> str:
    text = "   " + indicator.upper() + " is "
    text += "ON " if newstate == 1 else "OFF "
    return text


if __name__ == "__main__":
    asyncio.run(main())
