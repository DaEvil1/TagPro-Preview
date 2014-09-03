rgb_codes = {
        (0, 0, 0) : "black",
        (55, 55, 55): "spike",
        (155, 0,  0): "red spawn",
        (0, 0, 155): "blue spawn",
        (255, 128, 0): "bomb",
        (128, 128, 0): "neutral flag",
        (255, 0, 0): "red flag",
        (0, 0, 255): "blue flag",
        (0, 117, 0): "gate",
        (212, 212, 212): "floor",
        (220, 186, 186): "red speed",
        (187, 184, 221): "blue speed",
        (185, 0, 0): "red endzone",
        (25, 0, 148): "blue endzone",
        (185, 122, 87): "button",
        (120, 120, 120): "wall",
        (0, 255, 0): "powerup",
        (128, 64, 112): "45 tile",
        (128, 112, 64): "315 tile",
        (64, 80, 128): "135 tile",
        (64, 128, 80): "225 tile",
        (202, 192, 0): "portal",
        (255, 255, 0): "boost",
        (255, 115, 115): "red boost",
        (115, 115, 255): "blue boost",
}

tiles_map = {
        "spike" : (480, 0),
        "red spawn" : (560, 0),
        "blue spawn" : (600, 0),
        "bomb" : (480, 40),
        "neutral flag" : (520, 40),
        "red flag" : (560, 40),
        "blue flag" : (600, 40),
        "gate off" : (480, 120),
        "gate neutral" : (520, 120),
        "gate red" : (560, 120),
        "gate blue" : (600, 120),
        "floor" : (520, 160),
        "red speed" : (560, 160),
        "blue speed" : (600, 160),
        "red endzone" : (560, 200),
        "blue endzone" : (600, 200),
        "button" : (520, 240),
        "black" : (560, 240),
        "wall" : (600, 240),
        "powerup" : (480, 280),
        "315 tile" : (600, 280),
        "45 tile" : (600, 320),
        "225 tile" : (600, 360), 
        "135 tile" : (600, 400), 
        "mars ball" : (480, 360),
        }
portal_map = {
        "portal on" : (0, 0), 
        "portal off" : (160, 0)
        }

boost_map = {
        "boost" : (0, 0)
        }

boost_red_map = {
        "red boost" : (0, 0)
        }

boost_blue_map = {
        "blue boost" : (0, 0)
        }
