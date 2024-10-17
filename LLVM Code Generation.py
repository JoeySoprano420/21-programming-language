import llvmlite.ir as ir
import llvmlite.binding as llvm

class LLVMCodeGenerator:
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create the LLVM module
        self.module = ir.Module(name='Dynamic21')
        self.builder = None
        self.variables = {}

        # LLVM types
        self.int_type = ir.IntType(32)
        self.bool_type = ir.IntType(1)

    def create_function(self):
        func_type = ir.FunctionType(self.int_type, [])
        function = ir.Function(self.module, func_type, name="main")
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        return function

    def declare_variable(self, name, value):
        # Declare and store variable in LLVM
        var = self.builder.alloca(self.int_type, name=name)
        self.builder.store(ir.Constant(self.int_type, value), var)
        self.variables[name] = var

    def assign_register(self, register, value):
        if register in self.variables:
            var = self.variables[register]
            self.builder.store(ir.Constant(self.int_type, value), var)
        else:
            raise ValueError(f"Register {register} not found!")

    def add_operation(self, register, identifier):
        if register in self.variables and identifier in self.variables:
            reg_value = self.builder.load(self.variables[register], name="load_reg")
            id_value = self.builder.load(self.variables[identifier], name="load_id")
            result = self.builder.add(reg_value, id_value, name="add_result")
            self.builder.store(result, self.variables[register])
        else:
            raise ValueError(f"Variable not found!")

    def generate_code(self):
        print(str(self.module))

    def execute_code(self):
        llvm_ir = str(self.module)

        # Create a target machine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()

        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()

        with open('output.o', 'wb') as f:
            f.write(target_machine.emit_object(mod))

# Example LLVM usage
codegen = LLVMCodeGenerator()
main_func = codegen.create_function()
codegen.declare_variable('x', 10)
codegen.assign_register('eax', 5)
codegen.add_operation('eax', 'x')
codegen.generate_code()
