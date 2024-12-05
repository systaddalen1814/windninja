#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

script for reading in a generic Domain Average Initialization WindNinja cfg file, varying the inputs, including the dem

varying the dem is the trickiest part, it requires the input dems to be in a specific dems_folder each in separate folders labeled dem0, dem1, dem2, dem3 ... demN, where N is the number of dems to use

then the various cases of wind speed and z0 are generated and placed into each of these dem folders for a given dem

To generate the dems, it is recommended to prepare and use the prepare_varyWnCfg_dems.py script


NOTE, normally, a call to "export VTK_OUT_AS_UTM=TRUE" would need to be done in the command line before running the script, but currently this is handled directly by the python script
Fortunately, looks like python system calls environment is better set than R, didn't have to track down all the fun path stuff to run openfoam for this script like I did when doing similar stuff in R


A good way to run this script and save the WindNinja log output, well for all the runs at once at least:
   python3 run_varyWnCfg.py 2>&1 | tee varyWnCfg_runLog.txt

"""

### helpful install packages
### sudo apt update
### sudo apt upgrade
### sudo apt install python3
### sudo apt install python3-dev
### sudo apt install python3-matplotlib  ## not sure this one is really needed for this script

import os
import shutil

import numpy as np

import time



### leave this as "" if you want to use the system WindNinja rather than your own separate local WindNinja build
##pathToCurrentWindNinjaBuild = "~/src/miscFixes/build"
pathToCurrentWindNinjaBuild = ""

dems_folder = "/output/dems_folder"

base_cli_file = "./base_cli.cfg"

wind_dirs = np.linspace(0.0,337.5,16)
nWindDirs = len(wind_dirs)

def main():
    
    if os.path.exists(dems_folder) == False:
        raise RuntimeError("!!! input dems_folder \""+dems_folder+"\" does not exist !!!")
    if os.path.isfile(base_cli_file) == False:
        raise RuntimeError("!!! input base_cli_file \""+base_cli_file+"\" does not exist !!!")
    ### need to find the paths and numbers of dem folders to output simulations to
    ### huh, thought I would need one more filter, like if the directory had "dem" in its name, but seems to have worked fine as is
    dem_base_foldernames = [ d for d in os.listdir(dems_folder) if os.path.isdir(os.path.join(dems_folder,d)) ]
    #print(dem_base_foldernames)   ## these happen to also be the dem base filenames with my current organization
    
    ### need to sort them into numerical order, but still keep them as strings, looks like regular sort function to sort as string order does the numerical sort of the end chars correctly
    dem_base_foldernames.sort()
    #print(dem_base_foldernames)
    
    nDems = len(dem_base_foldernames)
    dem_foldernames = [ os.path.join(dems_folder,d) for d in dem_base_foldernames ]
    #print(dem_foldernames)
    dem_filenames = []
    for idx in range(nDems):
        current_dem_filename = dem_foldernames[idx]+"/dem"+str(idx)+".tif"
        dem_filenames.append( current_dem_filename )
    #print(dem_filenames)
    
    
    vegetationTypes = ["grass","brush","trees"]
    simTypes = ["mass","momentum"]
    
    ### need to set a CPLConfigOption, looks like I found a way to do so before all the simulations that sticks for each later python system call
    ### This is the equivalent of running "export VTK_OUT_AS_UTM=TRUE" in the command line before running WindNinja
    os.environ["VTK_OUT_AS_UTM"] = "TRUE"
    
    ### kay, now to run each given simulation, making and tracking various foldernames and cfg filenames as needed
    for demIdx in range(nDems):
    # for demIdx in range(1):  ## for debugging, don't want to run near so many
    #for demIdx in range(1,2,1):
        
        current_dem_foldername = dem_foldernames[demIdx]
        current_dem_filename = dem_filenames[demIdx]
        #print(current_dem_foldername)
        #print(current_dem_filename)
        
        ### if already exists the folders, clean them up to start over. Fortunately the other stuff is still left to use that is outside these main folders
        for simTypeIdx in range(len(simTypes)):
            current_simType = simTypes[simTypeIdx]
            current_simType_folder = current_dem_foldername+"/"+current_simType
            if os.path.exists(current_simType_folder):
                # folder exists, need to delete it, this will delete everything within the folder as well as the folder
                shutil.rmtree(current_simType_folder)
            ## now the folder with all files are deleted if they existed, can just make them as if they never were there, no need for a check just make them
        
        for simTypeIdx in range(len(simTypes)):
            
            current_simType = simTypes[simTypeIdx]
            
            current_simType_folder = current_dem_foldername+"/"+current_simType
            os.mkdir(current_simType_folder)
            
            for vegIdx in range(len(vegetationTypes)):
                
                current_veg_type = vegetationTypes[vegIdx]
                
                current_veg_directory = current_simType_folder+"/"+current_veg_type
                os.mkdir(current_veg_directory)
                
                for windDirIdx in range(nWindDirs):
                    
                    current_wind_dir = wind_dirs[windDirIdx]
                    
                    current_wind_directory = current_veg_directory+"/"+str(current_wind_dir).replace(".","o")+"deg"
                    os.mkdir(current_wind_directory)
                    
                    current_output_directory = current_wind_directory
                    
                    current_cfg_filename = current_output_directory+"/cli.cfg"
                    shutil.copyfile(base_cli_file, current_cfg_filename)
                    
                    with open(current_cfg_filename, 'r') as file:
                        filedata = file.read()
                    filedata = filedata.replace("$dem_file",current_dem_filename)
                    if current_simType == "momentum":
                        filedata = filedata.replace("#momentum_flag              = true","momentum_flag              = true")  ## uncomment it out
                    filedata = filedata.replace("$vegetation_type",current_veg_type)
                    filedata = filedata.replace("$wind_dir",str(current_wind_dir))
                    filedata = filedata.replace("$output_directory",current_output_directory)
                    with open(current_cfg_filename, 'w') as file:
                        file.write(filedata)
                    
                    wnBuildPath = pathToCurrentWindNinjaBuild
                    if wnBuildPath != "":
                        wnBuildPath = wnBuildPath+"/src/cli/"
                    current_cmd = wnBuildPath+"WindNinja_cli "+current_cfg_filename
                    print("", flush=True)  ## add a new line before the WindNinja run
                    print("running \""+current_simType+"\" simulation for dem \"dem"+str(demIdx)+"\" vegType \""+current_veg_type+"\" windDir \""+str(current_wind_dir)+" deg\"", flush=True)
                    startTime = time.perf_counter()
                    os.system(current_cmd)
                    endTime = time.perf_counter()
                    print("python os.system() timer: "+str(endTime-startTime)+" seconds", flush=True)
                    print("", flush=True)  ## add a new line after the WindNinja run
                    
                    if current_simType == "momentum":
                        startTime = time.perf_counter()
                        ## if it's a momentum solver run, the NINJAFOAM directory needs to be found from the dem location, and deleted, don't want to carry around such big files
                        current_foam_output_directory = [ d for d in os.listdir(current_dem_foldername) if "NINJAFOAM" in d ]
                        current_foam_output_directory = [ os.path.join(current_dem_foldername,d) for d in current_foam_output_directory ][0]
                        shutil.rmtree( current_foam_output_directory )
                        endTime = time.perf_counter()
                        print("python delete NINJAFOAM dir timer: "+str(endTime-startTime)+" seconds", flush=True)
                        print("", flush=True)  ## add a new line
                    
                    ## also delete all the ascii cloud output files, don't need to keep them around
                    ## might see this automatically dropped from within WindNinja itself in the future, for now just find and delete the files
                    current_cloud_files = [ f for f in os.listdir(current_output_directory) if "cld" in f ]
                    current_cloud_files = [ os.path.join(current_output_directory,f) for f in current_cloud_files ]
                    for idx in range(len(current_cloud_files)):
                        os.remove( current_cloud_files[idx] )
                    
                    ## looks like also want to delete the surface vtk files, can just use the dem tiff files if need the surface
                    current_vtk_files = [ f for f in os.listdir(current_output_directory) if "surf.vtk" in f ]
                    current_vtk_file = [ os.path.join(current_output_directory,f) for f in current_vtk_files ][0]
                    os.remove( current_vtk_file )

if __name__ == '__main__':
    main()







