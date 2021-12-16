import sys
import subprocess
import os
import argparse
import json

# custom imports
from mutator import Mutator
from equivalence_checker_cbmc import EquivalenceChecker
from program_manipulation import ProgramManipulator 



def L1_runner(oracle_program, func_name, test_suite, mutation_directory, compilation_info, solver, new_input_filename, music_exec, fakeheader_path, working_dir_name="working_directory/",  file_dependencies=[], pre_compile_flags=None,binary_folder=None, oracle_binary=None):
    run_data = {}
    M = Mutator(oracle_program, func_name, mutation_directory, compilation_info=compilation_info, compilation_pre_flags=pre_compile_flags, MUSIC_executable=music_exec, working_dir_name=working_dir_name, file_dependencies=file_dependencies)
    if binary_folder is None:
        M.generate_mutations()
    if test_suite is not None:
        time_ran, total_mutations, mutations_killed = M.kill_mutations(test_suite, oracle_binary, binary_folder)
        mutator_pass1_data = {
                "wall_time" : time_ran,
                "total_mutations" : total_mutations,
                "mutations_killed" : mutations_killed,
                "existing_test_suite_name" : test_suite
        }
        run_data["mutator_pass_on_existing"] = mutator_pass1_data
    else:
        print(f"Creating a test suite for all generated mutations")
    # For PTX Suite, every run is on all gen mutations.
    
    M.generate_mutations()
    EQC = EquivalenceChecker(oracle_program, func_name, mutation_directory, test_suite, new_input_filename=new_input_filename, backend=solver, path_to_fakeheaders=fakeheader_path)
    time_ran, tests_pre_dd, tests_pos_dd = EQC.runner()
    eqc_data = {
        "wall_time" : time_ran,
        "num_tests_gen_pre_dd" : tests_pre_dd,
        "num_tests_gen_post_dd" : tests_pos_dd,
        "suite_filename" : new_input_filename
    }
    run_data["equivalence_checker"] = eqc_data
    print("Now will test newly generated inputs for mutation kill score.")
    if binary_folder is None:
        M.generate_mutations()
    time_ran, total_mutations, mutations_killed = M.kill_mutations(new_input_filename, binary_folder)
    mutator_pass2_data = {
                "wall_time" : time_ran,
                "total_mutations" : total_mutations,
                "mutations_killed" : mutations_killed,
                "new_test_suite_name" : new_input_filename
    }
    run_data["mutator_pass_on_new"] = mutator_pass2_data
    write_run_data(run_data, oracle_program)
    return run_data

    
def write_run_data(run_data, oracle_program):
    json_data = json.dumps(run_data)
    f = open(f"output_{ProgramManipulator.extract_last_file_from_prog_path(oracle_program)}.json", "w+")
    f.write(json_data)
    f.close()
    print(f"Wrote Output Data file at: output_{ProgramManipulator.extract_last_file_from_prog_path(oracle_program)}.json")



def only_generate_mutations(oracle_program, function_name, mutation_directory_name, compilation_info, music_exec):
    M = Mutator(oracle_program, function_name, mutation_directory_name, compilation_info=compilation_info, MUSIC_executable=music_exec)
    M.generate_mutations()

def only_kill_mutations(oracle_program, function_name, test_suite, mutation_directory_name, compilation_info, music_exec, binary_folder=None):
    run_data = {}
    M = Mutator(oracle_program, func_name, mutation_directory, compilation_info=compilation_info, MUSIC_executable=music_exec)
    time_ran, total_mutations, mutations_killed = M.kill_mutations(test_suite, binary_folder)
    mutator_pass1_data = {
                "wall_time" : time_ran,
                "total_mutations" : total_mutations,
                "mutations_killed" : mutations_killed,
                "existing_test_suite_name" : test_suite
    }
    run_data["mutator_pass_on_existing"] = mutator_pass1_data
    write_run_data(run_data, oracle_program)

