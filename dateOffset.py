#!/usr/bin/env python3
# This script will offset the given range of images in the PhenoCam archive (i.e. if the timezone was set incorrectly)

from datetime import datetime, timedelta
import argparse
from os import path, walk, rename
from sys import stderr, exit
#import shutil # Removed for data saftey


# Path to the PhenoCam archive
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
# Positive/Negative Offset
direction = parser.add_mutually_exclusive_group(required=True)
direction.add_argument('--negative', action='store_true',
    help="Flip direction of offset (i.e. +08:00 becomes -08:00)")
# Variable not used except to force the user to select either positive or negative
direction.add_argument('--positive', action='store_true',
    help="Add offset to the original time")
# Terminal verbosity
parser.add_argument('--verbose', '-v', action='count', default=0,
    help="Post more messages useful for debugging")
# Dry Run
parser.add_argument('--dry-run', '-n', action='store_true',
    help="Don't actually move files.")
# Continue on error, very dangerous!!
parser.add_argument('--overwrite', action='store_true',
    help=argparse.SUPPRESS)
metaSelection = parser.add_mutually_exclusive_group(required=False)
# Move only meta data files. NOT RECCOMENDED FOR PRODUCTION USE!
metaSelection.add_argument('--meta-only', action='store_true', default=False,
    help=argparse.SUPPRESS)
# move only image files. NOT RECCOMENDED FOR PRODUCTION USE!
metaSelection.add_argument('--image-only', action='store_true', default=False,
    help=argparse.SUPPRESS)
# Hide warning about data saftey, hidden from help
metaSelection.add_argument('--ignore-warning', action='store_true', default=False,
    help=argparse.SUPPRESS)

args = parser.parse_args()
if not args.ignore_warning:
    # Display data saftey warning
    stderr.write("WARNING!!!\nThis script renames files in the PhenoCam data archive. There is potential risk of data loss if you are not careful! Always ensure there is an up-to-date backup before continuing. Please read through README.md for a full description of all flags, and check the output of your command with a dry-run first.\nThis script will return now. You may suppress this message by appending `--ignore-warning` to your previous command.\n")
    if args.verbose > 0:
        print(f"Archive path: {ARCHIVE}")
    exit()


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
# Absolute file system path to the site, i.e. /data/archive/harvard/
sitePath = path.join(ARCHIVE, args.sitename)



if "__main__" in __name__:
    if args.verbose > 1:
        print(f"Archive path: {ARCHIVE}\n")

    # Every file in the site dir
    for root, dirs, files in walk(sitePath, topdown=True):
        dirs.sort()
        files.sort()
        for file in files:
            # Make sure the file is a JPEG, not center line
            if file.endswith(".jpg") and not "ROI" in file and not "cli" in file:
                # IR images have a different file name
                try:
                    if "IR" in file:
                        imageDate = datetime.strptime(file, args.sitename+'_IR_%Y_%m_%d_%H%M%S.jpg')
                    else:
                        imageDate = datetime.strptime(file, args.sitename+'_%Y_%m_%d_%H%M%S.jpg')
                except ValueError:
                    if args.verbose > 0:
                        print(f"!!! File does not follow standard naming: {file} (skipped)")
                    continue
                # Check that date is within range
                if startDate <= imageDate <= endDate:
                    # Add the delta to the image time
                    imageDate = imageDate + td
                    if args.verbose > 0:
                        print(f"Original: {imageDate - td}\tModified: {imageDate}")
                    # Save IR images to a different file name
                    if "IR" in file:
                        newFile = datetime.strftime(imageDate, args.sitename+'_IR_%Y_%m_%d_%H%M%S.jpg')
                    else:
                        newFile = datetime.strftime(imageDate, args.sitename+'_%Y_%m_%d_%H%M%S.jpg')
                    # get full path for original image
                    oldFilePath = path.join(root, '/'.join(dirs), file)
                    # Path to move to, may be in a different directory (such as moving back a month)
                    newFilePath = path.join(sitePath, str(imageDate.year), str(imageDate.month).zfill(2), newFile)
                    # Meta file paths
                    oldMetaPath = oldFilePath.replace('.jpg', '.meta')
                    newMetaPath = newFilePath.replace('.jpg', '.meta')

                    if args.verbose > 0:
                        print(f"\tNew image path: {newFilePath}")
                        print(f"\tNew meta path : {newMetaPath}")
                    # Don't overwrite images
                    if not args.meta_only and (args.overwrite or not path.exists(newFilePath)):
                        if not args.dry_run:
                            # Move the image
                            rename(oldFilePath, newFilePath)
                        elif args.verbose > 1:
                            print(f"!!! Did not move image: {file} (Dry-run)")
                    elif not args.meta_only:
                        print(f"!!! Image already exists: {newFile} (did NOT move)")
                    # Don't overwrite meta files, sometimes meta files don't exist or match the image
                    if path.exists(oldMetaPath) and not args.image_only and (args.overwrite or not path.exists(newMetaPath)):
                        if not args.dry_run:
                            # Move the meta file
                            rename(oldMetaPath, newMetaPath)
                        elif args.verbose > 1:
                            print(f"!!! Meta file not moved: {path.basename(oldMetaPath)} (Dry-run)")
                    elif not path.exists(oldMetaPath):
                        print(f"!!! Meta file not found: {path.basename(oldMetaPath)}")
                    elif not args.image_only:
                        print(f"!!! Meta file already exists: {path.basename(newMetaPath)} (did NOT move)")
                # Image not within range
                elif args.verbose > 1:
                    print(f"Skipped: {file}")

