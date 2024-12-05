#!/bin/bash

# Define source and destination details
REMOTE_USER="ohpc"
REMOTE_HOST="192.168.56.62"
SOURCE_BASE="/ohpc_nfs/WN_sims"
DEST_BASE="/data"

# List of specific folders to process
FOLDER_INDICES=(0 9 15 20 22 32 44 45 47 49 51 57 59 62 64 65 66 67 69 72 73 74 78 83 85 87 89 92 94 99 101 102 104 105 112 114 118 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 140 142 144 145 147 152 154 156 158 159 161 164 165 167 169 171 173 175 178 182 184 186 188 190 193 197 199 200)

# Loop through specified folder indices
for i in "${FOLDER_INDICES[@]}"; do
    echo "Processing folder $i..."

    # Define source paths on the remote server
    DEMS_FOLDER="${SOURCE_BASE}/${i}/dems_folder"
    DEM0_FOLDER="${DEMS_FOLDER}/dem0"

    # Define local destination paths
    LOCAL_DEST_DEMS="${DEST_BASE}/${i}/dems_folder/dem0"
    LOCAL_DEST_FOLDER="${DEST_BASE}/${i}/dems_folder"

    # Create local directory structure
    mkdir -p "$LOCAL_DEST_DEMS"

    # Use scp to copy the specific files
    scp "${REMOTE_USER}@${REMOTE_HOST}:${DEM0_FOLDER}/dem0.tif" "$LOCAL_DEST_DEMS/"
    scp "${REMOTE_USER}@${REMOTE_HOST}:${DEM0_FOLDER}/info.txt" "$LOCAL_DEST_DEMS/"
    scp "${REMOTE_USER}@${REMOTE_HOST}:${DEMS_FOLDER}/fetch_dem_log.txt" "$LOCAL_DEST_FOLDER/"
done

echo "Copy completed!"
