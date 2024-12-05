#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

script for preparing folders and dems for running the varyWnCfg.py script

call this script to prepare a set of dems with corresponding info files, within dem folders, within an overall dems_folder, where a given dem is named dem0, dem1, dem2, dem3, ... demN where N is the number of dems to use, the dems generated using a randomly generated list of lat/lon points with specified lat/lon buffer size.

NOTE, running this script deletes the dems_folder specified by dem_output_path, with all containing folders, in prep of generating a new set. If you want to preserve a set of output dems, copy and paste the dem_output_folder to a new location, giving it a new name to track past outputs.

NOTE, the lat/lon random point generation method currently just does regular random number generation sampling of a big specified bounding box. The choice of bounding box could be refined, and the randomizer method could also be refined.

DON'T FORGET TO DO THE FOLLOWING IN YOUR COMMAND LINE TO GET fetch_dem built from WindNinja TO WORK CORRECTLY
export CUSTOM_SRTM_API_KEY=$YOUR_OPEN_TOPOGRAPHY_API_KEY

A good way to run this script and save a log of the output:
   python3 prepare_varyWnCfg_dems.py 2>&1 | tee prepareDems_runLog.txt

"""

import os
import shutil

import random

import time



nDems = 100

latBuf = 30.0  ## km, would need to adapt the methods to use different values
lonBuf = 30.0  ## km

dem_output_path = "/data"

##dem_type = "gmted"
dem_type = "srtm"



### trying to pick these to avoid getting too much coastal water, and get more land, just eyeballing a map of lat/lon
overallWestLonBound = -125.0  ## -125.0 doesn't contain Alaska, and goes a hint off the west coast, way off the west coast below like 35 deg North, but should be good enough for a start
overallEastLonBound = -105.0  ## Natalie asked for this value to be -105
overallNorthLatBound = 49.0  ## looks like this value goes pretty constant for most of Washington till at least Minnesota, googling northernmost latitude of Montana I got 49.0 degrees
overallSouthLatBound = 35.0  ## 35.0 degrees is not an ideal value, cuts off a large section of California, Arizona, and New Mexico, pretty much all of Texas. But seems like a good starting point




def calc_latLonPoint( randomizer_method,  overallWestLonBound, overallEastLonBound, overallNorthLatBound, overallSouthLatBound ):
    
    
    if randomizer_method != "random":
        raise RuntimeError("!!! calc_latLonPoint() unknown input randomizer_method "+randomizer_method+"!!!\n  available input randomizer_methods are \"random\"")
    
    if overallWestLonBound >= overallEastLonBound:
        raise RuntimeError("!!! calc_latLonPoint() input overallWestLonBound and overallEastLonBound are not ordered from west to east or are equal !!!\n  overallWestLonBound = "+str(overallWestLonBound)+", overallEastLonBound = "+str(overallEastLonBound))
    
    if overallSouthLatBound >= overallNorthLatBound:
        raise RuntimeError("!!! calc_latLonPoint() input overallSouthLatBound and overallNorthLatBound are not ordered from south to north or are equal !!!\n  overallSouthLatBound = "+str(overallSouthLatBound)+", overallNorthLatBound = "+str(overallNorthLatBound))
    
    
    ### might need to adjust this method, I worry about too much repetition in some spots, wonder if a normal distribution or uniform distribution of some kind might be better?
    if randomizer_method == "random":
        lon = overallWestLonBound + (overallEastLonBound - overallWestLonBound)*random.random()
        lat = overallSouthLatBound + (overallNorthLatBound - overallSouthLatBound)*random.random()
    
    
    return ( lat, lon )




def main():
    
    
    dems_folder = dem_output_path+"/dems_folder"
    if os.path.exists(dems_folder):
        # folder exists, need to delete it, this will delete everything within the folder as well as the folder
        shutil.rmtree(dems_folder)
    ## now the folder with all files are deleted if they existed, can just make them as if they never were there, no need for a check just make them
    os.mkdir(dems_folder)
    
    
    ### probably better ways to do this, especially to get more control over the command line calls and information sharing, but for now, here it goes
    cmd_log_filename = dems_folder+"/fetch_dem_log.txt"
    cmd_log_file = open( cmd_log_filename, "w" )
    for idx in range(nDems):
        startTime = time.perf_counter()
        print("", flush=True)  ## add a new line before the dem download
        current_lat, current_lon = calc_latLonPoint( "random",  overallWestLonBound, overallEastLonBound, overallNorthLatBound, overallSouthLatBound )
        print("current_lat,lon = "+str(current_lat)+","+str(current_lon), flush=True)
        current_dem_folder = dems_folder+"/dem"+str(idx)
        print("current_dem_folder = \""+current_dem_folder+"\"", flush=True)
        os.mkdir(current_dem_folder)
        ## still seems like a good idea to at least save the lat/lon point information somewhere
        current_info_filename = current_dem_folder+"/info.txt"
        current_info_file = open( current_info_filename, "w" )
        current_info_file.write( "lat,lon = "+str(current_lat)+","+str(current_lon)+"\n" )
        current_info_file.write( "latBuf,lonBuf = "+str(latBuf)+","+str(lonBuf)+"\n" )
        current_info_file.write( "buf_units = km\n" )
        current_info_file.write( "dem_type = "+dem_type+"\n" )
        current_info_file.close()
        ## now print and do the command
        ## for debugging, can comment out the command while working out the call
        current_cmd = "fetch_dem --point "+str(current_lon)+" "+str(current_lat)+" "+str(lonBuf)+" "+str(latBuf)+" --buf_units kilometers --src "+dem_type+" "+current_dem_folder+"/dem"+str(idx)+".tif"
        print(current_cmd, flush=True)
        cmd_log_file.write( current_cmd+"\n" )
        os.system(current_cmd)
        endTime = time.perf_counter()
        print("dem download timer: "+str(endTime-startTime)+" seconds", flush=True)
        print("", flush=True)  ## add a new line after the dem download
    cmd_log_file.close()
    





if __name__ == '__main__':
    main()






