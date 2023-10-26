#ifndef LIB_VECTOR_HEADER
#define LIB_VECTOR_HEADER

#include <vector>
#include <string>
#include <algorithm>
#include <iterator>
#include <iostream>

namespace wam {
    typedef std::vector<std::string> Vstring;
    typedef std::vector<int> Vint;
    typedef std::vector<short> Vshort;

    template<typename V>
    void printV(const V& array, bool endl=true) {
        std::copy(std::begin(array), std::end(array), std::ostream_iterator<typename V::value_type>(std::cout, " "));
        if(endl)
            std::cout << std::endl;
    }
}


#endif