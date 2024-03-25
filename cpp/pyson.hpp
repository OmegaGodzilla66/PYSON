// Single header PYSON library for C++.
// Written by Ember Lee (hotcocoaNcode on GitHub), late at night.
// Guaranteed to have made *some* stupid mistake.

#ifndef PYSON_HPP
#define PYSON_HPP

#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

/**
 * Enum containing the four possible PYSON data types.
 */
enum pysonObjectType {
    STR,
    INT,
    LIST,
    FLOAT
};

/**
 * A class representing a possible piece of PYSON data.
 * Can either be a std::string, int, std::vector<std::string>, or float.
 * Please check object type before accessing, as only one value is guaranteed to be non-null.
 */
class pysonObject {
public:
    pysonObjectType type;
    std::string stringValue;
    int integerValue;
    std::vector<std::string> listValue;
    float floatValue;
    pysonObject(std::string string){
        type = STR;
        stringValue = string;
    }
    pysonObject(int integer){
        type = INT;
        integerValue = integer;
    }
    pysonObject(std::vector<std::string> list){
        type = LIST;
        listValue = list;
    }
    pysonObject(float flt){
        type = FLOAT;
        floatValue = flt;
    }
};

/**
 * Function used to parse PYSON data. Splits a std::string into an std::vector<std::string> by a delimiter of std::string.
 * @param in String to be split.
 * @param del Delimiter to split by.
 * @return String split by delimiter in an std::vector.
 */
std::vector<std::string> splitStr(std::string in, std::string del){
    // shamelessly stolen from gfg with minor modification
    std::vector<std::string> v;

    int start, end = -1 * del.size();
    do {
        start = end + del.size();
        end = in.find(del, start);
        v.push_back(in.substr(start, end - start));
    } while (end != -1);

    return v;
}

/**
 getMap retrieves PYSON data from a .pyson file and returns it in the format of an std::map. If it fails, an error message is put to std::cerr and the function returns an empty map.
 @param filePath Path to retrieve PYSON data from.
 @return PYSON data in the form of a string to pysonObject map.
 */
std::map<std::string, pysonObject> getMap(std::string filePath){
    std::ifstream fileStream(filePath);
    if (!fileStream.good()){
        std::cerr << "File not found!" << std::endl;
        return {};
    }
    std::stringstream buffer;
    buffer << fileStream.rdbuf();
    std::string fileContents = buffer.str();

    std::map<std::string, pysonObject> pysonMap;

    std::vector<std::string> lines = splitStr(fileContents, "\n");
    for (auto line : lines){
        std::vector<std::string> splitLine = splitStr(line, ":");

        if (splitLine.size() < 2) {
            std::cerr << "Failed parsing!" << std::endl;
            return {};
        }

        // God dammit C++. Please let me have a switch/case for once.
        if (splitLine[1] == "str") {
            pysonMap.insert({splitLine[0], {splitLine[2]}});
        } else if (splitLine[1] == "int") {
            pysonMap.insert({splitLine[0], {std::stoi(splitLine[2])}});
        } else if (splitLine[1] == "float") {
            pysonMap.insert({splitLine[0], {std::stof(splitLine[2])}});
        } else if (splitLine[1] == "list") {
            pysonMap.insert({splitLine[0], {splitStr(splitLine[2], "(*)")}});
        } else {
            std::cerr << "Failed parsing!" << std::endl;
            return {};
        }
    }

    return pysonMap;
}

#endif //PYSON_HPP