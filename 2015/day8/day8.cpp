#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <utility>

using namespace std;


typedef vector<string> Lines;


bool load_input(const char *filename, Lines& lines) {
    string line;

    lines.clear();

    ifstream flux(filename);
    if(!flux) {
        cerr << "Unable to load " << filename << endl;
        return false;
    }

    while(getline(flux, line)) {
        if(line.size() > 0)
            lines.push_back(line);
    }

    return true;
}


typedef pair<size_t, size_t> Info;


Info getLineInfo(const string& txt) {
    size_t total {}, beg{}, end{};

    if(txt[0] == '\"' && txt.back() == '\"') {
        beg = 1;
        end = txt.size() - 1;
    }

    for(size_t i{beg}; i < end; ++i) {
        total += 1;
        if(txt[i] == '\\') {
            if(txt[i+1] == 'x') i += 3;
            else ++i;
        }
    }

    return std::make_pair(txt.size(), total);
}


string encode(const string& txt) {
    string newtxt{'\"'};

    for(size_t i{}; i < txt.size(); ++i) {
        if(txt[i] == '\"')
            newtxt += "\\\"";
        else if(txt[i] == '\\')
            newtxt += "\\\\";
        else
            newtxt += txt[i];
    }
    newtxt += '\"';
    return newtxt;
}


int main() {
    Lines lines;

    load_input("input", lines);


    size_t count{}, count2{};
    string txt_enc;

    for(auto& line: lines) {
        auto info = getLineInfo(line);
        cout << line << " : " << info.first << " " << info.second << endl;
        count += info.first - info.second;

        txt_enc = encode(line);
        cout << line << " -> " << txt_enc << endl;
        count2 += txt_enc.size() - info.first;
    }


    cout << "part1 " << count << endl;
    cout << "part2 " << count2 << endl;


    return EXIT_SUCCESS;
}