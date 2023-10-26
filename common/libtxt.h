#ifndef LIB_HEADER_TEXT
#define LIB_HEADER_TEXT

#include <string>

namespace wam {
    bool startswith(const std::string& txt, const std::string& prefix) {
        //if(txt.size() < prefix.size())
        //    return false;
        
        return txt.compare(0, prefix.size(), prefix) == 0;
    }
}

#endif