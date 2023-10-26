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



using namespace std;


typedef vector<string> Vstring;
typedef vector<int> Vint;


bool load_input(const char *filename, Vstring& lines) {
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

Vstring explode(std::string str, char delimiter)
{
    Vstring output;
    std::stringstream ss{str};
    std::string token;

    while (getline(ss, token, delimiter)) {
        if (token.size() > 0)
            output.push_back(token);
    }

    return output;
}


typedef pair<string, string> Plink;

void parse_line(const string& txt, string& p1, string& p2, int& happyness) {
    auto tokens = explode(txt, ' ');

    p1 = tokens[0];
    p2 = tokens[10];
    p2.pop_back();
    happyness = stoi(tokens[3]);
    if(tokens[2] == "lose") happyness *= -1;
}


void part1(map<Plink, int>& constraints, set<string>& players) {
    Vstring table(players.begin(), players.end());

    sort(table.begin(), table.end());

    Vint happy;

    do {
        int d{};
        // copy(table.begin(), table.end(), ostream_iterator<string>(cout, " "));
        for(size_t i{}; i < table.size() - 1; ++i) {
            d += constraints[make_pair(table[i], table[i+1])];
            d += constraints[make_pair(table[i+1], table[i])];
        }
        d += constraints[make_pair(table[0], table.back())];
        d += constraints[make_pair(table.back(), table[0])];

        // cout << " : " << d << endl;

        happy.push_back(d);
    } while(std::next_permutation(table.begin(), table.end()));

    auto [vmin, vmax] = minmax_element(happy.begin(), happy.end());
    cout << "part1 " << *vmax << endl;
}

void part2(map<Plink, int>& constraints, set<string>& players) {
    Vstring table(players.begin(), players.end());

    sort(table.begin(), table.end());

    Vint happy;

    do {
        int d{};
        // copy(table.begin(), table.end(), ostream_iterator<string>(cout, " "));
        for(size_t i{}; i < table.size() - 1; ++i) {
            d += constraints[make_pair(table[i], table[i+1])];
            d += constraints[make_pair(table[i+1], table[i])];
        }

        // cout << " : " << d << endl;

        happy.push_back(d);
    } while(std::next_permutation(table.begin(), table.end()));

    auto [vmin, vmax] = minmax_element(happy.begin(), happy.end());
    cout << "part2 " << *vmax << endl;
}


int main() {
    Vstring lines;
    load_input("input", lines);

    string p1, p2;
    int val;

    set<string> players;

    map<Plink, int> constraints;

    for(auto& line: lines) {
        parse_line(line, p1, p2, val);
        constraints[{p1, p2}] = val;

        players.insert(p1);
        players.insert(p2);
    }

    part1(constraints, players);
    part2(constraints, players);

    return EXIT_SUCCESS;
}