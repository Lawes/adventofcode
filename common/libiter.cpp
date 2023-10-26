#include "libiter.h"
// #include "impl/combination.hpp"

#include <algorithm>
#include <numeric>
#include <iterator>

using namespace std;

bool wam::Combination::next() {
    const auto lengthOfSubsequence = size();
    auto viewed_element_it = rbegin(m_current);
    auto reversed_begin = rend(m_current);

    /*Looking for this element here*/

    while ((viewed_element_it != reversed_begin) && 
           (*viewed_element_it >= m_total -
                                  lengthOfSubsequence + 
                                  std::distance(viewed_element_it, reversed_begin))) {
        //std::distance shows position of element in subsequence here
        viewed_element_it++;
    }

    if (viewed_element_it == reversed_begin)
        return false;

    auto it = std::prev(viewed_element_it.base());

    /*
        Increment the found element. 
        The rest following elements we set as seqeunce[pos] = seqeunce[pos-1] + 1
    */
    iota(it, end(m_current), *it + 1);

    return true;
}


bool wam::Combination_remplacement::next() {
    auto viewed_element_it = rbegin(m_current);
    auto reversed_begin = rend(m_current);

    /*Looking for this element here*/

    while ((viewed_element_it != reversed_begin) && 
           (*viewed_element_it >= m_total)) {
        viewed_element_it++;
    }

    if (viewed_element_it == reversed_begin)
        return false;

    auto it = std::prev(viewed_element_it.base());

    fill(it, end(m_current), *it + 1);

    return true;
}

bool wam::Permutation::next() {
    return next_permutation(begin(m_current), end(m_current));
}

bool wam::Product::next() {
    auto it = rbegin(m_current);
    auto reversed_begin = rend(m_current);

    for(; it != reversed_begin; ++it) {
        auto indice = distance(it, reversed_begin);
        if(*it + 1 < m_vmax[indice-1]) {
            (*it)++;
            break;
        }
        else {
            *it = 0;
        }
    }

    return it != reversed_begin;

}