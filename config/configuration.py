import configparser
import os
import numpy as np
config_path = "./config.config"


def createConfigDefault():
    config = configparser.ConfigParser()
    config.add_section("Markers")
    config.add_section("Options")
    config.add_section("Target")
    with open(config_path, "w") as config_file:
        config.write(config_file)


def checkConfig():
    if not os.path.exists(config_path):
        createConfigDefault()


def configSetMarkersHCVBounds(lower, upper):
    checkConfig()
    
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set("Markers", "hsv_lower", ' '.join(str(e) for e in lower.tolist()))
    config.set("Markers", "hsv_upper", ' '.join(str(e) for e in upper.tolist()))
    
    with open(config_path, "w") as config_file:
        config.write(config_file)
    
    
def configGetMarkersHCVBounds():
    checkConfig()

    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_option("Markers","hsv_lower") or\
        not config.has_option("Markers","hsv_lower"):
        return

    hsv_lower = config.get("Markers","hsv_lower").split()
    hsv_upper = config.get("Markers","hsv_upper").split()

    return np.array([int(hsv_lower[0]),int(hsv_lower[1]),int(hsv_lower[2])]),\
             np.array([int(hsv_upper[0]),int(hsv_upper[1]),int(hsv_upper[2])])


def poins_to_str(points):
    pointsstr = ""
    for point in points:
        for coord in point:
            pointsstr += str(coord)
            pointsstr += " "
    return pointsstr


def str_to_points(strpoint):
    points = []
    for i in range(4):
        points.append([int(strpoint[2*i]), int(strpoint[2*i + 1])])
    return points


def configSetMarkerPoints(points):#[[526, 422], [47, 285], [579, 114], [199, 33]]
    checkConfig()
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    pointsstr = poins_to_str(points)
    
    config.set("Markers", "points", pointsstr)

    with open(config_path, "w") as config_file:
        config.write(config_file)
    
    
def configGetMarkerPoints():
    checkConfig()

    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_option("Markers", "points"):
        return
    res = config.get("Markers", "points").split()
    points = str_to_points(res)
    
    return points

def configSetValue(name, value):
    checkConfig()

    config = configparser.ConfigParser()
    config.read(config_path)

    config.set("Options", name,value)
    
    with open(config_path, "w") as config_file:
        config.write(config_file)
    

def configGetValue(name):
    checkConfig()

    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_option("Options", name):
        return
    
    res = config.get("Options", name)
    return res


def configSetTargetHCVBounds(lower, upper):
    checkConfig()
    
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set("Target", "hsv_lower", ' '.join(str(e) for e in lower.tolist()))
    config.set("Target", "hsv_upper", ' '.join(str(e) for e in upper.tolist()))
    
    with open(config_path, "w") as config_file:
        config.write(config_file)
    
    
def configGetTargetHCVBounds():
    checkConfig()

    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_option("Target","hsv_lower") or\
        not config.has_option("Target","hsv_lower"):
        return

    hsv_lower = config.get("Target","hsv_lower").split()
    hsv_upper = config.get("Target","hsv_upper").split()

    return np.array([int(hsv_lower[0]),int(hsv_lower[1]),int(hsv_lower[2])]),\
             np.array([int(hsv_upper[0]),int(hsv_upper[1]),int(hsv_upper[2])])



def main():
    configSetValue("val1", "2e")
    print(configGetValue("val1"))
    pass

if __name__ == "__main__":
    main()