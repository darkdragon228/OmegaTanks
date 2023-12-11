import sys
from screeninfo import get_monitors
from bin.core import *

core_init()

for m in get_monitors():
    Wwidth = m.width
    Wheight = m.height

interface1 = Interface()
interface2 = Interface()

interface1.add_button(Wwidth/2-150, 300, 200, 100, "bin/sprites/button1.png", interface2.start, None, "компанія", 20, 30)
interface1.add_button(Wwidth/2-150, 440, 200, 100, "bin/sprites/button1.png", MapEditor, None, "редактор карт", 20, 30)
interface1.add_button(Wwidth/2-150, 580, 200, 100, "bin/sprites/button1.png", sys.exit, None, "вихід", 45, 30)

interface2.add_button(200, 100, 100, 100, "bin/sprites/button2.png", ReadMap, "bin/maps/company/phase1/level1.json", "1", 40, 30)
interface2.add_button(350, 100, 100, 100, "bin/sprites/button2.png", ReadMap, "bin/maps/company/phase1/level2.json", "2", 40, 30)
interface2.add_button(Wwidth-250, Wheight-150, 200, 100, "bin/sprites/button1.png", interface2.exit, None, "назад", 40, 30)

interface1.start()