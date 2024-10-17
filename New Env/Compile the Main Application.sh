g++ -o 21 main.cpp lexer/generated/*.cpp parser/*.c ast/*.cpp graphics/*.cpp `llvm-config --cxxflags --ldflags --libs`
