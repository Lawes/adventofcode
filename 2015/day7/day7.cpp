#include <map>
#include <string>
#include <sstream>
#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>

using namespace std;

enum class OperationType {
    Assign,
    And,
    Or,
    Not,
    Lshift,
    Rshift
};

struct Operation {
    OperationType type;
    string store, a, b, raw;
};


class Machine {
    public:
        typedef unsigned short value_type;
        typedef string key_type;

    private:
        map<key_type, value_type> m_memory;
    

        bool op_assign(key_type key, key_type a) {
            bool res {false};
            if(m_memory.find(key) != end(m_memory))
                return res;

            value_type va;
            if(get_value(a, va)) {
                res = true;
                m_memory[key] = va;
            }
            return res;
        }

        bool op_and(key_type kout, key_type a, key_type b) {
            bool res {false};
            value_type va, vb;
            if(get_value(a, va) && get_value(b, vb)) {
                res = true;
                m_memory[kout] = va & vb;
            }
            return res;
        }
        bool op_lshift(key_type kout, key_type a, key_type b) {
            bool res {false};
            value_type va, vb;
            if(get_value(a, va) && get_value(b, vb)) {
                res = true;
                m_memory[kout] = va << vb;
            }
            return res;
        }
    
        bool op_rshift(key_type kout, key_type a, key_type b) {
            bool res {false};
            value_type va, vb;
            if(get_value(a, va) && get_value(b, vb)) {
                res = true;
                m_memory[kout] = va >> vb;
            }
            return res;
        }
        bool op_not(key_type kout, key_type a) {
            bool res {false};
            value_type va;
            if(get_value(a, va)) {
                res = true;
                m_memory[kout] = ~va;
            }
            return res;
        }

        bool op_or(key_type kout, key_type a, key_type b) {
            bool res {false};
            value_type va, vb;
            if(get_value(a, va) && get_value(b, vb)) {
                res = true;
                m_memory[kout] = va | vb;
            }
            return res;
        }

    public:
        Machine() = default;

        void reset_value() {
            m_memory.clear();
        }

        void set_value(key_type a, value_type b) {
            m_memory[a] = b;
        }

        bool get_value(key_type a, value_type& b) {
            bool res = false;
            if(a[0] >= '0' && a[0] <= '9') {
                res = true;
                b = stoi(a);
            }
            else {
                auto it = m_memory.find(a);
                if(it != end(m_memory)) {
                    res = true;
                    b = it->second;
                }
            }
            return res;
        }

        bool play(const Operation& op) {
            bool action {false};

            switch (op.type)
            {
            case OperationType::Assign:
                action = op_assign(op.store, op.a);
                break;
            case OperationType::And:
                action = op_and(op.store, op.a, op.b);
                break;
            case OperationType::Or:
                action = op_or(op.store, op.a, op.b);
                break;
            case OperationType::Lshift:
                action = op_lshift(op.store, op.a, op.b);
                break;
            case OperationType::Rshift:
                action = op_rshift(op.store, op.a, op.b);
                break;
            case OperationType::Not:
                action = op_not(op.store, op.a);
                break;
            default:
                break;
            }

            return action;
        }

        void display() {
            for(auto&v : m_memory) {
                cout << v.first << " : " << v.second << endl;
            }
        }
};



std::vector<string> explode(std::string str, char delimiter)
{
    std::vector<string> output;
    std::stringstream ss(str);
    std::string token;

    while (getline(ss, token, delimiter)) {
        if (token.size() > 0)
            output.push_back(token);
    }

    return output;
}

bool load_input(const char *filename, vector<Operation>& instructions) {
    string line;

    instructions.clear();

    ifstream flux(filename);
    if(!flux) {
        cerr << "Unable to load " << filename << endl;
        return false;
    }

    string type;
    while(getline(flux, line)) {
        if(line.size() > 0) {
            auto tokens = explode(line, ' ');
            Operation op;

            if(tokens.size() == 3) {
                op.raw = tokens[1];
                op.type = OperationType::Assign;
                op.store = tokens[2];
                op.a = tokens[0];
            }
            else if(tokens.size() == 4) {
                op.type = OperationType::Not;
                op.raw = tokens[0];
                op.store = tokens[3];
                op.a = tokens[1];
            }
            else if(tokens[1] == "AND") {
                op.type = OperationType::And;
                op.raw = tokens[1];
                op.store = tokens[4];
                op.a = tokens[0];
                op.b = tokens[2];
            }
            else if(tokens[1] == "OR") {
                op.type = OperationType::Or;
                op.raw = tokens[1];
                op.store = tokens[4];
                op.a = tokens[0];
                op.b = tokens[2];
            }
            else if(tokens[1] == "LSHIFT") {
                op.type = OperationType::Lshift;
                op.raw = tokens[1];
                op.store = tokens[4];
                op.a = tokens[0];
                op.b = tokens[2];
            }
            else if(tokens[1] == "RSHIFT") {
                op.type = OperationType::Rshift;
                op.raw = tokens[1];
                op.store = tokens[4];
                op.a = tokens[0];
                op.b = tokens[2];
            }
            instructions.push_back(op);
        }

    }

    return true;
}


int main() {
    vector<Operation> input, instructions;
    load_input("input", input);

    copy(input.begin(), input.end(), back_inserter(instructions));

    auto device = Machine();

    bool hasChanged {true};

    while(hasChanged) {
        hasChanged = false;
        vector<Operation> remaining;
        for(const auto& op: instructions) {
            if(device.play(op)) {
                hasChanged = true;
                // cout << "success " << op.raw << " : " << op.store << " " << op.a << " " << op.b << endl;
            }
            else {
                remaining.push_back(op);
            }
        }
        instructions = remaining;
    }

    Machine::value_type part1;
    device.get_value("a", part1);
    cout << "part1 " << part1 << endl;

    instructions.clear();
    copy(input.begin(), input.end(), back_inserter(instructions));
    device.reset_value();
    device.set_value("b", part1);
    device.display();
    hasChanged = true;

    while(hasChanged) {
        hasChanged = false;
        vector<Operation> remaining;
        for(const auto& op: instructions) {
            if(device.play(op)) {
                hasChanged = true;
                // cout << "success " << op.raw << " : " << op.store << " " << op.a << " " << op.b << endl;
            }
            else {
                remaining.push_back(op);
            }
        }
        instructions = remaining;
    }

    Machine::value_type part2;
    device.get_value("a", part2);
    cout << "part2 " << part2 << endl;

   return EXIT_SUCCESS;
}