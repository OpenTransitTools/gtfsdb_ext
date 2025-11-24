

def make_pelias_csv_record(id="", name="", lat=0.0, lon=0.0, source="", layer="", aliases=None, popularity=-111):
    """
    create a csv format according to the Pelias csv loader specs
    https://github.com/pelias/csv-importer?tab=readme-ov-file#overview
    """
    ret_val = {"id": id, "name": name, "lat": lat, "lon": lon, "source": source, "layer": layer}

    # optional csv columns
    if aliases: ret_val["name_json"] = aliases
    if popularity >= 0: ret_val["popularity"] = popularity

    return ret_val


def to_alias_json(*names):
    """
    return a string that looks like ["alias X","alias Y","alias Z"] 
    """
    ret_val = ""
    if names and len(names) > 0:
        v = ','.join(['"{}"'.format(n) for n in names])
        ret_val = "[{}]".format(v)
    return ret_val
        

def direction_to_dir(direction, upper=True, def_val=""):
    ret_val = def_val
    if direction:
        if direction.lower() == "southeast":
            ret_val = "se"
        elif direction.lower() == "southwest":
            ret_val = "sw"
        elif direction.lower() == "northeast":
            ret_val = "ne"
        elif direction.lower() == "northwest":
            ret_val = "nw"
        elif direction.lower() == "north":
            ret_val = "n"
        elif direction.lower() == "south":
            ret_val = "s"
        elif direction.lower() == "east":
            ret_val = "e"
        elif direction.lower() == "west":
            ret_val = "w"

    if upper:
        ret_val = ret_val.upper()

    return ret_val
