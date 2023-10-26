#include "libwam.h"

#include <map>
#include <iostream>
#include <memory>
#include <functional>

using namespace std;
using namespace wam;


struct Memory {
    map<string, int> registers;
    int next_jump;
};

struct Instruction {
    typedef function<void(const string&, int, Memory&)> InstructionFunc;
    string reg;
    int jump{1};
    InstructionFunc func;
    Instruction(const string& name, InstructionFunc f) : reg{name}, jump(1), func{f} {}
    Instruction(const string& name, int j, InstructionFunc f) : reg{name}, jump(j), func{f} {}
    void exec(Memory& mem) const {
        func(reg, jump, mem);
    }
};


typedef vector<Instruction> InstructionSequence;


Instruction instructionFactory(const string& line) {
    auto tokens = explode(line, ' ');
    if(tokens[0] == "hlf")
        return {
            tokens[1],
            [](const string& r, int j, Memory& m) {
                m.registers[r] /= 2;
                m.next_jump = j;
            }
        };
    else if(tokens[0] == "tpl")
        return {
            tokens[1],
            [](const string& r, int j, Memory& m) {
                m.registers[r] *= 3;
                m.next_jump = j;
            }
        };
    else if(tokens[0] == "inc")
        return {
            tokens[1],
            [](const string& r, int j, Memory& m) {
                m.registers[r]++;
                m.next_jump = j;
            }
        };
    else if(tokens[0] == "jmp")
        return {
            "",
            stoi(tokens[1]),
            [](const string& r, int j, Memory& m) {
                m.next_jump = j;
            }
        };
    else if(tokens[0] == "jie") {
        tokens[1].pop_back();

        return {
            tokens[1],
            stoi(tokens[2]),
            [](const string& r, int j, Memory& m) {
                m.next_jump = (m.registers[r]%2 == 0)? j: 1;
            }
        };
    }

    tokens[1].pop_back();
        return {
            tokens[1],
            stoi(tokens[2]),
            [](const string& r, int j, Memory& m) {
                m.next_jump = (m.registers[r] == 1)? j: 1;
            }
        };
}

struct Processor {
    Memory mem;

    Processor() : mem{{{"a", 0}, {"b", 0}}, 1} {}

    void init() {
        mem.registers = {{"a", 0}, {"b", 0}};
    }
    void set(const string& name, int val) {
        mem.registers[name] = val;
    }

    int get(const string& name) {
        return mem.registers[name];
    }

    void execute(const InstructionSequence& seq) {
        int indice{};

        while(indice < seq.size()) {
            seq[indice].exec(mem);
            indice += mem.next_jump;
        }
    }
};

int main() {
    Vstring lines;
    read_lines("input", lines);

    InstructionSequence seq;

    for(auto &line: lines) {
        seq.push_back(instructionFactory(line));
    }

    Processor proc;

    proc.execute(seq);

    cout << "part1 " << proc.get("b") << endl;

    proc.init();
    proc.set("a", 1);
    proc.execute(seq);
    cout << "part2 " << proc.get("b") << endl;

    return EXIT_SUCCESS;
}