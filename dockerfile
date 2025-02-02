# Use the official Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    gnupg \
    lsb-release \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install GCC
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Clang
RUN apt-get update && apt-get install -y \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Add LLVM apt repository and install LLVM 18.1.0
RUN wget https://apt.llvm.org/llvm.sh && \
    chmod +x llvm.sh && \
    ./llvm.sh 18 && \
    rm llvm.sh

# Install Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Verify the installations
RUN gcc --version && \
    g++ --version && \
    clang --version && \
    /usr/lib/llvm-18/bin/llvm-config --version && \
    python3 --version && \
    pip3 --version 

RUN pip3 install z3-solver

# Clean up unnecessary files
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the /compiler directory from the host to the container
COPY . /workspace/compiler

# Set working directory
WORKDIR /workspace/compiler

# Set environment variables to use Clang as the default compiler
ENV CC=clang
ENV CXX=clang++

# Default command
CMD ["/bin/bash"]

# Build and run commands
# docker build -t my_compiler_image .
# docker run --rm -it --name my_compiler_container my_compiler_image