#include "libwam.h"

#include <string>
#include <iostream>
#include <list>
#include <memory>

using namespace wam;
using namespace std;


struct Player {
    int life, dmg, armor, mana;
};


ostream& operator<<(ostream& flux, const Player& p) {
    flux <<  "Entity: life=" << p.life << ", mana=" << p.mana << ", armor=" << p.armor;
    return flux;
}


struct Players {
    Player player, boss;
};

struct Spell {
    string name;
    int cost, timer;

    Spell(const string&s, int c, int t): name(s), cost(c), timer(t) {}
    virtual ~Spell() {}

    bool hasDot() {
        return timer > 0;
    }

    bool enter(Players& pstate) {
        debug_print("Cast " << name << " - " << cost << " - " << pstate.player.mana)
        if(cost > pstate.player.mana)
            return false;

        pstate.player.mana -= cost;
        _enter(pstate);
        return true;
    }
    virtual void _enter(Players& pstate) {}
    virtual void _action(Players& pstate) {}

    bool action(Players& pstate) {
        timer--;
        _action(pstate);
        debug_print(name << " timer " << timer)
        return timer>0;
    }
    virtual void end(Players& pstate) {};
};


typedef unique_ptr<Spell> SpellPtr;


struct MagicMissile : Spell {
    MagicMissile(): Spell("magic", 53, -1) {}
    virtual ~MagicMissile() {}

    virtual void _enter(Players& pstate) {
        pstate.boss.life -= 4;
        debug_print("drain damage, boss=" << pstate.boss.life)
    }

};

struct Drain: Spell {
    Drain() : Spell("drain", 73, -1) {}
    virtual ~Drain() {}

    virtual void _enter(Players& pstate) {
        pstate.boss.life -= 2;
        pstate.player.life += 2;
    }
};

struct Shield : Spell {
    Shield() : Spell("shield", 113, 6) {}
    virtual ~Shield() {}

    virtual void _enter(Players& pstate) {
        pstate.player.armor += 7;
    }

    virtual void end(Players& pstate) {
        pstate.player.armor -= 7;
    }
};

struct Poison : Spell {
    Poison() : Spell("poison", 173, 6) {}
    virtual ~Poison() {}

    virtual void _action(Players& pstate) {
        pstate.boss.life -= 3;
        debug_print("poison damage, boss=" << pstate.boss.life)
    }
};

struct Recharge : Spell {
    Recharge() : Spell("recharge", 229, 5) {}
    virtual ~Recharge() {}

    virtual void _action(Players& pstate) {
        pstate.player.mana += 101;
        debug_print("gain mana " << pstate.player.mana)
    }
};


SpellPtr spell_factory(const string& name) {
    if(name == "magic")
        return make_unique<MagicMissile>();
    else if(name == "drain")
        return make_unique<Drain>();
    else if(name == "shield")
        return make_unique<Shield>();
    else if(name == "poison")
        return make_unique<Poison>();
    
    return make_unique<Recharge>();
}





struct Game {
    int winner{}, total_mana{};
    bool isHard;
    Players entities;
    list<SpellPtr> effects;

    Game(Player player, Player boss, bool hard): isHard(hard), entities{player, boss} {}

    void resolve_effects() {
        debug_print("resolve effects " << effects.size())
        auto it = begin(effects);
        for(; it != end(effects); ++it) {
            if(! (*it)->action(entities)) {
                (*it)->end(entities);
                effects.erase(it--);
            }
        }
        debug_print("end effects " << effects.size())
    }

    bool hasWinner() {
        return winner != 0;
    }

    bool turn(const string& spellname) {
        if(isHard){
            entities.player.life -= 1;
            if(entities.player.life <= 0) {
                winner = 2;
                return true;
            }
        }
        debug_print(endl << "* Player turn")
        debug_print("player -> " << entities.player)
        debug_print("bos    -> " << entities.boss)
    
        resolve_effects();
        if(entities.boss.life <= 0) {
            winner = 1;
            return true;
        }

        for(const auto &s: effects)
            if(s->name == spellname)
                return false;

        debug_print("generate spell " << spellname)
        auto spell = spell_factory(spellname);

        if(!spell->enter(entities))
            return false;

        total_mana += spell->cost;
        if(entities.boss.life <= 0) {
            winner = 1;
            return true;
        }


        if(spell->hasDot())
            effects.push_back(std::move(spell));


        debug_print(endl << "* Boss turn")
        debug_print("player -> " << entities.player)
        debug_print("bos    -> " << entities.boss)

        resolve_effects();
        if(entities.boss.life <= 0) {
            winner = 1;
            return true;
        }

        int dmg = max(entities.boss.dmg - entities.player.armor, 1);
        debug_print("Boss attack " << dmg)
        entities.player.life -= dmg;
        if(entities.player.life <= 0) {
            winner = 2;
        }

        return true;     
    }

    int play(const Vstring& spells) {

        for(auto& spell: spells) {
            if(!turn(spell))
                return -1;

            if(hasWinner())
                return winner;
        }
        return winner;
    }

};

typedef vector<pair<int, Vstring>> Stack;


void explore(Player player, Player boss, bool hard) {
    int min_mana = 100000;
    Vstring min_cast;

    Vstring spells{"recharge", "shield", "drain", "poison", "magic"};

    Stack stack;

    for(auto spell: spells)
        stack.push_back({0, {spell}});

    while(!stack.empty()) {
        auto elem = stack.back();
        stack.pop_back();

        if(elem.first > min_mana)
            continue;

        auto g = Game(player, boss, hard);
        auto status = g.play(elem.second);
        if(status == -1 || status == 2)
            continue;
        else if(status == 1) {
            if(g.total_mana < min_mana) {
                min_mana = g.total_mana;
                min_cast = elem.second;
                cout << "find : " << g.total_mana << " - ";
                printV(elem.second);
                //cout << "MINIMUM" << endl;
            }
        }
        else {
            for(auto spell: spells) {
                Vstring cast(elem.second);
                cast.push_back(spell);
                stack.push_back({g.total_mana, cast});
            }
        }
    }

}


int main() {
    auto g = Game({10, 0, 0, 250}, {14, 8, 0, 0}, false);

    auto status = g.play({"recharge", "shield", "drain", "poison", "magic"});

    cout << "end " << status << endl;
    cout << g.entities.player << endl;
    cout << g.entities.boss << endl;


    explore({10, 0, 0, 250}, {14, 8, 0, 0}, false);

    cout << "part1" << endl;
    explore({50, 0, 0, 500}, {58, 9, 0, 0}, false);
    cout << "part2" << endl;
    explore({50, 0, 0, 500}, {58, 9, 0, 0}, true);

    return EXIT_SUCCESS;
}


