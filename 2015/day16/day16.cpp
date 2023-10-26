#include "libwam.h"

#include <map>
#include <iostream>

using namespace std;
using namespace wam;


typedef map<string, int> MFCSAM;


MFCSAM parse_line(const string& txt) {
    auto tokens = explode(txt, ' ');

    MFCSAM info;

    string key;
    int nsue = stoi(tokens[1]);
    for(size_t i{2}; i < tokens.size(); i+=2) {
        key = tokens[i];
        key.pop_back();

        info[key] = stoi(tokens[i+1]);
    }

    return info;
}

map<string, int> refsue {
    {"children", 3},
    {"cats", 7},
    {"samoyeds", 2},
    {"pomeranians", 3},
    {"akitas", 0},
    {"vizslas", 0},
    {"goldfish", 5},
    {"trees", 3},
    {"cars", 2},
    {"perfumes", 1}
};

bool match(const MFCSAM& e) {
    for(auto [key, val]: refsue) {
        const auto it = e.find(key);
        if(it != end(e)) {
            auto v = refsue[key];
            if(it->second != v)
                return false;
        }
    }
    return true;
}

bool match2(const MFCSAM& e) {
    for(auto [key, val]: refsue) {
        const auto it = e.find(key);
        if(it != end(e)) {
            auto v = refsue[key];
            if(key == "cats" || key == "trees") {
                if(it->second < v)
                    return false;
            }
            else if(key == "pomeranians" || key == "goldfish") {
                if(it->second > v)
                    return false;
            }
            else if(it->second != v)
                return false;
        }
    }
    return true;
}

int main() {

    Vstring lines;
    read_lines("input", lines);


    vector<MFCSAM> sues;

    for(auto line: lines) {
        sues.push_back(parse_line(line));
        auto elem = sues.back();
        for(auto& e: elem) {
            cout << e.first << " " << e.second << " - ";
        }
        cout << endl;
    }

    for(size_t i{};  i < sues.size(); ++i) {
        const auto& sue = sues[i];
        if(match(sue)) {
            cout << "part1 " << i+1 << " : ";
            for(auto& e: sue) {
                cout << e.first << " " << e.second << " - ";
            }
            cout << endl;
        }
    }

    for(size_t i{};  i < sues.size(); ++i) {
        const auto& sue = sues[i];
        if(match2(sue)) {
            cout << "part2 " << i+1 << " : ";
            for(auto& e: sue) {
                cout << e.first << " " << e.second << " - ";
            }
            cout << endl;
        }
    }

    return EXIT_SUCCESS;
}