#ifndef LIB_WAM_HEADER
#define LIB_WAM_HEADER

#include "libv.h"
#include "libio.h"
#include "libiter.h"
#include "libtxt.h"
#include "librandom.h"

#include <algorithm>
#include <iostream>
#include <iterator>


#ifdef MY_DEBUG_MODE
  #define debug_print(expr) std::cerr << expr << std::endl;
  #define debug_disp(expr)  std::cerr << __FILE__ << ":" << __LINE__ << ":"  << " ; " <<  #expr << " = " << (expr)  <<  std::endl
  #define debug_loc(msg)  std::cerr << __FILE__ << ":" << __LINE__ << ":" << msg 
  #define debug_line __FILE__ << ":" << __LINE__ << ":" <<

#else
  #define debug_print(expr)
  #define debug_disp(expr) 
  #define debug_loc(msg)  
  #define debug_line 
#endif 


namespace wam {

    template<typename T>
    typename T::value_type sum(const T& v) {
        typename T::value_type res{0};

        for(auto elem: v)
            res += elem;
        
        return res;
    }

    template<typename T>
    typename T::value_type prodV(const T& v) {
        typename T::value_type res{1};

        for(auto elem: v)
            res *= elem;
        
        return res;
    }

}


#endif