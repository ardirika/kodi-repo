#!/bin/sh
# rm -rf _repo
rsync -av --exclude=repository.boogie --exclude=repository.vms ~/Library/Application\ Support/Kodi/addons/ .
cd _tools 
python generate_repo.py
cd -
