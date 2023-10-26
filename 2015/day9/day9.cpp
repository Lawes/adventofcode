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


typedef vector<string> Tokens;


bool load_input(const char *filename, Tokens& lines) {
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


struct Parcour {
    string a, b;
    size_t distance;
};


Tokens explode(std::string str, char delimiter)
{
    Tokens output;
    std::stringstream ss{str};
    std::string token;

    while (getline(ss, token, delimiter)) {
        if (token.size() > 0)
            output.push_back(token);
    }

    return output;
}


Parcour parse_line(const string& line) {
    auto tokens = explode(line, ' ');

    return {tokens[0], tokens[2], stoull(tokens[4])};
}


int main() {
    Tokens lines;

    load_input("input", lines);


    set<string> cities;
    vector<string> lcities;
    map<pair<string, string>, size_t> distances;

    for(auto& line: lines) {
        auto p = parse_line(line);
        cities.insert(p.a);
        cities.insert(p.b);

        distances[make_pair(p.a, p.b)] = p.distance;
        distances[make_pair(p.b, p.a)] = p.distance;
    
        cout << p.a << " - " << p.b << " : " << p.distance << endl;
    }

    lcities.resize(cities.size());
    copy(cities.begin(), cities.end(), lcities.begin());
    sort(lcities.begin(), lcities.end());

    vector<size_t> alldist;

    do {
        size_t d{};
        for(size_t i{}; i < lcities.size() - 1; ++i) {
            d += distances[make_pair(lcities[i], lcities[i+1])];
        }
        alldist.push_back(d);
        // copy(lcities.begin(), lcities.end(), ostream_iterator<string>(cout, " "));
        // cout << d << endl;
    } while(std::next_permutation(lcities.begin(), lcities.end()));


    auto [vmin, vmax] = minmax_element(alldist.begin(), alldist.end());

    cout << "part1 " << *vmin << endl;
    cout << "part2 " << *vmax << endl;


    return EXIT_SUCCESS;
}