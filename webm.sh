#!/bin/bash
ffmpeg -framerate 24 -f image2 -i ./out/image_%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p output.webm
