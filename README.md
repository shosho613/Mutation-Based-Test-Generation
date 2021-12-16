# Mutation Based Test Generation Pipeline

# Contact Information
Shoham Shitrit, University of Rochester '22
sshitrit@u.rochester.edu 
shohamshitrit1@gmail.com

# Prerequisites

### MUSIC
This tool relies on MUSIC to generate mutations of C programs. Follow the instructions here[https://github.com/swtv-kaist/MUSIC] to clone and build the tool. 

### Pycparser

This tool depends on pycparser to manipulate C programs and functions inside them.

Installing pycparser with `pip install` is suitable, but the tool relies on the fake standard library headers, which can only be accessed by cloning the pycparser repo here[https://github.com/eliben/pycparser]

* There was also a common parsing issue early in development along the lines of "Atomic Bool not recognized". This was fixed by calling pycparser from the cloned repo, and not the pip package. 


# To run script on standalone program:
Use runner.py
1. oracle program
2. function name
3. optional: test suite. If supplied, tool will attempt to boslter test suite with new inputs to cover survived mutations. Otherwise, the tool will create a new test suite in attempts to cover the total generated mutations.
4. optional: compilation-info. this is a place for compilation flags to be supplied.
For example, if the compilation command for the program is:
gcc program.c -lm -o program
Then "-lm" should be supplied as compilation info. 
There are more flags listed in `python3 runner.py -help`
Example command:
`python3 runner.py fma_rn_ftz_f32.c execute_fma_rn_ftz_f32 f32_3.ssv --compilation-info="testutils.c -lm" --new-input-filename="new_inputs.txt"`

# To run script on ROCetta instructions:
Use L2_runner.py
Currently, many path values are hard coded into the script. Feel free to adjust as needed to run on different file structures. 

* There is a "yaml" or "no-yaml" flag on this script. If "yaml" is present, test suite data is taken from the instructions.yaml file. 
Most uses should have the "no-yaml" flag, as it will utilize the gpusemtest python tools to extract instruction files. 
To run:
`python3 L2_runner.py <path to MUSIC> <path to fake_libc_headers> <yaml or no-yaml>`