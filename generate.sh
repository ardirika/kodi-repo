#!/bin/sh
# rm -rf _repo
rsync -av --exclude=repository.vms --exclude=repository.bluecop.xbmc-plugins ~/Library/Application\ Support/Kodi/addons/ .
cd _tools 
python generate_repo.py
cd -
