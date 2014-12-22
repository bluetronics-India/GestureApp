import os

KEY_UP = 126;     KEY_DOWN = 125
KEY_RIGHT = 124;  KEY_LEFT = 123


sleep = "osascript -e 'tell app \"Finder\" to sleep'"

expose_up = """osascript<< END
tell application "System Events"
key code 126 using {control down}
end tell
END"""

expose_down = """osascript<< END
tell application "System Events"
key code 125 using {control down}
end tell
END"""

brght_up = """osascript<< END
tell application "System Events"
key code 113
end tell
END
"""

brght_down = """osascript<< END
tell application "System Events"
key code 107
end tell
END
"""

widget_scrn = """osascript<< END
tell application "System Events"
key code 111
end tell
END
"""

def vol(l): os.system("osascript -e 'set volume output volume "+str(l)+"'")


# run command
# os.system(widget_scrn)



# bash way to do it - pipe the text to osascript
# notice the for slashes in System Events
"""
echo "tell application \"System Events\"
key code 126 using {control down}
end tell" | osascript
"""
