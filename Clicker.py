import win32api, win32con, pyHook, time, pythoncom, threading
from spelldefinitions import SpellType, SpellMode

SLEEP_TIME = 0.0333333
REMIND_TIME = 3

MANA_RECHARGE = 4.4

SPELL_MODE = SpellMode.Syncronised
SPELLS_TO_CAST = [SpellType.CallToArms, SpellType.GoblinsGreed]
SPELL_DELAY = 0.5

def EngageCursorHold(flag = True):
    global bHoldCursor, cursorPos
    if flag:
        print("Locking cursor...")
        bHoldCursor = True
        cursorPos = win32api.GetCursorPos()
        win32api.ClipCursor((cursorPos[0] - 1, cursorPos[1] - 1, cursorPos[0] + 1, cursorPos[1] + 1))
    else:
        win32api.ClipCursor()
        bHoldCursor = False
        print("Cursor unlocked!")

def SwitchClicking():
    global lock, bShouldClick, bHoldCursor
    
    clickLock.acquire()
    bShouldClick = not bShouldClick
    if bShouldClick:
        print("Starting clicking...")
        EngageCursorHold(True)
    else:
        EngageCursorHold(False)
        print("Ending clicking!")
    clickLock.release()
    
def SwitchCasting():
    global bShouldCast
    bShouldCast = not bShouldCast
    
    if bShouldCast:
        print("Spell casting enabled!")
    else:
        print("Spell casting disabled.")
    
def ResetSpellTimer(time = 0):
    global spellLock, spellTime
    spellLock.acquire()
    spellTime = time
    spellLock.release()
    print("Spell timer reset!")
    
def CastSpells():
    if not bShouldCast or SPELL_MODE == SpellMode.Disabled:
        return
        
    sc = None
    if SPELL_MODE == SpellMode.Syncronised:
        sc = threading.Thread(target=CastSyncronised)
    elif SPELL_MODE == SpellMode.Delay:
        sc = threading.Thread(target=CastDelay)
    elif SPELL_MODE == SpellMode.DelayedBurst:
        sc = threading.Thread(target=CastDelayedBurst)
        
    if sc == None:
        CastSpell()
    else:
        sc.setDaemon(True)
        sc.start()
    
    ResetSpellTimer(time.time())
    
def CastSpell(spell):
    ONE_KEYCODE = 0x31
    
    keycode = ONE_KEYCODE + (spell['num'] - 1)
    win32api.keybd_event(keycode, 0, 0, 0)
    win32api.keybd_event(keycode, 0, win32con.KEYEVENTF_KEYUP, 0)
        
def CastSyncronised():
    for spell in SPELLS_TO_CAST:
        CastSpell(spell)
    
def CastDelay():
    for spell in SPELLS_TO_CAST:
        CastSpell(spell)
        time.sleep(SPELL_DELAY)
        
def CastDelayedBurst():
    spells = SPELLS_TO_CAST
    
    CastSpell(spells.pop(0))
    
    time.sleep(SPELL_DELAY)
    
    for spell in spells:
        CastSpell(spell)

def OnKeyboardEvent(event):
    if event.KeyID == 223:      # `
        SwitchClicking()
    elif event.KeyID == 107:    # +
        SwitchCasting()
    elif event.KeyID == 106:    # *   
        ResetSpellTimer()
    elif event.KeyID == 109:    # -
        global bHoldCursor
        EngageCursorHold(not bHoldCursor)
    elif event.KeyID == 27:     # Esc
        exit()
    
def KeyboardMonitor():
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    
    pythoncom.PumpMessages()

def CheckSpellCast():
    global spellLock, elapsed, spellTime, timeToCast
    spellLock.acquire()
    elapsed = time.time() - spellTime
    spellLock.release()
    if elapsed > timeToCast:
        CastSpells()
        
    global elapsedRemind, remindTime
    elapsedRemind = time.time() - remindTime
    if elapsedRemind > REMIND_TIME:
        print("Time since last cast: {:3.2f}".format(elapsed))
        remindTime = time.time()
        
def ClickMouse():
    if not bHoldCursor:
        mX, mY = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mX, mY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, mX, mY, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, cursorPos[0], cursorPos[1], 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, cursorPos[0], cursorPos[1], 0, 0)

bShouldCast = False
timeToCast = 1
for spell in SPELLS_TO_CAST:
    timeToCast += spell['cost']
timeToCast /= MANA_RECHARGE
print("Time between spells: {:3.2f}".format(timeToCast))
    
clickLock = threading.Lock()
spellLock = threading.Lock()

bHoldCursor = False
cursorPos = (0, 0)

km = threading.Thread(target=KeyboardMonitor)
km.setDaemon(True)
km.start()

spellTime = 0
remindTime = 0
bShouldClick = False
while(True):
    time.sleep(SLEEP_TIME)

    clickLock.acquire()
    flag = bShouldClick
    clickLock.release()
    
    if not bShouldClick:
        continue
        
    if bShouldCast:
        CheckSpellCast()
    
    ClickMouse()