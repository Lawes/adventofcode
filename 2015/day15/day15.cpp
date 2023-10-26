#include "libwam.h"


using namespace wam;
using namespace std;


struct Info {
    string name;
    vector<int> params;
    // int capacity, durability, flavor, texture, calories;
};

Info parse_line(const string& txt) {
    auto tokens = explode(txt, ' ');

    string name = tokens[0];
    name.pop_back();

    return {
        name, {
            stoi(tokens[2]), stoi(tokens[4]),
            stoi(tokens[6]), stoi(tokens[8]),
            stoi(tokens[10])
        }
    };
}


int make_calorie(const vector<Info>& ingredients, const vector<int>& spoon) {
    int count = 0;
    for(size_t i{}; i < ingredients.size(); ++i)
        count += ingredients[i].params[4] * spoon[i];
    return count;
}

int make_cookie(const vector<Info>& ingredients, const vector<int>& spoon) {
    int total{1};
    
    for(size_t iparam{}; iparam < 4; ++iparam) {
        int count = 0;
        for(size_t i{}; i < ingredients.size(); ++i)
            count += ingredients[i].params[iparam] * spoon[i];

        if(count <= 0)
            return 0;

        total *= count;
    }
    return total;
}

int main() {
    Vstring lines;
    read_lines("input", lines);

    vector<Info> ingredients;

    for(const auto& line: lines) {
        ingredients.push_back(parse_line(line));
        auto& e = ingredients.back();

        cout << e.name << " : ";
        copy(begin(e.params), end(e.params), ostream_iterator<int>(cout, " "));
        cout << endl;
    }

    {
        int current_max = 0;
        vector<int> allcount;

        for(int p1=0; p1 < 100; ++p1) {
            for(int p2=0; p2 < 100 - p2; ++p2) {
                for(int p3=0; p3 < 100 - p1 - p2; ++p3) {
                    int p4 = 100 - p1 - p2 - p3;
                    vector<int> combv{p1, p2, p3, p4};
                    auto total = make_cookie(ingredients, combv);
                    if(total > 0 && total > current_max) {
                        // copy(begin(combv), end(combv), ostream_iterator<int>(cout , " "));
                        //cout << " : " << total << endl;
                        current_max = total;
                        allcount.push_back(total);
                    }
                }
            }
        }

        cout << "part1 " << current_max << endl;
    }

    {
        int current_max = 0;
        vector<int> allcount;

        for(int p1=0; p1 < 100; ++p1) {
            for(int p2=0; p2 < 100 - p2; ++p2) {
                for(int p3=0; p3 < 100 - p1 - p2; ++p3) {
                    int p4 = 100 - p1 - p2 - p3;
                    vector<int> combv{p1, p2, p3, p4};
                    auto total = make_cookie(ingredients, combv);
                    if(make_calorie(ingredients, combv) != 500)
                        continue;
                    if(total > 0 && total > current_max) {
                        // copy(begin(combv), end(combv), ostream_iterator<int>(cout , " "));
                        //cout << " : " << total << endl;
                        current_max = total;
                        allcount.push_back(total);
                    }
                }
            }
        }

        cout << "part2 " << current_max << endl;
    }

    return EXIT_SUCCESS;
}