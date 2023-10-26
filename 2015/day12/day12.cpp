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

#include <boost/json/src.hpp>


using namespace std;


typedef vector<string> Vstring;
typedef vector<int> Vint;


bool load_input(const char *filename, Vstring& lines) {
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


void extract_number(const string& txt, Vint& v) {
    v.clear();

    int current=0, sign=1;
    bool isNum=false;

    for(size_t i{}; i < txt.size(); ++i) {
        if(txt[i] >= '0' && txt[i] <= '9') {
            isNum = true;
            current = current*10 + txt[i] - '0';
        }
        else if(txt[i] == '-')
            sign = -1;
        else {
            if(isNum) {
                v.push_back(current*sign);
                current = 0;
                isNum = false;
            }
            sign = 1;
        }
    }
}


boost::json::value parse_json(const string& txt) {
    boost::json::value jv;
    try {
        boost::json::error_code ec;
         jv = boost::json::parse(txt, ec);
        if( ec )
            std::cout << "Parsing failed: " << ec.message() << "\n";
    }
    catch(std::bad_alloc const& e) {
        std::cout << "Parsing failed: " << e.what() << "\n";
    }

    return jv;
}


int extract_num_json(const boost::json::value& jv) {
    int res = 0;

    switch(jv.kind())
    {
    case boost::json::kind::object:
    {
        auto const& obj = jv.get_object();
        for(auto it = obj.begin(); it != obj.end(); ++it) {
            // it->key();
            res += extract_num_json( it->value());
        }
        break;
    }

    case boost::json::kind::array:
    {
        auto const& arr = jv.get_array();
        for(auto it = arr.begin(); it != arr.end(); ++it) {
            res += extract_num_json(*it);
        }
        break;
    }

    case boost::json::kind::string:
    {
        jv.get_string();
        break;
    }

    case boost::json::kind::uint64:
        res += jv.get_uint64();
        break;

    case boost::json::kind::int64:
        res += jv.get_int64();
        break;

    case boost::json::kind::double_:
        jv.get_double();
        break;

    default:
        break;

    }

    return res;
}

bool has_red(const boost::json::value& jv) {
    if(jv.kind() == boost::json::kind::object) {
        auto const& obj = jv.get_object();
        for(auto it = obj.begin(); it != obj.end(); ++it) {
            if(it->key() == "red") {
                return true;
            }
            auto val = it->value();
            if( val.kind() == boost::json::kind::string)
                if(val.get_string() == "red")
                    return true;
        } 
    }

    return false;
}


int extract_num_json2(const boost::json::value& jv) {
    int res = 0;

    switch(jv.kind())
    {
    case boost::json::kind::object:
    {
        auto const& obj = jv.get_object();
        if(!has_red(obj))
            for(auto it = obj.begin(); it != obj.end(); ++it) {
                // it->key();
                res += extract_num_json2( it->value());
            }
        break;
    }

    case boost::json::kind::array:
    {
        auto const& arr = jv.get_array();
        for(auto it = arr.begin(); it != arr.end(); ++it) {
            res += extract_num_json2(*it);
        }
        break;
    }

    case boost::json::kind::string:
    {
        jv.get_string();
        break;
    }

    case boost::json::kind::uint64:
        res += jv.get_uint64();
        break;

    case boost::json::kind::int64:
        res += jv.get_int64();
        break;

    case boost::json::kind::double_:
        jv.get_double();
        break;

    default:
        break;

    }

    return res;
}



template<typename T>
int sum(const T& v) {
    typename T::value_type res{0};

    for(auto elem: v)
        res += elem;
    
    return res;
}


int main() {
    Vstring lines;
    Vint v;

    {
        vector<string> tests {"[1,-2,3]", "{\"a\":-2,\"b\":4}", "[[[3]]]", "{\"a\":[-1,1]}", "{}", "[]"};
        for(auto txt: tests) {
            extract_number(txt, v);
            cout << txt << " : ";
            copy(v.begin(), v.end(), ostream_iterator<int>(cout, " "));
            cout << ", sum1=" << sum(v);


            auto jv = parse_json(txt);
            cout << ", sum2=" << extract_num_json(jv) << endl;
        }

    }

    load_input("input", lines);

    extract_number(lines[0], v);
    cout << "part1 " << sum(v) << " : " << extract_num_json(parse_json(lines[0])) << endl;
    cout << "part2 " << extract_num_json2(parse_json(lines[0])) << endl;

}