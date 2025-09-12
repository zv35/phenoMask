#!/usr/bin/env python3
# This is the core script that contains most functions, not ran as a script
from datetime import datetime, timedelta
from os import rename, walk

"""
import json
import bz2 # Compress cache files
class _cache:
    def __init__(self):
        pass
"""


class _phenoImage:
    def __init__(self, filePath, time):
        self.originalFilePath = filePath # Where the 
        self.finalFilePath = filePath
        self.time = time
        
    def __lt__(self, other):
        return self.time < other.time
        
    def __add__(self, other: timedelta):
        self.time = self.time + other
    
    def __sub__(self, other: timedelta):
        self.time = self.time - other


class phenoMask:
    maskedFiles = []
    disjoint = False # If the set is noncontiguious, such as after a union

    def __init__(self, sitename, startDate, endDate, startTime=timedelta(0), endTime=timedelta(hours=24)):
        self.sitename = sitename

        # Start date for including images
        startDate = datetime.strptime(startDate, '%Y-%m-%d')
        # End time for including images
        endDate = datetime.strptime(endDate, '%Y-%m-%d')
        
        # Convert startTime to datetime
        startTime = datetime.strptime(startTime, '
        # Convert endTime to datetime
        endTime = datetime.strptime(endTime, '%H:%M:%S')
        
        # Add start/end times to date
        startDate = startDate + startTime
        endDate = endDate + endTime
        
        # Check that dates are valid
        if startDate > endDate:
            # TODO
            raise Exception("Your start date must be before your end date!")
            return -1
            
        self.startDate = startDate
        self.endDate = endDate

    def __len__(self):
        # Length of mask is length of f
        return len(self.maskedFiles)
        
    # Make class iterable
    def __iter__(self):
        # For each file
        for maskedFile in self.maskedFiles:
            # Return file
            yield maskedFile 
    
    def __add__(self, other: type(self)):
        self.disjoint = True
        for maskedFile in other.maskedFiles:
            if not maskedFile in self.maskedFiles:
                self.maskedFiles.append(maskedFile)
        return self
    
    def __sub__(self, other: type(self)):
        self.disjoint = True
        for maskedFile in other.maskedFiles:
            if maskedFile in self.maskedFiles:
                self.maskedFiles.remove(maskedFile)
        return self
    
    def sort(self):
        """
        Sort the order of masked files as to minimize collisions.
        """
        return self.maskedFiles.sort()
    
    def gather(self, exclude=[], clear=False):
        """
        Search for files within the site directory.
        """
        for root, dirs, files in walk(self.sitePath, topdown=True):

    def apply(self):
        """
        Apply a function to all members of the mask
        """
        pass
    
    def collisions(self):
        """
        Checks for collisions when moving files in order.
        Does not actually move any files.
        """
        collisions = []
        for maskedFile in self.maskedFiles:
            if exists(maskedFile.newPath) and not maskedFile.newPath in oldPaths:
                collisions.append(maskedFile)
        return collisions
            

    def moveFiles(self, dryRun=True, pop=True):
        """
        Move all files in the mask to their new destination.
        """
        if not dryRun:
            for maskedFile in self.maskedFiles:
                if not maskedFile.oldPath == maskedFile.newPath:
                    rename(maskedFile.oldPath, maskedFile.newPath)
            return 0
        else:
            return -1
        

