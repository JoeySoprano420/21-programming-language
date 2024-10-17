#include <regex>

std::string input = "Example string 123";
std::regex pattern(R"(\d+)");
std::smatch matches;

if (std::regex_search(input, matches, pattern)) {
    std::cout << "Found a number: " << matches[0] << std::endl;
}
