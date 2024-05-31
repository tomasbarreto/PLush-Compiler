# PLUSH

## Project Structure

So starting from the top:

1. The compiler folder has everything related to the implementation of the compiler and some tests.
2. plush.sh - automated shell script to compile and run your own plush program when inside the provided docker container.
3. setup.sh - automated shell script that builds and runs the docker container where the compiler will be executed.
4. README.md
5. dockerfile - has all the commands to install the necessary tools to run the compiler and build the container image.
6. Report-LiquidTypeChecking.pdf - Project's phase 5 report.

Inside the compiler folder:
1. compiler.py - runs all the pipeline from reading the source code from your plush program to generating its correspondent LLVM IR version.
2. plush_tokenizer.py - handles the compiler tokenization stage.
3. plush_parse.py - handles the compiler parsing stage (builds the AST).
4. plush_typechecker.py - handles the compiler typechecking stage.
5. plush_compiler.py - converts the typechecked AST to LLVM IR code.
6. tree_mode.py - python script that gets called when you want to just see the AST from your plush program.
7. c_functions - is the folder where u will find the plush ffi library.
8. grammar - The grammar folder has an incomplete sketch of the plush grammar.

## How compile a plush program

1. Download the project and unzip it.
2. Write your plush program and save it in the project root folder (plush directory where you have the setup.sh, this README.md, ...) as a .pl file. (see the next section)
4. Open a terminal in the project root (plush directory, the one from the previous step) and enter the following command: ./setup.sh (this command will build and execute the docker container with everything prepared to run the compiler).
5. Compile and run your program by entering the following command: `./plush.sh your_program.pl`
6. If just want to see the AST in a json format without compiling enter the following command: `./plush.sh --tree your_program.pl`


## Details when writting a plush program

1. When declaring (FFI or not) or defining a procedure you must write down its void type.
2. For every FFI that you want to use in your program, you must declare it before using it, else plush won't know that it exists.

### Author

Tomás Barreto - fc56282