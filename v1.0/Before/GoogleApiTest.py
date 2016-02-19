# -*- coding: utf-8 -*-
import urllib

params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
f = urllib.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=台灣台大&key=AIzaSyDU0SvmkoV9K_hm5xqDM39_-acX5HF7IW4")
print f.read()