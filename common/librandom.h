#ifndef _LIB_RANDOM_HEADER
#define _LIB_RANDOM_HEADER

#include <random>
#include <iterator>
#include <chrono>

namespace wam {
    class Random {
        private:
            std::mt19937 _gen;

        public:
            Random(size_t seed) {
                _gen = std::mt19937(seed);
            }

            Random() {
                _gen = std::mt19937(std::chrono::high_resolution_clock::now().time_since_epoch().count());
            }

            int uniform_int(int mi, int ma) {
                std::uniform_int_distribution<int> rand(mi, ma);
                return rand(_gen);
            }

            template<typename T>
            typename T::iterator uniform_choice(T &v) {
                std::uniform_int_distribution<size_t> rand(0, v.size());
                return std::begin(v) + rand(_gen);
            }
    };

}


#endif