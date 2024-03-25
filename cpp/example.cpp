#include <iostream>
#include "pyson.hpp"

int main() {
    // Make sure to run in same directory a example.pyson!
    // ...definitely haven't made that mistake before.
    std::map<std::string, pysonObject> examplePyson = getMap("./example.pyson");

    for (auto a : examplePyson){
        std::cout << a.first << ": ";
        if (a.second.type == STR){
            std::cout << a.second.stringValue << std::endl;
        } else if (a.second.type == INT) {
            std::cout << a.second.integerValue << std::endl;
        } else if (a.second.type == FLOAT) {
            std::cout << a.second.floatValue << std::endl;
        } else if (a.second.type == LIST) {
            std::cout << "{";
            for (auto entry : a.second.listValue) {
                std::cout << "\""<< entry << "\" ";
            }
            std::cout << "}" << std::endl;
        }
    }

    return 0;
}
