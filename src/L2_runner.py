
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from program_manipulation import ProgramManipulator
from runner import *
from shutil import copy
from os.path import isfile, join
import subprocess
import os
import re
import yaml
import time
import multiprocessing as mp
import threading
import queue


def process_instructions_yaml(yaml_file):
    file = open(yaml_file,"r")
    insn_info = yaml.safe_load(file)
    return insn_info

def get_input_path(insn_info, insn):
    for entry in insn_info:
        if entry['insn'] == insn:
            return entry['tests'][0]['input']
    return None


def compile_mutated_binary(mutation,function_name, insn, ptxc_pm, command_change_dir_to_ptx, mutated_binary_folder, make_command, path_to_fakeheaders):
    try:
        print(f"Compiling {mutation}")
        mutation_pm = ProgramManipulator(mutation, path_to_fakeheaders)
        # extract mutated function from mutated folder
        mutated_func_node = mutation_pm.get_function_ast(function_name)
        # replace in ptx.c
        ptxc_pm = ptxc_pm.replace_function(mutated_func_node, function_name)
        # stitch together ast and write to ptxc.c
        new_ptxc_program = ptxc_pm.create_string_from_program()
        # write to ptxc.c
        f = open(path_to_ptxc, "w+")
        f.write(new_ptxc_program)
        f.close()

        # get MUTxxx
        # add_rm_ftz_sat_f32.MUT2.c
        pattern="\w*.(\w*).\w*"
        mutation_filename = ProgramManipulator.extract_last_file_from_prog_path(mutation)
        mutation_number = re.search(pattern, mutation_filename).group(1)
        # get make command for specific insn 
        subprocess.call(f"{command_change_dir_to_ptx} && {make_command}", shell=True, timeout=5)
        subprocess.call(f"{command_change_dir_to_ptx} && mv {insn} {insn}_{mutation_number}.exe && mv {insn}_{mutation_number}.exe {mutated_binary_folder}/", shell=True)
        print(f"Created executable: {insn}_{mutation_number}.exe")
    except Exception as e:
        print(f"Exception in compile mutated binary {mutation}")
        print(e)
        raise e

def run_single_insn(insn, ptxc_pm, path_to_ptx_semantics, path_to_MUSIC, path_to_fakeheaders, file_dependencies, pre_compile_flags, test_suite_path, result_dict):
    mutation_directory_name = f"mutated-programs-{insn}"
    working_dir_name = f"working-directory-{insn}/"
    if not os.path.isdir(f"./{working_dir_name}"):
        os.mkdir(f"./{working_dir_name}")
    else:
        os.system(f"rm -rf {working_dir_name}")
        os.mkdir(f"./{working_dir_name}")
    insn_start = time.perf_counter()
    print(f"Processing {insn}")
    
    # prepare insn.c file with execute_function from ptxc
    oracle_program_path = f"{path_to_ptx_semantics}/c/{insn}.c"
    function_name = f"execute_{insn}"
    insn_file_copy_path = f"{insn}_copy.c"
    insn_file = open(insn_file_copy_path, "w+")
    copy(oracle_program_path, insn_file_copy_path)
    insn_pm = ProgramManipulator(f"{insn}_copy.c", path_to_fakeheaders)
    execute_insn_func = ptxc_pm.get_function(function_name)
    updated_insn_program = insn_pm.add_function_to_program(execute_insn_func, add_header="ptxc_utils.h")

    insn_file.truncate(0)
    insn_file.write(updated_insn_program)
    insn_file.close()
    # insn file is now ready for mutation.
    solver = ""  #default
    run_data = L1_runner(insn_file_copy_path, function_name, f"{path_to_ptx_semantics}/{test_suite_path}", mutation_directory_name, "-lm", solver, f"new_inputs_{insn}", 
    path_to_MUSIC, path_to_fakeheaders, working_dir_name=working_dir_name,  file_dependencies=file_dependencies, pre_compile_flags=pre_compile_flags,)
    result_dict[insn] = run_data
    try:
        os.system(f"rm -rf {working_dir_name}")
        os.system(f"rm -rf {mutation_directory_name}")
        os.system(f"rm {insn_file_copy_path}")
    except Exception as e:
        print("failed cleanup")
        pass


