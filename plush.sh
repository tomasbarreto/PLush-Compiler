
usage() {
  echo "Usage: plush [OPTIONS]... FILE.pl"
  echo "Options:"
  echo "  --tree    Enable tree mode"
  exit 1
}

tree_mode=false
params=()

for arg in "$@"; do
  if [[ "$arg" == "--tree" ]]; then
    tree_mode=true
  elif [[ "$arg" == *.pl ]]; then
    pl_file="$arg"
  else
    params+=("$arg")
  fi
done

if [[ ! "$pl_file" == *.pl ]]; then
  echo "Error: The last parameter must be a .pl file"
  usage
fi

if $tree_mode; then
  python3 compiler/tree_mode.py "$pl_file"
else
  python3 compiler/compile.py "$pl_file"
  cd compiler/c_functions
  gcc -c plush_library.c -o plush_library.o
  cd ..
  /usr/lib/llvm-18/bin/llc -o=program.s output.ll
  $CC -o program program.s c_functions/plush_library.o -lm
  ./program
fi
