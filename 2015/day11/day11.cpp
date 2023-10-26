#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <iostream>
#include <utility>
#include <iterator>
#include <algorithm>
#include <map>
#include <set>
#include <list>

using namespace std;


typedef vector<char> SS;

void next_pass(SS& txt) {
    char inc{1};

    for(auto it = txt.begin(); it != txt.end() && inc != 0; ++it) {
        (*it) += inc;
        if(*it > 'z') {
            *it = 'a';
        }
        else
            inc = 0;
    }
    if(inc > 0) txt.push_back('a');
}


bool check(const SS& txt) {
    for(auto v: txt) {
        if(v == 'i' || v == 'l' || v == 'o') 
            return false;
    }

    size_t count_pair{};
    for(size_t i{}; i < txt.size() - 1; ++i) {
        if(txt[i] == txt[i+1]) {
            count_pair++;
            ++i;
        }
    }
    if(count_pair < 2)
        return false;

    for(size_t i{}; i+2 < txt.size(); ++i) {
        if(txt[i] == txt[i+1]+1 && txt[i] == txt[i+2]+2)
            return true;
    }

    return false;
}

string next_valid(const string& txt) {
    SS v{txt.rbegin(), txt.rend()};

    do {
        next_pass(v);
    } while(!check(v));

    return string(v.rbegin(), v.rend());
}


int main() {

    {
        vector<string> tests {"a", "zz", "yz", "xx", "xy", "xz", "ya"};
        for(auto txt: tests) {
            SS v{txt.rbegin(), txt.rend()};
            next_pass(v);
            cout << txt << " : ";
            copy(v.rbegin(), v.rend(), ostream_iterator<char>(cout, ""));
            cout << endl;
        }
    }

    {
        vector<string> tests {"hijklmmn", "abbceffg", "abbcegjk"};
        for(auto txt: tests) {
            SS v{txt.rbegin(), txt.rend()};
            cout << txt << " : " << check(v) << endl;
        }
    }

    {
        vector<string> tests {"abcdefgh", "ghijklmn"};
        for(auto txt: tests) {
            cout << txt << " : " << next_valid(txt) << endl;
        }
    }


    cout << "part1 : " << next_valid("cqjxjnds") << endl;
    cout << "part2 : " << next_valid(next_valid("cqjxjnds")) << endl;

    return EXIT_SUCCESS;
}