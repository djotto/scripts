#!/bin/bash

# Check if the number of iterations and the command are provided as command line arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <iterations> <command>"
    echo "Example: $0 1000 'git info'"
    exit 1
fi

iterations=$1
shift
command=$@

# Variables to store cumulative times
total_real=0
total_user=0
total_sys=0

# Function to convert time format mm:ss.sss to seconds
convert_time() {
    local time_str=$1
    local min=$(echo $time_str | awk -F'm' '{print $1}')
    local sec=$(echo $time_str | awk -F'm' '{print $2}' | awk -Fs '{print $1}')
    echo "scale=3; $min*60 + $sec" | bc
}

# Run the command for the specified number of iterations
echo "Running '$command' $iterations times..."

for i in $(seq 1 $iterations)
do
    # Capture the time output
    result=$( (time $command) 2>&1 )
    
    # Extract real, user, and sys times
    real_time=$(echo "$result" | grep real | awk '{print $2}')
    user_time=$(echo "$result" | grep user | awk '{print $2}')
    sys_time=$(echo "$result" | grep sys | awk '{print $2}')
    
    # Convert times to seconds
    real_sec=$(convert_time "$real_time")
    user_sec=$(convert_time "$user_time")
    sys_sec=$(convert_time "$sys_time")
    
    # Add to cumulative times
    total_real=$(echo "$total_real + $real_sec" | bc)
    total_user=$(echo "$total_user + $user_sec" | bc)
    total_sys=$(echo "$total_sys + $sys_sec" | bc)
done

# Calculate averages
average_real=$(echo "scale=3; $total_real / $iterations" | bc)
average_user=$(echo "scale=3; $total_user / $iterations" | bc)
average_sys=$(echo "scale=3; $total_sys / $iterations" | bc)

# Print averages
echo "Average real time: $average_real seconds"
echo "Average user time: $average_user seconds"
echo "Average sys time: $average_sys seconds"
