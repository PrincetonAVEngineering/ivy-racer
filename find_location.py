# do pip3 install geocoder in terminal before running

import geocoder

def get_coordinates():
    g = geocoder.ip('me')
    return g.latlng
 