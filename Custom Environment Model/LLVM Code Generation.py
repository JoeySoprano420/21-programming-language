class LLVMCodeGenerator:
    def __init__(self):
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create the module and function builder
        self.module = ir.Module(name='Dynamic21')
        self.builder = None
        self.variables = {}  # To store variable references

        # Setup function signatures
        self.int_type = ir.IntType(32)
        self.bool_type = ir.IntType(1)

    def create_function(self):
        # Define a 'main' function
        func_type = ir.FunctionType(self.int_type, [])
        function = ir.Function(self.module, func_type, name="main")
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        return function

    def create_var(self, name, value):
        var = self.builder.alloca(self.int_type, name=name)
        self.builder.store(ir.Constant(self.int_type, value), var)
        self.variables[name] = var
        return var

    def assign_var(self, register, value):
        if register in self.variables:
            var = self.variables[register]
            self.builder.store(ir.Constant(self.int_type, value), var)
        else:
            raise ValueError(f"Variable {register} not found!")

    def add_instruction(self, reg, identifier):
        if reg in self.variables and identifier in self.variables:
            reg_val = self.builder.load(self.variables[reg])
            id_val = self.builder.load(self.variables[identifier])
            added_val = self.builder.add(reg_val, id_val)
            self.builder.store(added_val, self.variables[reg])
        else:
            raise ValueError(f"Variables {reg} or {identifier} not found!")

    def generate_code(self):
        print(str(self.module))

    def execute_code(self):
        llvm_ir = str(self.module)

        # Create a target machine and compile
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()

        # Compile the code to object code
        with open('output.o', 'wb') as f:
            f.write(target_machine.emit_object(mod))

    # Traverse the AST and generate LLVM code
    def generate_from_ast(self, ast):
        function = self.create_function()

        for node in ast:
            if node[0] == 'var_decl':
                # Variable declaration
                _, var_type, var_name, var_value = node
                self.create_var(var_name, var_value)

            elif node[0] == 'assign':
                # Assignment operation
                _, reg, value = node
                self.assign_var(reg, value)

            elif node[0] == 'add':
                # Addition operation
                _, reg, identifier = node
                self.add_instruction(reg, identifier)

        # Close function by returning 0
        self.builder.ret(ir.Constant(self.int_type, 0))

