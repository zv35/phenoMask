#!/usr/bin/env python3
# This script will offset the given range of images in the PhenoCam archive (if the timezone was set incorrectly)

from datetime import datetime, timedelta
import argparse
from os import path, walk
import shutil


ARCHIVE = "/projects/phenocam/data/archive/"


parser = argparse.ArgumentParser(prog="dateOffset.py",
    description="Offset a given range of images in the PhenoCam archive (if the timezone was set incorrectly)")
# Sitename to change
parser.add_argument('sitename', action='store',
    help="The site name which you want to make a timelapse of (case sensitive).")
# First date to start video (or earleist the site has)
parser.add_argument('startDate', action='store', default="2000-01-01",
    help="The first day to include. Format: YYYY-MM-DD")
# The last date to end the video with (or present date)
parser.add_argument('endDate', action='store', default="9999-12-31",
    help="The Last day to include. Format: YYYY-MM-DD")
# Time offset
parser.add_argument('offset', action='store', default="00:00",
    help="Time difference, HH:MM")
parser.add_argument('--negative', action='store_true',
    help="Flip direction of offset (i.e. +08:00 becomes -08:00)")
# Terminal verbosity
parser.add_argument('--verbose', '-v', action='count', default=0,
    help="Post more messages useful for debugging")
# Dry Run
parser.add_argument('--dry-run', '-n', action='store_true',
    help="Don't actually move files.")
# Continue on error
parser.add_argument('--overwrite', action='store_true',
    help="If a file already exists in place, overwrite it with the new one (NOT RECCOMENDED)")

args = parser.parse_args()


# Start date for including images
startDate = datetime.strptime(args.startDate,'%Y-%m-%d')
# End time for including images
endDate = datetime.strptime(args.endDate,'%Y-%m-%d')
# Check that dates are valid
if startDate > endDate:
    raise Exception("Your start date must be before your end date!")
# Convert offset to time delta
    # Check which way to offset
sign = -1 if args.negative else +1
    # Split the offset into hours and minutes
hours, minutes = map(int, args.offset[1:].split(':'))
    # Convert to timedelta
td = timedelta(hours=sign * hours, minutes=sign * minutes)
# Absolute filesystem path to the site, i.e. /data/archive/harvard/
sitePath = path.join(ARCHIVE, args.sitename)


for root, dirs, files in walk(sitePath):
    for file in files:
        # Make sure the file is a jpeg
        if file.endswith(".jpg") and not "ROI" in file and not "cli" in file:
            if "IR" in file:
                imageDate = datetime.strptime(file, args.sitename+'_IR_%Y_%m_%d_%H%M%S.jpg')
            else:
                imageDate = datetime.strptime(file, args.sitename+'_%Y_%m_%d_%H%M%S.jpg')
            if startDate <= imageDate <= endDate:
                imageDate = imageDate + td
                if args.verbose > 0:
                    print(f"Original: {imageDate - td}\tModified: {imageDate}")
                if "IR" in file:
                    newFile = datetime.strftime(imageDate, args.sitename+'_IR_%Y_%m_%d_%H%M%S.jpg')
                else:
                    newFile = datetime.strftime(imageDate, args.sitename+'_%Y_%m_%d_%H%M%S.jpg')
                oldFilePath = path.join(root, '/'.join(dirs), file)
                newFilePath = path.join(sitePath, str(imageDate.year), str(imageDate.month).zfill(2), newFile)
                if args.verbose > 0:
                    print(f"\tNew file path: {newFilePath}")
                if args.overwrite or not path.exists(newFile):
                    if not args.dry_run:
                        shutil.move(oldFilePath, newFilePath)
                    elif args.verbose > 1:
                        print(f"!!! Did not move file: {file} (Dry-run)")
                else:
                    print(f"!!! File already exists: {newFile} (did NOT move)")
            elif args.verbose > 1:
                print(f"Skipped: {file}")

