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

typedef vector<short> VV;


VV next_step(const VV& v) {
    VV vv;

    for(size_t i{}; i < v.size(); ++i) {
        auto current = v[i];
        int count{1};
        size_t di{1};

        while(i+di < v.size()) {
            if(v[i+di] != current) break;
            ++di;
            ++count;
        }
        vv.push_back(count);
        vv.push_back(current);
        i += di - 1;
    }
    return vv;
}



int main() {

    VV v{1, 1, 1, 2, 1};

    auto vv = next_step(v);

    copy(vv.begin(), vv.end(), ostream_iterator<VV::value_type>(cout, " "));
    cout << endl;

    vv = {1, 3, 2, 1, 1, 3, 1, 1, 1, 2};

    for(size_t i{}; i < 40; ++i) {
        vv = next_step(vv);
        // copy(vv.begin(), vv.end(), ostream_iterator<size_t>(cout, " "));
        // cout << endl;
    }

    cout << "part1 " << vv.size() << endl;

    vv = {1, 3, 2, 1, 1, 3, 1, 1, 1, 2};

    for(size_t i{}; i < 50; ++i) {
        vv = next_step(vv);
        // copy(vv.begin(), vv.end(), ostream_iterator<size_t>(cout, " "));
        // cout << endl;
    }

    cout << "part2 " << vv.size() << endl;

    return EXIT_SUCCESS;
}