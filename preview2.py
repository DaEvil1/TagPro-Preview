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
    floor = Object(files["tiles"])
    x, y = functions["tiles"]["floor"]
    square = (x, y, 40, 40)
    floor.Modify("chop", square)
    return functions, floor

def background_gen(base, functions):
    excluded = ("floor", "black", "gate neutral", "gate off", 
                "gate red", "gate blue", "wall")
    rel_coords = [(i, j) for i in range(-1, 2) for j in range (-1, 2) if i != j !=-i]
    floor_back_rects = []
    for i in range(1, len(base) - 1):
        for j in range(1, len(base[i]) - 1):
            if base[i][j] not in excluded:
                floor_bool = True
                for coord in rel_coords:
                    if base[i + coord[0]][j + coord[1]] == "black":
                        floor_bool = False
                if floor_bool:
                    floor_back_rects.append((j*40, i*40, (j+1)*40, (i+1)*40))
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
    functions, floor = var_init(files)
    floor_back_rects = background_gen(base, functions)
    win, screen = win_init(width, height)
    tiles = gen_tile_objs(functions, files)
    rects, tiles_id = gen_rects(base)
    for element in floor_back_rects:
        floor_rect = element
        floor.data["rect"] = floor_rect
        floor.AlphaBlit(screen)
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
        state = data["fields"][element]["defaultState"]
        base[coords[1]][coords[0]] = gate_states[state]
#        print base[coords[1]][coords[0]]
#        print coords
#        print element, data["fields"][element]["defaultState"]
    for element in data["portals"]:
        coords = string.split(element, ",")
        coords = [int(i) for i in coords]
        base[coords[1]][coords[0]] = "portal off"
        if "x" in data["portals"][element]["destination"]:
            base[coords[1]][coords[0]] = "portal on"
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

