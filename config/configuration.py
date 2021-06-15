import configparser
import os
import numpy as np
config_path = "./config.config"


def createConfigDefault():
    config = configparser.ConfigParser()
    config.add_section("Markers")
    config.add_section("Options")
    with open(config_path, "w") as config_file:
        config.write(config_file)


def checkConfig():
    if not os.path.exists(config_path):
        createConfigDefault()


def configSetHCVBounds(lower, upper):
    checkConfig()
    
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set("Markers", "hsv_lower", ' '.join(str(e) for e in lower.tolist()))
    config.set("Markers", "hsv_upper", ' '.join(str(e) for e in upper.tolist()))
    
    with open(config_path, "w") as config_file:
        config.write(config_file)
    
    
def configGetHCVBounds():
    checkConfig()

    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_option("Markers","hsv_lower") or\
        not config.has_option("Markers","hsv_lower"):
        return

    hsv_lower = config.get("Markers","hsv_lower").split()
    hsv_upper = config.get("Markers","hsv_upper").split()

    return np.array(hsv_lower), np.array(hsv_upper)


def configSetMarkerPoints(points):#[[526, 422], [47, 285], [579, 114], [199, 33]]
    checkConfig()
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    pointsstr = ""
    for point in points:
        for coord in point:
            pointsstr += str(coord)
            pointsstr += " "
        # pointsstr = pointsstr.join(str(e) for e in point)
        # # pointsstr = pointsstr.join(" ")

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
    points = []
    for i in range(4):
        points.append([int(res[2*i]), int(res[2*i + 1])])
    
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



def main():
    configSetValue("val1", "2e")
    print(configGetValue("val1"))
    pass

if __name__ == "__main__":
    main()