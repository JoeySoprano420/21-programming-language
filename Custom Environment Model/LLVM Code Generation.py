import llvmlite.ir as ir
import llvmlite.binding as llvm

class LLVMCodeGenerator:
    def __init__(self):
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create the module and function builder
        self.module = ir.Module(name='Dynamic21')
        self.builder = None

        # Setup function signatures
        self.int_type = ir.IntType(32)
        self.bool_type = ir.IntType(1)

    def create_function(self):
        func_type = ir.FunctionType(self.int_type, [self.int_type])
        function = ir.Function(self.module, func_type, name="main")
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        return function

    def create_var(self, name, value):
        var = self.builder.alloca(self.int_type, name=name)
        self.builder.store(ir.Constant(self.int_type, value), var)
        return var

    def add_instruction(self, reg, val):
        loaded_reg = self.builder.load(reg, name='load_reg')
        added = self.builder.add(loaded_reg, ir.Constant(self.int_type, val))
        self.builder.store(added, reg)

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

# Usage Example
codegen = LLVMCodeGenerator()
main_func = codegen.create_function()
x = codegen.create_var('x', 10)
codegen.add_instruction(x, 5)
codegen.generate_code()
codegen.execute_code()
