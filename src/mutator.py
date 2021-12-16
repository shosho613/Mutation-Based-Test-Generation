# This is the component that will run the desired mutator tool on a C program to generate mutated programs.
# Currently this component supports the MUSIC mutation tool.
from program_manipulation import ProgramManipulator 
import subprocess
import os
import time
import copy
from os.path import isfile, join
import multiprocessing as mp

# TODO: try killing mutants with new test set

class Mutator(object):

    def __init__(self, program_name, function_name, mutated_program_dir_name, compilation_info=None, compilation_pre_flags=None ,MUSIC_executable="./MUSIC/music", working_dir_name="working_directory/", file_dependencies=[]):
        """
        Args:
        program_name = Name of program to mutate
        function_name = Name of function to mutate
        """
        self.program_name = program_name
        self.function_name = function_name
        self.MUSIC_executable = MUSIC_executable
        self.function_lines = ProgramManipulator.get_function_lines(program_name, function_name)
        self.mutated_program_dir_name = mutated_program_dir_name
        self.compilation_info = compilation_info
        self.compilation_pre_flags = compilation_pre_flags
        self.working_dir_name = working_dir_name
        self.file_dependencies = file_dependencies
    
    def generate_mutations(self):
        filename = ProgramManipulator.extract_last_file_from_prog_path(self.program_name)
        # create the directory for mutations (MUSIC requirement)
        if not os.path.isdir(f"./{self.mutated_program_dir_name}"):
	        os.mkdir(f"./{self.mutated_program_dir_name}")
        else:
	        os.system(f"rm -rf {self.mutated_program_dir_name}")
	        os.mkdir(f"./{self.mutated_program_dir_name}")
        subprocess.call(f"{self.MUSIC_executable} {self.program_name} -o {self.mutated_program_dir_name} -rs {filename}:{self.function_lines[0]} -re {filename}:{self.function_lines[1]} --", shell=True)
        print(f"Mutated Programs generated at {self.mutated_program_dir_name} successfully")
        

    @staticmethod
    def outputs_equal(o1, o2):
        if len(o1) != len(o2):
            print("Outputs are not the same length. They are not equal.")
            return False
        for i in range(len(o1)):
            v1 = float.fromhex(o1[i])
            v2 = float.fromhex(o2[i])
            if v1 != v2:
                print(f"Outputs at row {i+1} are not the same.\n{v1} vs {v2}.")
                return False
        return True

    def compile_test_and_compare_mutation(self, mutation, working_dir, oracle_outputs, test_suite):
        mutation_executable = f"{ProgramManipulator.extract_last_file_from_prog_path(mutation)}.exe"
        mutation_output_file = f"{ProgramManipulator.extract_last_file_from_prog_path(mutation)}.txt"

        subprocess.call(f"cp {self.mutated_program_dir_name}/{mutation} {working_dir}", shell=True, timeout=5)

        subprocess.call(f"gcc {self.compilation_pre_flags} {mutation} {self.compilation_info} -o {mutation_executable}", shell=True, cwd=working_dir, timeout=5)
        # run on test suite
        result = subprocess.call(f"./{mutation_executable} ../{test_suite} {mutation_output_file}", shell=True, cwd=working_dir, timeout=5)
        

        if result == 137:  # 137 is SIGKILL code.
            print(f"Unuseful mutation {mutation}. (Thread killed). Deleting.")
            subprocess.call(f"rm {self.mutated_program_dir_name}/{mutation}", shell=True, timeout=5)
        else:
            try:
                mutation_outputs = open(f"{working_dir}{mutation_output_file}", "r").readlines()
                # compare output to oracle output
                # if same, kill
                # else, keep
                if not Mutator.outputs_equal(oracle_outputs,mutation_outputs):
                    subprocess.call(f"rm {self.mutated_program_dir_name}/{mutation}", shell=True, timeout=5)
                    print(f"Test suite covers {mutation}. Deleting file.")
                else:
                    print(f"{mutation} has not been killed. No differentiating test case found.")
            except Exception as e:
                print(e)
                print(f"Unuseful mutation {mutation}. Killing. In exception")
                subprocess.call(f"rm {self.mutated_program_dir_name}/{mutation}", shell=True, timeout=5)
        # clean up
        subprocess.call(f"rm {mutation_output_file} {mutation} {mutation_executable}", shell=True, cwd=working_dir, timeout=5)
        # return mutation, open(test_suite, "r").readlines(), mutation_outputs

    def test_and_compare_mutation(self, test_suite, oracle_outputs, mutation_executable, survived_mutations, working_dir):
        mutation_output_file = f"{ProgramManipulator.extract_last_file_from_prog_path(mutation_executable)}.txt"
        mutation_output = Mutator.get_program_output(mutation_executable, test_suite, mutation_output_file, working_dir)
        if mutation_output is None:
            print(f"Unuseful mutation {mutation_executable}. Deleting.")
            survived_mutations.remove(mutation_executable)
        else:
            if not Mutator.outputs_equal(oracle_outputs, mutation_output):
                survived_mutations.remove(mutation_executable)
                print(f"Test suite covers {mutation_executable}. Deleting.")
            else:
                print(f"{mutation_executable} has not been killed. No differentiating test case found.")

 
    @staticmethod
    def get_program_output(program_executable, test_suite, output_filename, working_dir):
        try:
            executable_name = ProgramManipulator.extract_last_file_from_prog_path(program_executable)
            subprocess.call(f"cp {program_executable} {working_dir}", shell=True, timeout=5)

            result = subprocess.call(f"./{executable_name} ../{test_suite} {output_filename}", shell=True, cwd=working_dir, timeout=5)
            if result == 137: # 137 is SIGKILL code.
                return None
            program_outputs = open(f"{working_dir}{output_filename}", "r").readlines()
            os.remove(f"{working_dir}{output_filename}")
            os.remove(f"{working_dir}{executable_name}")
            return program_outputs
        except Exception as e:
            print(f"In get program output: {e}")
            return None

    def kill_mutations_with_binary(self, test_suite, oracle_binary, mutated_binary_folder):
        mutated_binaries = [join(mutated_binary_folder,f) for f in os.listdir(mutated_binary_folder) if isfile(join(mutated_binary_folder, f))]
        print(f"Total mutated binaries before copy: {len(mutated_binaries)}")
        start = time.perf_counter()
        survived_mutations = copy.deepcopy(mutated_binaries)
        total_mutations = len(mutated_binaries)
        print(f"Total mutated binaries: {total_mutations}")

        oracle_output_file = "oracle_output.txt"
        working_directory = self.working_dir_name
        for command in self.compilation_info:
            subprocess.call(command, shell=True, timeout=5)
        oracle_outputs = Mutator.get_program_output(oracle_binary, test_suite, oracle_output_file, working_directory)
        print("Generated oracle outputs.")
        #pool = mp.Pool(mp.cpu_count())
        for mutation in mutated_binaries:
            self.test_and_compare_mutation(test_suite, oracle_outputs, mutation, survived_mutations, working_directory)
            
        #pool.close()
        #pool.join()
        stop = time.perf_counter()


        print(f"Total Killed Mutations: {total_mutations-len(survived_mutations)} out of {total_mutations} total mutations")
        print(f"Kill ratio {(total_mutations-len(survived_mutations))/total_mutations}")
        print(f"Run Statistics:\nTime Taken: {stop-start} seconds")
        return start-stop, total_mutations, len(survived_mutations)


    def kill_mutations(self, test_suite, oracle_binary=None, binary_folder=None):
        if binary_folder is None or oracle_binary is None:
            return self.kill_mutations_with_compile(test_suite)
        else:
            return self.kill_mutations_with_binary(test_suite, oracle_binary, binary_folder)

    
    def kill_mutations_with_compile(self, test_suite):
        working_dir = self.working_dir_name
        oracle_executable = "oracle_exec"
        oracle_output_file = "oracle_output.txt"

        # add file dependencies to working_dir
        for file in self.file_dependencies:
            subprocess.call(f"cp {file} {working_dir}", shell=True, timeout=5)
        # compile oracle
        subprocess.call(f"cp {self.program_name} {working_dir}", shell=True, timeout=5)
        print(f"gcc {self.compilation_pre_flags} {ProgramManipulator.extract_last_file_from_prog_path(self.program_name)} {self.compilation_info} -o {oracle_executable}")
        subprocess.call(f"gcc {self.compilation_pre_flags} {ProgramManipulator.extract_last_file_from_prog_path(self.program_name)} {self.compilation_info} -o {oracle_executable}", shell=True, cwd=working_dir, timeout=5)
        # run oracle on test suite
        time.sleep(2)
        subprocess.call(f"./{oracle_executable} ../{test_suite} {oracle_output_file}", shell=True, cwd=working_dir, timeout=5)
        # get oracle output
        oracle_outputs = open(f"{working_dir}{oracle_output_file}", "r").readlines()
        # for each mutation 
        mutated_programs = [f for f in os.listdir(self.mutated_program_dir_name) if isfile(join(self.mutated_program_dir_name, f))]
        mutated_programs = [m for m in mutated_programs if m.endswith(".c")]
        total_mutations = len(mutated_programs)
        print(f"Total mutations: {total_mutations}")
        
        start = time.perf_counter()
        pool = mp.Pool(mp.cpu_count())
        for mutation in mutated_programs:
            pool.apply_async(self.compile_test_and_compare_mutation, (mutation, working_dir, oracle_outputs, test_suite))
        pool.close()
        pool.join()
        # for mutation in mutated_programs:
        #     self.test_and_compare_mutation(mutation, working_dir, oracle_outputs, test_suite)
        stop = time.perf_counter()
        subprocess.call(f"rm {oracle_executable} {oracle_output_file}", shell=True, cwd=working_dir, timeout=5)

        survived_mutations = [f for f in os.listdir(self.mutated_program_dir_name) if isfile(join(self.mutated_program_dir_name, f))]
        survived_mutations = len([m for m in survived_mutations if m.endswith(".c")])
        print(f"Total Killed Mutations: {total_mutations-survived_mutations} out of {total_mutations} total mutations")
        print(f"Kill ratio {(total_mutations-survived_mutations)/total_mutations}")
        print(f"Run Statistics:\nTime Taken: {stop-start} seconds")
        
        return stop-start, total_mutations, total_mutations - survived_mutations

    @staticmethod
    def write_survived_outputs(surv, filename):
        f = open(filename, "w+")
        for s in surv:
            f.write(s[0])
            f.write("\n")
            f.write(s[1])
        f.close()
    

if __name__ == "__main__":
    oracle_program_path = "test-dedup/add_rm_ftz_sat_f32.c"
    function_name = "execute_add_rm_ftz_sat_f32"
    mutated_directory = "mutated-programs"
    compilation_info = "testutils.c -lm"
    M = Mutator(oracle_program_path, function_name, mutated_directory, compilation_info=compilation_info)
    #print(M.function_lines)
    M.generate_mutations()
    M.kill_mutations("test-dedup/data/f32_2.ssv")