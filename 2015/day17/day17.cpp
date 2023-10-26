#include "libwam.h"

#include <iostream>

using namespace wam;
using namespace std;


void part1(int total, const vector<int>& numbers) {
    int count = 0;
    vector<int> choice;
    for(size_t i{2}; i < numbers.size(); ++i) {
        Combination comb(numbers.size(), i);
        choice.resize(i);

        do {
            const auto& v = comb.get();
            for(size_t j{}; j < v.size(); ++j)
                choice[j] = numbers[v[j]];

            auto s = sum(choice);
            if(s == total) {
                count++;
                // copy(begin(choice), end(choice), ostream_iterator<int>(cout, " "));
                // cout << endl;
            }
        } while(comb.next());

    }
    cout << "part1 " << count << endl;

}


void part2(int total, const vector<int>& numbers) {

    vector<int> choice;
    for(size_t i{2}; i < numbers.size(); ++i) {
        int count = 0;
        Combination comb(numbers.size(), i);
        choice.resize(i);

        do {
            const auto& v = comb.get();
            for(size_t j{}; j < v.size(); ++j)
                choice[j] = numbers[v[j]];

            auto s = sum(choice);
            if(s == total) {
                count++;
                // copy(begin(choice), end(choice), ostream_iterator<int>(cout, " "));
                // cout << endl;
            }
        } while(comb.next());

        if(count > 0) {
            cout << "part2 " << i << " " << count << endl;
            break;
        }

    }

}



int main() {

    Vstring lines;
    read_lines("input", lines);

    Vint nums;

    for(auto line: lines) {
        nums.push_back(stoi(line));
    }

    sort(rbegin(nums), rend(nums));

    cout << "numbers : ";
    copy(begin(nums), end(nums), ostream_iterator<int>(cout, " "));
    cout << endl;

    part1(25, {20, 15, 10, 5, 5});

    part1(150, nums);
    part2(150, nums);

    return EXIT_SUCCESS;
}