#include "libwam.h"
#include <iostream>
#include <vector>

using namespace wam;
using namespace std;

struct Player {
    int life, dmg, armor, gold;
};

struct Object {
    string name;
    int cost, dmg, armor;
};

struct Stuff {
    int iweapon, iarmor, iring1, iring2;
};

typedef vector<Stuff> Stuffs;


vector<Object> weapons{
    {"Dagger", 8, 4, 0},
    {"Shortsword", 10, 5, 0},
    {"Warhammer", 25, 6, 0},
    {"Longsword", 40, 7, 0},
    {"Greataxe", 74, 8, 0}
};

vector<Object> armors{
    {"None", 0, 0, 0},
    {"Leather", 13, 0, 1},
    {"Chainmail", 31, 0, 2},
    {"Splintmail", 53, 0, 3},
    {"Bandedmail", 75, 0, 4},
    {"Platemail", 102, 0, 5}
};

vector<Object> rings{
    {"Damage +1", 25, 1, 0},
    {"Damage +2", 50, 2, 0},
    {"Damage +3", 100, 3, 0},
    {"Defense +1", 20, 0, 1},
    {"Defense +2", 40, 0, 2},
    {"Defense +3", 80, 0, 3}
};

void print_stuff(const Stuff& s) {
    cout << weapons[s.iweapon].name << " - ";
    cout << armors[s.iarmor].name << " - ";
    if(s.iring1 < 0)
        cout << "None";
    else
        cout << rings[s.iring1].name;
    cout << " - ";
    if(s.iring2 < 0)
        cout << "None";
    else
        cout << rings[s.iring2].name;
    cout << endl;
}

void equip(Player& p, const Object& o) {
    p.dmg += o.dmg;
    p.armor += o.armor;
    p.gold += o.cost;
}

Player shop(const Stuff& s) {
    Player p{100, 0, 0, 0};

    equip(p, weapons[s.iweapon]);
    equip(p, armors[s.iarmor]);
    if(s.iring1 >= 0)
        equip(p, rings[s.iring1]);
    if(s.iring2 >= 0)
        equip(p, rings[s.iring2]);

    return p;
}



Player parse_player(const Vstring& lines) {
    Player p;
    for(auto& line: lines) {
        auto tokens = explode(line, ' ');
        if(startswith(line, "Hit Points")) {
            p.life = stoi(tokens[2]);
        }
        else if(startswith(line, "Damage")) {
            p.dmg = stoi(tokens[1]);
        }
        else if(startswith(line, "Armor")) {
            p.armor = stoi(tokens[1]);
        }
    }
    return p;
}


void genAllStuffs(Stuffs& stuffs) {
    stuffs.clear();
    Vint sizes{static_cast<int>(weapons.size()), static_cast<int>(armors.size())};
    Product prod(sizes);
    do {
        const auto & indice = prod.get();
        stuffs.push_back({indice[0], indice[1], -1, -1});

        for(int i{}; i<static_cast<int>(rings.size()); ++i) {
            stuffs.push_back({indice[0], indice[1], i, -1});
        }
        Combination comb(rings.size(), 2);
        do {
            const auto & indice_ring = comb.get();
            stuffs.push_back({indice[0], indice[1], indice_ring[0], indice_ring[1]});
        }while(comb.next());

    } while(prod.next());
}


int winning_fight(Player p1, Player p2) {
    int dmg_12 = max(p1.dmg - p2.armor, 1);
    int dmg_21 = max(p2.dmg - p1.armor, 1);
    // cout << "dmg12 : " << dmg_12 << ", dmg21 : " << dmg_21 << endl;

    int tour12 = p2.life / dmg_12 + ((p2.life%dmg_12 == 0)? 0: 1);
    int tour21 = p1.life / dmg_21 + ((p1.life%dmg_21 == 0)? 0: 1);
    // cout << "1 kill 2 : " << tour12 << ", 2 kill 1 : " << tour21 << endl;
    return tour12 <= tour21? 1: 2;
}



void part1(const Player& boss) {
    vector<pair<Stuff, int>> winning;

    Player p;
    Stuffs stuffs;
    genAllStuffs(stuffs);
    for(auto& stuff: stuffs) {
        p = shop(stuff);
        if(winning_fight(p, boss) == 1) {
            winning.push_back({stuff, p.gold});
        }
    }

    cout << "winning configuration : " << winning.size() << endl;

    auto cmin = *min_element(begin(winning), end(winning), [](auto a, auto b){return a.second < b.second;});
    cout << "part1 " << cmin.second << endl;
    print_stuff(cmin.first);
}


void part2(const Player& boss) {
    vector<pair<Stuff, int>> loosing;

    Player p;
    Stuffs stuffs;
    genAllStuffs(stuffs);
    for(auto& stuff: stuffs) {
        p = shop(stuff);
        if(winning_fight(p, boss) == 2) {
            loosing.push_back({stuff, p.gold});
        }
    }
    auto cmin = *max_element(begin(loosing), end(loosing), [](auto a, auto b){return a.second < b.second;});
    cout << "part2 " << cmin.second << endl;
    print_stuff(cmin.first);

}

int main() {
    Vstring lines;
    read_lines("input", lines);

    auto boss = parse_player(lines);

    cout << boss.life << " " << boss.dmg << " " << boss.armor << endl;
    cout << winning_fight({8, 5, 5}, {2, 7, 2}) << endl;
    cout << winning_fight({8, 5, 5}, {14, 7, 2}) << endl;

    part1(boss);
    part2(boss);

    return EXIT_SUCCESS;
}
