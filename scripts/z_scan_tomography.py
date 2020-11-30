import pylablib.aux_libs.devices.DCAM as cam
from pylablib.aux_libs.devices.DCAM_lib import lib, DCAMLibError

import matplotlib.pyplot as plt
import sys

npos = 80
step = -50 # micron
fig, ax = plt.subplots(npos, figsize=(10, 10*npos))

def zscan_noframe(cam0, npos: int, step: int, unit: str = ['m', 'u', 'c'])
    cam0.stop_acquisition()
    unit_dict = {'c': Units.LENGTH_CENTIMETRES, 'm': Units.LENGTH_MILLIMETRES, 'u': Units.LENGTH_MICROMETRES}

    zdrive.move_absolute(2.54, Units.LENGTH_CENTIMETRES)

    zscan = []
    zmx = []
    for i in range(npos):

        frame = cam0.snap(nframes=1)

        #bar = ax[i].imshow(frame[0])
        #plt.colorbar(bar, ax=ax[i])
        zscan.append(frame[0])
        zmx.append(frame[0].sum())
        zdrive.move_relative(step, u)
        zdrive.wait_until_idle()

def zscan_store_frames(cam0, npos: int, step: )
    zdrive.move_absolute(2.54, Units.LENGTH_CENTIMETRES)

    zscan = []
    zmx = []
    for i in range(npos):

        frame = cam0.snap(nframes=1)

        #bar = ax[i].imshow(frame[0])
        #plt.colorbar(bar, ax=ax[i])
        zscan.append(frame[0])
        zmx.append(frame[0].sum())
        zdrive.move_relative(step, Units.LENGTH_MICROMETRES)
        zdrive.wait_until_idle()