def set_up_argparse():
    # set up arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("oracle_program", help="The path to the oracle program.")
    parser.add_argument("function_name", help="The name of the function to mutate within the oracle program.")
    parser.add_argument("--test_suite", "-ts", help="The path to the existing test suite of the program. If none given, will generate completely new tests")
    parser.add_argument("--mutation-directory" , "-m", help="The name of the mutation directory to be created.")
    parser.add_argument("--compilation-info", "-c", help="Optional compilation flags/files to add to standard gcc compilation.")
    parser.add_argument("--solver", "-s", help="Choose from Z3, CVC4, or MiniSat(Default) as SAT checkers for equivalence checking.")
    parser.add_argument("--new-input-filename", help="Choose a filename for the newly generated input file. Optional.")
    parser.add_argument("--path-to-MUSIC", help="Specifiy path to MUSIC executable.")
    parser.add_argument("--path-to-fakeheaders", help="Specify a path to fake standard header files.")
    parser.add_argument("--path-to-mutated-binaries", help="Specify a path to executables of all the mutation files")
    
    # args to only run one action
    parser.add_argument("--only-gen-mutations", help="Will only generate mutations")
    parser.add_argument("--only-kill-mutations", help="Will only kill mutations given rest of the params")

    # extract args
    args = parser.parse_args()
    oracle_program = args.oracle_program
    func_name = args.function_name
    test_suite = args.test_suite
    mutation_directory = args.mutation_directory if args.mutation_directory else "mutated-programs"
    compilation_info = args.compilation_info if args.compilation_info else ""
    solver = ""
    if args.solver:
        if args.solver.lowercase() == "z3":
            solver = "--z3"
        elif args.solver.lowercase() == "cvc4":
            solver = "--cvc4"
    new_input_filename = args.new_input_filename if args.new_input_filename else None

    MUSIC_path = args.path_to_MUSIC if args.path_to_MUSIC else "./MUSIC/music"
    fakeheader_path = args.path_to_fakeheaders if args.path_to_fakeheaders else "pycparser/utils/fake_libc_include"
    path_to_mutated_binaries = args.path_to_mutated_binaries if args.path_to_mutated_binaries else None
    L1_runner(oracle_program, func_name, test_suite, mutation_directory, compilation_info, solver, new_input_filename, MUSIC_path, fakeheader_path, binary_folder=args.path_to_mutated_binaries)
if __name__ == "__main__":
    set_up_argparse()
    # example command
    # python3 L1/runner.py test-dedup/add_rm_ftz_sat_f32.c execute_add_rm_ftz_sat_f32 test-dedup/data/f32_2.ssv --compilation-info="testutils.c -lm" --new-input-filename="new_inputs.txt"
    # python3 L1/runner.py abs_f32.c execute_abs_f32 f32_1.ssv --compilation-info="testutils.c -lm" --new-input-filename="new_inputs.txt" > output.txt
    # python3 L1/runner.py add_sat_f32.c execute_add_sat_f32 test-dedup/data/f32_2.ssv --compilation-info="testutils.c -lm" --new-input-filename="new_inputs.txt" > output.txt
    # python3 L1/runner.py fma_rn_ftz_f32.c execute_fma_rn_ftz_f32 f32_3.ssv --compilation-info="testutils.c -lm" --new-input-filename="new_inputs.txt"
    # insn = "add_rm_ftz_sat_f32"
    # path_to_ptx_semantics = "../ROCetta/ptx-semantics-tests/v6.5"
    # path_to_MUSIC = "./MUSIC/music"
    # function_name = f"execute_{insn}"
    # oracle_program_path = f"{path_to_ptx_semantics}/c/{insn}.c"
    # test_suite_path = "test-dedup/data/f32_2.ssv"
    # mutation_directory_name = "mutated-programs"
    # mutated_binary_folder = f"mutated-binaries-{insn}"
    # path_to_fakeheaders = "pycparser/utils/fake_libc_include"
    # oracle_binary = f"{path_to_ptx_semantics}/c/{insn}"
    # run_data = L1_runner(oracle_program_path, function_name, test_suite_path, mutation_directory_name, [], "", f"new_inputs_{insn}", 
    #                     path_to_MUSIC, path_to_fakeheaders, binary_folder=f"{path_to_ptx_semantics}/c/{mutated_binary_folder}", oracle_binary=oracle_binary)
    # print(run_data)