class Worker(threading.Thread):
    def __init__(self, q, *args, **kwargs):
        self.q = q
        super().__init__(*args, **kwargs)
    def run(self):
        while True:
            try:
                work = self.q.get(timeout=3)  # 3s timeout
            except queue.Empty:
                return
            run_single_insn(*work)
            self.q.task_done()


def runner(path_to_MUSIC, path_to_fakeheaders, use_yaml=True):

   # idea; start by only looking at tests of f32 type:
   # command to get all of them: find . -maxdepth 1 -name "*f32*.c" -print 
   # in ROCetta/ptx-semantics-tests/v6.5/c 
   # 1630 functions
   # tests.yaml has compile commands

    print("Starting runner")
    total_start = time.perf_counter()
    result_dict = {}
    #insn_list = ["add_rm_ftz_sat_f32", "add_sat_f32", "abs_f32"] # is a list of oracle compiled binaries. 
    #path_to_fakeheaders = "pycparser/utils/fake_libc_include"
    path_to_ptx_semantics = "../ROCetta/ptx-semantics-tests/v6.5"
    #path_to_MUSIC = "./MUSIC/music"
    path_to_ptxc = f"{path_to_ptx_semantics}/c/ptxc.c"
    command_change_dir_to_ptx = f"cd {path_to_ptx_semantics}/c"
    all_insns = subprocess.check_output(f" find {path_to_ptx_semantics}/c -type f -print0 | xargs -0 basename -a", shell=True)
    all_insns_arr = str(all_insns).split('\\n')
    # for f32
    insn_list = [insn for insn in all_insns_arr if insn.endswith("f32")]
    insn_list = insn_list[:100]
    print(insn_list)
    ptxc_pm = ProgramManipulator(path_to_ptxc, path_to_fakeheaders)
    original_ptxc_contents = open(path_to_ptxc, "r").readlines()

    if use_yaml:
        insn_info = process_instructions_yaml(f"{path_to_ptx_semantics}/instructions.yaml")
    else:
        test_info_command = f"python3 ../ROCetta/ptx-semantics-tests/gpusemtest/run_test.py v6.5 c exec"
        

    # set file depencies for instructions.
    file_dependencies = ["128types.h", "lop3_lut.h" , "ptxc.h", "ptxc_utils.h", "ptxc_utils_template.h", "readbyte_prmt.h", "testutils.h", "testutils.c"]
    file_dependencies = [f"{path_to_ptx_semantics}/c/{f}" for f in file_dependencies]

    # set precompile flags;
    pre_compile_flags = "-g -O3 -L. testutils.c"

    ## parallel method
    # num_threads = mp.cpu_count()
    # q = queue.Queue()
    # for insn in insn_list:
    #      # test suite associated with 
    #     if use_yaml:
    #         test_suite_path = get_input_path(insn_info, insn)
    #     else:
    #         insn_info_command = test_info_command + f" {insn}"
    #         output = subprocess.check_output(test_info_command, shell=True)
    #         test_suite_path = output.split()[0].split(' ')[1]                
    #         # run and parse gpusemtest/run_test.py
    #     q.put_nowait((insn, ptxc_pm, path_to_ptx_semantics, path_to_MUSIC, path_to_fakeheaders, file_dependencies, pre_compile_flags, test_suite_path, result_dict))
    # for _ in range(num_threads):
    #     Worker(q).start()
    # q.join()

    ## serial method
    for insn in insn_list:
        # test suite associated with 
        if use_yaml:
            test_suite_path = get_input_path(insn_info, insn)
        else:
            insn_info_command = test_info_command + f" {insn}"
            output = subprocess.check_output(test_info_command, shell=True)
            test_suite_path = output.split()[0].split(' ')[1]                
            # run and parse gpusemtest/run_test.py
        try:
            run_single_insn(insn, ptxc_pm, path_to_ptx_semantics, path_to_MUSIC, path_to_fakeheaders, file_dependencies, pre_compile_flags, test_suite_path, result_dict)
        except Exception as e:
            result_dict[insn] = {"Insn Failed due to exception" : e}
    write_run_data(result_dict, "Run_Results")
    total_end = time.perf_counter()
    print(f"Total run took {total_end-total_start}")



# MUSIC path
MUSIC = sys.argv[1] 

# fake headers path
fake_headers = sys.argv[2]

# how to get input files
use_yaml = sys.argv[3]
flag = False
if use_yaml == "yaml":
    flag = True
runner(MUSIC, fake_headers, use_yaml=flag)
