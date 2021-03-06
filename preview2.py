#Preview 1st pass
from GUIWrapper import *
from rgb_and_map import *

import sys, os, traceback, string, json


#Global Variables:


#width, height = width - 20, height + 20
BackGr = (0, 0, 0)
name = "DaEvil1 Preview Map"
Transparent = (255, 255, 255)

image_source = sys.argv[1]
json_source = sys.argv[2]

def get_base():
    base = []
    image_map = Object(image_source)
    width = image_map.data["width"]
    height = image_map.data["height"]
    for i in range(height):
        base.append([])
        for j in range(width):
            cur_pixel = image_map.PixelColor((j, i))
            cur_pixel_color = [cur_pixel[k] for k in range(3)]
            cur_pixel_color = tuple(cur_pixel_color)
            pixel_name = rgb_codes[cur_pixel_color]
            base[i].append(pixel_name)
    return base, width, height

def get_paths():
    script_path = os.path.dirname(__file__)
    rel_tiles = "/img/tiles.png"
    rel_portal = "/img/portal.png"
    rel_boost = "/img/Boost.png"
    rel_blue_boost =  "/img/Blue Boost.png"
    rel_red_boost =  "/img/Red Boost.png"
    files = {}
    files["tiles"] = script_path + rel_tiles
    files["portal"] = script_path + rel_portal
    files["boost"] = script_path + rel_boost
    files["blue boost"] = script_path + rel_blue_boost
    files["red boost"] = script_path + rel_red_boost
    return files

def win_init(width, height):
    win = Window("Map Preview", width*40, height*40)
    win.Modify("background", BackGr)
    return win, win.Get("screen")

def var_init(files):
    functions = {"tiles" : tiles_map, "portal" : portal_map, "boost" : boost_map, 
            "red boost" : boost_red_map, "blue boost" : boost_blue_map}
    back_tiles = {}
    for i in ["floor", "red speed", "blue speed"]:
        newtile = Object(files["tiles"])
        x, y = functions["tiles"][i]
        square = (x, y, 40, 40)
        newtile.Modify("chop", square)
        back_tiles[i] = newtile
    return functions, back_tiles


def check_init():
    surrounding = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    rel_tiles = ["blue flag", "red flag", "powerup", "boost", "blue boost"
             , "red boost", "portal", "bomb", "spike", "button", "portal on"
             , "portal off", "blue spawn", "red spawn", "neutral flag"]
    tile_check = {"45 tile" : [[-1, 0], [0, -1]], "135 tile" : [[-1, 0], [0, 1]]
                 , "225 tile" : [[1, 0], [0, 1]], "315 tile" : [[1, 0], [0, -1]]
                 }
    for element in rel_tiles:
        tile_check[element] = surrounding
    return tile_check

def backgroundFix(y, x, base, tile_check, prevd=False):
    floors = ["floor", "blue speed", "red speed"]
    if base[y][x] in tile_check:
        for element in tile_check[base[y][x]]:
            try:
                dx, dy = element[0], element[1]
                current_t = base[y+ dy][x + dx] 
                if current_t in floors:
                    return current_t
                else:
                    if base[y+ dy][x + dx] in tile_check and (dy, dx) != -prevd:
                        current = (y, x)
                        recursive_tile = backgroundFix(y + dy, x + dx, base,  
                                                       tile_check, (dy, dx))
                        if recursive_tile:
                            return recursive_tile
            except:
                pass
    return False

def background_gen(base):
    tile_check = check_init()
    floor_back_rects = []
    for i in range(len(base)):
        for j in range(len(base[i])):
            floor_back_rects.append(False)
    for i in range(len(base)):
        for j in range(len(base[i])):
            n = j + i*len(base[i]) - 2
            back_tile = backgroundFix(i, j, base, tile_check)
            if back_tile:
                floor_back_rects[n] = ((j*40, i*40, (j+1)*40, (i+1)*40), back_tile)
    return floor_back_rects

def gen_tile_objs(functions, files):
    tiles ={}
    for element in functions:
        for i in functions[element]:
            newtile = Object(files[element])
            tile_x, tile_y = functions[element][i]
            square = (tile_x, tile_y, 40, 40)
            newtile.Modify("chop", square)
            tiles[i] = newtile
    return tiles
        
def gen_rects(base):
    rects = []
    tiles_id = []
    for i in range(len(base)):
        for j in range(len(base[i])):
            new_rect = (j*40, i*40, (j+1)*40, (i+1)*40)
            rects.append(new_rect)
            tiles_id.append(base[i][j])
    return rects, tiles_id


def draw_map(base, width, height, filename):
    files = get_paths()
    functions, back_tiles = var_init(files)
    floor_back_rects = background_gen(base)
    win, screen = win_init(width, height)
    tiles = gen_tile_objs(functions, files)
    rects, tiles_id = gen_rects(base)
    for element in floor_back_rects:
        if element:
            cur_tile = back_tiles[element[1]]
            tile_rect = element[0]
            cur_tile.data["rect"] = tile_rect
            cur_tile.AlphaBlit(screen)
    for i in range(len(tiles_id)):
        tiles[tiles_id[i]].data["rect"] = rects[i]
        tiles[tiles_id[i]].AlphaBlit(screen)
        win.Update()
    win.Modify("save", filename)
    win.Quit()



def translate_json(base):
    json_data = open(json_source, "r")
    data = json.load(json_data)
    author = data["info"]["author"]
    name = data["info"]["name"]
    gate_states = {
            "on" : "gate neutral", "off" : "gate off", 
            "red" : "gate red", "blue" : "gate blue"
            }
    for element in data["fields"]:
        coords = string.split(element, ",")
        coords = [int(i) for i in coords]
        if base[coords[1]][coords[0]] == "gate":
            state = data["fields"][element]["defaultState"]
            base[coords[1]][coords[0]] = gate_states[state]
#        print base[coords[1]][coords[0]]
#        print coords
#        print element, data["fields"][element]["defaultState"]
    for element in data["portals"]:
        coords = string.split(element, ",")
        coords = [int(i) for i in coords]
        if base[coords[1]][coords[0]] == "portal":
            base[coords[1]][coords[0]] = "portal off"
            if "destination" in data["portals"][element]:
                if "x" in data["portals"][element]["destination"]:
                    base[coords[1]][coords[0]] = "portal on"
    if "spawnPoints" in data:
        colors = ["red", "blue"]
        for color in colors:
            for element in data["spawnPoints"][color]:
                x = element["x"]
                y = element["y"]
                base[y][x] = color + " spawn"
    filename = name + " " + "by " + author + ".png"
    return base, filename

def main():
    base, width, height = get_base()
    base, filename = translate_json(base)
    draw_map(base, width, height, filename)
    #write_summary(height, width, new_file)



if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)
    pygame.quit() 

