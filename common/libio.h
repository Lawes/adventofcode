#ifndef MY_LIBIO_HEADER
#define MY_LIBIO_HEADER

#include "libv.h"

namespace wam {

    Vstring explode(std::string str, char delimiter);
    bool read_lines(const char *filename, Vstring& lines);

}


#endif