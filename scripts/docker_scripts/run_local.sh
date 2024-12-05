#!/bin/bash

# List of specific simulations to run
SIMULATION_NUMBERS=(0 9 15 20 22 32 44 45 47 49 51 57 59 62 64 65 66 67 69 72 73 74 78 83 85 87 89 92 94 99 101 102 104 105 112 114 118 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 140 142 144 145 147 152 154 156 158 159 161 164 165 167 169 171 173 175 178 182 184 186 188 190 193 197 199 200)

PARALLEL_TASKS=11  # Adjust to the number of available CPU cores
SINGULARITY_IMAGE="/home/sathwik/Latest/windninja/wn_latest1.sif"
SCRIPT_PATH="/home/sathwik/Latest/scripts/run.sh"

# Function to run a single simulation
run_simulation() {
    local simulation=$1
    singularity exec \
        -B /etc/passwd:/etc/passwd \
        -B /etc/group:/etc/group \
        -B "/data/${simulation}:/output" \
        -B /test:/home/sathwik/Latest/ \
        /home/sathwik/Latest/windninja/wn_latest1.sif \
        /home/sathwik/Latest/scripts/run.sh
}

# Export the function so GNU Parallel can use it
export -f run_simulation

# Check Singularity image exists
if [ ! -f "$SINGULARITY_IMAGE" ]; then
    echo "Error: Singularity image not found at $SINGULARITY_IMAGE"
    exit 1
fi

# Run specified simulations in parallel
printf "%s\n" "${SIMULATION_NUMBERS[@]}" | parallel -j "$PARALLEL_TASKS" run_simulation {}
