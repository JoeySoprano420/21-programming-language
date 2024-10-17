#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>

class ASTNode {
public:
    virtual llvm::Value* codegen() = 0; // Generate LLVM IR
};

class NumberNode : public ASTNode {
    int value;
public:
    NumberNode(int val) : value(val) {}
    llvm::Value* codegen() override {
        return llvm::ConstantInt::get(llvm::Type::getInt32Ty(llvm::getGlobalContext()), value);
    }
};

// Other AST node classes...
