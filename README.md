# PLUSH

## Project Structure

So starting from the top:

1. The compiler folder has everything related to the implementation of the compiler and some tests
2. The grammar folder has an incomplete sketch of the plush grammar

Inside the compiler folder:
1. compiler.py - runs all the pipeline from reading the source code from your plush program to generating its correspondent LLVM IR version.
2. plush_tokenizer.py - handles the compiler tokenization stage.
3. plush_parse.py - handles the compiler parsing stage (builds the AST).
4. plush_typechecker.py - handles the compiler typechecking stage.
5. plush_compiler.py - converts the typechecked AST to LLVM IR code.
6. plush.sh - automated script to compile and run your own plush program when inside the provided docker container (see the next section).
7. dockerfile - has all the commands to install the necessary tools to run the compiler and build the container image
8. tree_mode.py - python script that gets called when you want to just see the AST from your plush program.

## How compile a plush program

1. Write your plush program and save it in the folder compiler/programs as a .pl file. (see the next section)
2. Go to the compiler directory: `cd compiler`
3. Run the following command to build the docker image for the environment where the compiler is going to execute (it might take a bit of time): `docker build -t my_compiler_image .`
4. Run the container with the following command (after entering the command you will be presented with the container terminal): `docker run --rm -it --name my_compiler_container my_compiler_image`
5. Compile and run your program by entering the following command: `./plush.sh your_program.pl`
6. If just want to see the AST in a json format without compiling enter the following command: `./plush.sh --tree your_program.pl`


## Details when writting a plush program

1. When declaring (FFI or not) or defining a procedure you must write down its void type.
2. For every FFI that you want to use in your program, you must declare it before using it, else plush won't know that it exists.

### Author

Tomás Barreto - fc56282