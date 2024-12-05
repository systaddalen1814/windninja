import os
from collections import defaultdict

# Base directory path
base_path = "/mnt/nfs_share"  # Update this to your actual base path

# Vegetation types and wind directions
vegetation_types = ["grass", "brush", "trees"]
wind_directions = [
    "0o0deg", "22o5deg", "45o0deg", "67o5deg", "90o0deg",
    "112o5deg", "135o0deg", "157o5deg", "180o0deg",
    "202o5deg", "225o0deg", "247o5deg", "270o0deg",
    "292o5deg", "315o0deg", "337o5deg"
]

# Required files in each wind direction folder
required_files = ["cli.cfg", "*.vtk", "*ang.asc", "*ang.prj", "*vel.asc", "*vel.prj"]

# Function to check simulations
def check_simulations():
    properly_run_simulations = set()  # Set to store successfully run simulations
    all_simulations = set(range(201))  # All simulation IDs from 0 to 200
    problematic_simulations = set()  # Set to store simulations with issues
    
    for sim_dir in range(201):  # Simulations 0 to 200
        sim_path = os.path.join(base_path, f"WN_sims/{sim_dir}/dems_folder/dem0/momentum")
        
        if not os.path.exists(sim_path):
            problematic_simulations.add(sim_dir)
            continue  # Skip simulations with no momentum folder
        
        for vegetation in vegetation_types:
            veg_path = os.path.join(sim_path, vegetation)
            if not os.path.exists(veg_path):
                problematic_simulations.add(sim_dir)
                break  # Stop checking further for this simulation
            
            for wind_dir in wind_directions:
                wind_path = os.path.join(veg_path, wind_dir)
                if not os.path.exists(wind_path):
                    problematic_simulations.add(sim_dir)
                    break
                
                # Check required files in the wind_dir
                missing_files = [
                    file for file in required_files
                    if not any(
                        fname.endswith(file.split(".")[-1]) for fname in os.listdir(wind_path)
                    )
                ]
                if missing_files:
                    problematic_simulations.add(sim_dir)
                    break
            
            if sim_dir in problematic_simulations:
                break  # No need to continue checking this simulation

    # Simulations with no issues
    properly_run_simulations = all_simulations - problematic_simulations
    return properly_run_simulations

# Function to summarize properly run simulations
def summarize_properly_run_simulations(properly_run_simulations, output_file="properly_run_simulations.txt"):
    with open(output_file, "w") as f:
        f.write("Properly Run Simulations:\n")
        f.write(f"  Total properly run simulations: {len(properly_run_simulations)}\n")
        f.write(f"  Simulations: {', '.join(map(str, sorted(properly_run_simulations)))}\n")
    
    print(f"Results written to {output_file}")

# Main execution
properly_run_simulations = check_simulations()
summarize_properly_run_simulations(properly_run_simulations)
