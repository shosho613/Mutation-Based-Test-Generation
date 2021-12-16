# This is a helper file to assist in program manipulation and extraction with the help of pycparser
#TODO: this is a stop gap fix because pycparser is a dependency.
import sys
sys.path.append('../')
sys.path.extend(['.', '..'])

try:
    from pycparser.pycparser import parse_file, c_generator, c_ast, c_parser
except:
    from pycparser import parse_file, c_generator, c_ast, c_parser
import os
import tempfile
import random
import string
import pathlib
from os.path import isfile, join


class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self, bodies=[]):
        self.bodies = bodies

    def visit_FuncDef(self, node):
        self.bodies.append(node)

class ProgramManipulator(object):

    def __init__(self, program, path_to_fakeheaders, other_headers=[]):
        self.program_filename  = program

        self.cpp_args = ['-E', f"-I{path_to_fakeheaders}", f"-I{pathlib.Path(program).parent}", f"-I{pathlib.Path(__file__).parent}"]
        for header in other_headers:
            self.cpp_args.append(header)
        # cpp args required.
        self.cpp_args.append( "-DPYCPARSER")
        self.cpp_args.append("-D__STDC_VERSION__=199901L")
        self.cpp_path = 'gcc'
        self.ast = self.parse_program(path_to_fakeheaders)
        v = FuncDefVisitor(bodies=[])
        v.bodies.clear()
        v.visit(self.ast)
        self.all_includes = ProgramManipulator.get_all_includes(program)
        self.function_nodes = v.bodies

    @staticmethod
    def substring_in_array(substr, array):
        for a in array:
            if a in substr:
                return True
        return False


    @staticmethod
    def remove_nonstd_includes(program, fakeheader_path):
        # extract all includes
        lines = open(program, 'r').readlines()
        include_lines = [l for l in lines if "#include" in l]
        # get all names of files ending in .h in pycparser/utils/fake_libc_includes
        std_includes = [f for f in os.listdir(fakeheader_path) if isfile(join(fakeheader_path, f))]
        # get nonstd include lines

        nonstd_includes = set([l for l in include_lines if not ProgramManipulator.substring_in_array(l, std_includes)])
        lines = [l for l in lines if l not in nonstd_includes]
        new_program = "".join(lines)
        return new_program

    @staticmethod 
    def get_all_includes(program):
        lines = open(program, 'r').readlines()
        include_lines = [l for l in lines if "#include" in l]
        return include_lines

    def parse_program(self, path_to_fakeheaders):
        try:
            ast = parse_file(self.program_filename, use_cpp=True, cpp_path=self.cpp_path, cpp_args=self.cpp_args)
            return ast
        except Exception as e:
            raise(e)
            

    @staticmethod
    def get_function_lines(program, function_name):
        """
        Method to get function lines given C file and function name.
        Essentially a curly bracket matcher.
        Assumption: Only one function in file with function_name
        Args:
        Program = string of program names
        function_name = string of function name
        Returns:
        tuple of lines (start_line, end_line)
        """
        program_lines = open(program, "r").readlines()
        function_lines = [None, None]
        unmatched_curly_brackets = 0
        for i in range(len(program_lines)):

            line = program_lines[i]
            if function_name in line and function_lines[0] == None:
                function_lines[0] = i
                unmatched_curly_brackets += 1
                print(function_lines[0])
                if not "{" in line:
                    unmatched_curly_brackets -= 1
                    
                continue

            # in function
            if function_lines[0]:
                if "}" in line:
                    unmatched_curly_brackets -= 1
                    if unmatched_curly_brackets == 0:
                        function_lines[1] = i
                        return function_lines
                if "{" in line:
                    unmatched_curly_brackets += 1

        raise Exception(f"Cannot find lines for function {function_name} in file {program}.")


    def get_function(self,function_name):
        """ Gets function body string from pycparser.
        Returns None if function name does not exist in program.
        Args:
        Program
        function_name = string of function name
        """
        generator = c_generator.CGenerator()
        for node in self.function_nodes:
            if node.decl.name == function_name:
                return generator.visit(node)
        return None

    def get_function_ast(self, function_name):
        for node in self.function_nodes:
            if node.decl.name == function_name:
                return node
        return None

    def get_function_inputs(self, function_name):
        inputs = []
        try:
            for node in self.function_nodes:
                if node.decl.name == function_name:
                    for param in node.decl.type.args.params:
                        inputs.append([param.name, param.type.type.names[0]])
        except:
            return []
        return inputs
                    
    def remove_function(self, function_name):
        self.function_nodes = [node for node in self.function_nodes if node.decl.name != function_name]
        return self
    
    def replace_function(self, new_function, function_name):
        tmp = []
        for node in self.function_nodes:
            if node.decl.name == function_name:
                tmp.append(new_function)
            else:
                tmp.append(node)
        self.function_nodes = tmp
        return self

        self.function_nodes[self.get_function_ast(function_name)]
    def get_function_return_type(self, function_name):
        t = None
        try:
            for node in self.function_nodes:
                if node.decl.name == function_name:
                    return node.decl.type.type.type.names[0]
        except:
            return t

    def get_function_name(self, func_node):
        for node in self.function_nodes:
            if node == func_node:
                return node.decl.name

        return None

    def create_string_from_program(self):
        function_bodies = [self.get_function(self.get_function_name(body)) for body in self.function_nodes]
        #print(f"Length of function bodies: {len(function_bodies)}")
        function_bodies = set(function_bodies)
        #print(f"Length of function bodies: {len(function_bodies)}")
        program = ""
        program += "".join(self.all_includes)
        program += "".join(function_bodies)
        return program

    def add_function_to_program(self, new_function, new_function_name=None, add_header=None):
        """
        Adds a function to an existing C program, optionally with a new function name.
        Returns:
        New program with added function
        """
        function_bodies = [self.get_function(self.get_function_name(body)) for body in self.function_nodes]
        program = ""
        program += "".join(self.all_includes)
        if add_header:
            program += f"#include \"{add_header}\"\n"
        program += "\n" + new_function
        program += "".join(function_bodies)
        return program


    @staticmethod
    def rename_function(function, current_name, desired_name):
        function = function.replace(current_name, desired_name)
        return function


    @staticmethod
    def extract_last_file_from_prog_path(path):
        splitted = path.split('/')
        return splitted[-1] 



    
    def instrument_for_cbmc_check(program, oracle_func_name, mutated_func_name):
        """
        Add instrumentation in main to check for equivalence of two functions using
        CBMC constructs.
        """
        pass



if __name__ == "__main__":
    sys.path.extend(['.', '..'])
    # oracle_program, function_name, survived_mutations, checker
    program_path = "../ROCetta/ptx-semantics-tests/v6.5/c/ptxc.c"
    pm = ProgramManipulator(program_path, "pycparser/utils/fake_libc_include")
    lines = ProgramManipulator.get_function_lines(program_path, "execute_add_rm_ftz_sat_f32")
    #print(lines)
    f = pm.create_string_from_program()
    print(f)
    # inputs = pm.get_function_inputs("execute_add_rm_ftz_sat_f32")
    # r_type = pm.get_function_return_type("execute_add_rm_ftz_sat_f32")
    # print(r_type)
    # ast.show()

