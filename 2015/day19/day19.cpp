#include "libwam.h"

#include <iostream>
#include <algorithm>
#include <list>
#include <map>
#include <set>

using namespace wam;
using namespace std;

typedef string Molecule;


struct MoleculeComp {
    bool operator() (const Molecule&a, const Molecule&b) const {
        if(a.size() < b.size()) return true;
        return a < b;
    }
};

typedef set<Molecule, MoleculeComp>  MoleculeContainer;


struct Replace {
    Molecule key;
    Molecule rep;
    int size;
};

typedef vector<Replace> Machine;

Molecule parse_molecule(const string& txt) {
    Molecule res;

    for(size_t i{}; i < txt.size(); ++i) {
        if(txt[i] >= 'a' && txt[i] <= 'z')
            res.pop_back();
        res += txt[i];
        res += ' ';
    }
    return res;
}

int count_elements(const Molecule& molecule) {
    return std::count(begin(molecule), end(molecule), ' ');
}

Replace parse_replacement(const string& txt) {
    auto tokens = explode(txt, ' ');
    auto mol =  parse_molecule(tokens[2]);
    int s = count_elements(mol);

    return {tokens[0] + ' ', mol, s};
}


void generate_all(const Machine& machine, MoleculeContainer& molecules) {
    MoleculeContainer all;

    for(auto it = rbegin(molecules); it != rend(molecules); ++it) {
        const auto& molecule = *it;

        for(auto& rep: machine) {
            auto kinit = rep.key;
            auto kreplace = rep.rep;

            auto indice = molecule.find(kinit);            
            while(indice != string::npos) {
                // cout << "    find " << indice << endl;
                Molecule newone{molecule};
                newone.replace(indice, kinit.size(), kreplace);

                all.insert(newone);
                indice = molecule.find(kinit, indice+1);
            }
        }
    }
    molecules = all;
}


bool reduce_all(const Machine& machine, MoleculeContainer& molecules) {
    MoleculeContainer all;
    bool tocheck = false;

    for(auto it = rbegin(molecules); it != rend(molecules); ++it) {
        const auto& molecule = *it;

        for(auto& rep: machine) {
            auto kinit = rep.key;
            auto kreplace = rep.rep;

            auto indice = molecule.find(kreplace);            
            while(indice != string::npos) {
                // cout << "    find " << indice << endl;
                Molecule newone{molecule};
                newone.replace(indice, kreplace.size(), kinit);

                if(newone.size() == 2)
                    tocheck = true;

                all.insert(newone);
                indice = molecule.find(kreplace, indice+1);
            }
        }
    }
    molecules = all;
    return tocheck;
}


int main() {
    Vstring lines;
    read_lines("input", lines);

    Machine replacements;

    for(size_t i{}; i < lines.size() - 1; ++i) {
        replacements.push_back(parse_replacement(lines[i]));
        cout << replacements.back().key << " : " << replacements.back().rep << ", " << replacements.back().size <<  endl;
    }


    Molecule molecule = parse_molecule(lines.back());
    cout << molecule << endl;
    // copy(begin(molecule), end(molecule), ostream_iterator<string>(cout, " "));
    cout << endl;

    MoleculeContainer all{molecule};

    generate_all(replacements, all);

    cout << "part1 " << all.size() << endl;

    all.clear();

    all.insert(molecule);
    int step = 0;
    bool searching = true;
    while(searching) {
        step++;
        if(reduce_all(replacements, all)) {
            for(auto& m: all) {
                if(m == "e ") {
                    searching = false;
                    break;
                }
            }
        }
        cout << "step " << step << " : " << all.size() << endl;
    };

    cout << "part2 :" << step << endl;


    return EXIT_SUCCESS;
}