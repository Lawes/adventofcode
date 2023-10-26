#include "libwam.h"

#include <iostream>
#include <set>
#include <cmath>

using namespace std;
using namespace wam;

int min_package_count(const Vint& list_p, int cible) {
   int count{};
    for(size_t i{}; i < list_p.size(); ++i) {
        count += list_p[i];
        if(count >= cible) {
            return i+1;
        }
    }
    return -1;
}


void min_package_nbr(const Vint& list_p, int cible, vector<Vint>& res) {
    res.clear();

    int min_count = min_package_count(list_p, cible);

    for(size_t i{min_count}; i < list_p.size(); ++i) {
        Combination comb(list_p.size(), i);

        do {
            auto &v = comb.get();
            int s{};
            for(auto indice: v)
                s += list_p[indice];
            
            if(s == cible)
                res.push_back({v});
        } while(comb.next());
        if(res.size() > 0)
            break;
    }
}

Vint remaining(const Vint& list_p, const Vint& used_indices) {
    Vint res;
    set<int> used(begin(used_indices), end(used_indices));
    for(size_t i{}; i < list_p.size(); ++i) {
        if(used.find(i) == end(used))
            res.push_back(list_p[i]);
    }
    return res;
}

bool is_2split(const Vint& list_p, int cible) {
    auto min_count = min_package_count(list_p, cible);
    for(size_t i{min_count}; i < list_p.size(); ++i) {
        Combination comb(list_p.size(), i);

        do {
            auto &v = comb.get();
            int s{};
            for(auto indice: v)
                s += list_p[indice];
            
            if(s == cible) {
                return true;
            }
                
        } while(comb.next());
    }
    return false;
}


bool is_3split(const Vint& list_p, int cible) {
    auto min_count = min_package_count(list_p, cible);
    for(size_t i{min_count}; i < list_p.size(); ++i) {
        Combination comb(list_p.size(), i);

        do {
            auto &v = comb.get();
            int s{};
            for(auto indice: v)
                s += list_p[indice];
            
            if(s == cible) {
                auto list_p_remain = remaining(list_p, v);
                if(is_2split(list_p_remain, cible)) {
                    return true;
                }
            }
                
        } while(comb.next());
    }
    return false;
}

void part1(const Vint& list_packages) {
 int tota_weight = sum(list_packages),
        group_weight = tota_weight/3;

    cout << "Total weight = " << tota_weight << ", per group = " << group_weight << endl;

 
    vector<Vint> res;
    min_package_nbr(list_packages, group_weight, res);
    size_t min_qe = pow(static_cast<size_t>(*max_element(begin(list_packages), end(list_packages))), res[0].size());
    cout << min_qe <<endl;

    for(auto& one: res) {
        auto list_p_remain = remaining(list_packages, one);
        auto isOk = is_2split(list_p_remain, group_weight);
        if(!isOk)
            continue;

        size_t qe = 1;
        for(auto indice: one) {
            qe *= static_cast<size_t>(list_packages[indice]);
        }


        if( qe < min_qe)
            min_qe = qe;

    }
    cout << "Nbp possibilities : " << res.size() << endl;

    cout << "part1 : "<< min_qe << endl;
}



void part2(const Vint& list_packages) {
    int tota_weight = sum(list_packages),
        group_weight = tota_weight/4;
    cout << "Total weight = " << tota_weight << ", per group = " << group_weight << endl;
    vector<Vint> res;
    min_package_nbr(list_packages, group_weight, res);
    size_t min_qe = pow(static_cast<size_t>(*max_element(begin(list_packages), end(list_packages))), res[0].size());
    cout << min_qe <<endl;

    for(auto& one: res) {
        auto list_p_remain = remaining(list_packages, one);
        auto isOk = is_3split(list_p_remain, group_weight);
        if(!isOk)
            continue;
        cout << "one sum : ";
        size_t qe = 1;
        for(auto indice: one) {
            qe *= static_cast<size_t>(list_packages[indice]);
            cout << list_packages[indice] << " ";
        }
        cout << " - qe :" << qe << endl;

        if( qe < min_qe)
            min_qe = qe;

    }
    cout << "Nbp possibilities : " << res.size() << endl;

    cout << "part2 : "<< min_qe << endl;

}

int main() {

    Vstring lines;
    read_lines("input", lines);

    Vint list_packages;
    for(auto& line: lines) {
        list_packages.push_back(stoi(line));
    }

    sort(rbegin(list_packages), rend(list_packages));

    part1(list_packages);

    part2({11, 10, 9, 8, 7, 5, 4, 3, 2, 1});
    part2(list_packages);

    return EXIT_SUCCESS;
}