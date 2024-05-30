#!/bin/bash

# Function to display usage
usage() {
  echo "Usage: plush [OPTIONS]... FILE.pl"
  echo "Options:"
  echo "  --tree    Enable tree mode"
  exit 1
}

# Initialize variables
tree_mode=false
params=()

# Iterate over all the arguments
for arg in "$@"; do
  if [[ "$arg" == "--tree" ]]; then
    tree_mode=true
  elif [[ "$arg" == *.pl ]]; then
    pl_file="$arg"
  else
    params+=("$arg")
  fi
done

# Check if the last parameter is a .pl file
if [[ ! "$pl_file" == *.pl ]]; then
  echo "Error: The last parameter must be a .pl file"
  usage
fi

# Display parsed information
echo "Tree mode: $tree_mode"
echo "Parameters: ${params[@]}"
echo "PL file: $pl_file"

# Execute the appropriate Python script based on the presence of --tree
if $tree_mode; then
  echo "Executing tree_mode_script.py with $pl_file"
  python3 tree_mode.py "$pl_file"
else
  echo "Executing normal_mode_script.py with $pl_file"
  python3 compile.py "$pl_file"
  cd c_functions
  gcc -c plush_library.c -o plush_library.o
  cd ..
  llc -o=program.s output.ll
  CC -o program program.s c_functions/plush_library.o
  ./program
fi
