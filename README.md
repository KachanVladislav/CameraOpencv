# CameraOpencv
OpenCV(4.5.2), Python(3.9.5) wrapperspective by 4 points

config/ -- saving config

config.py - configuring marker point settings, getting perspective matrix
-options:
    --markershcv : interactive config for markers bound and save
    --markersreset : calculate markers points and save
    --targethcv : targethcv bound interactive config
    --show : for showing result
    --camnum : setting up camera number    

server.py - runs udp server, also thread that finding target poitns
ugp input messages:
    b'gt' - get target points
    b'gs' - get size of warped window
    