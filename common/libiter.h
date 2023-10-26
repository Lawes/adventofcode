#ifndef LIB_ITER_HEADER
#define LIB_ITER_HEADER

#include <cstddef>
#include <vector>
#include <numeric>


namespace wam {

    class BaseCombinatoric {
        public:
            typedef int Indice;
            typedef std::vector<Indice> Indices;

        private:
            Indice m_size;
        
        protected:
            Indices m_start, m_current;

        public:
            template<typename Iterator>
            BaseCombinatoric(Iterator begin, Iterator end) {
                std::copy(begin, end, std::back_inserter(m_start));
                m_size = m_start.size();
                m_current.resize(m_start.size());
                start();
            }

            BaseCombinatoric(Indice size) : m_size(size), m_start(size), m_current(size) {
                std::iota(std::begin(m_start), std::end(m_start), 0);
                start();
            }

            virtual ~BaseCombinatoric() = default;

            Indice size() const {
                return m_size;
            }

            void get(Indices& v) {
                v.resize(m_size);
                std::copy(std::begin(m_current), std::end(m_current), std::begin(v));
            }

            const Indices& get() const {
                return m_current;
            }

            void start() {
                std::copy(std::begin(m_start), std::end(m_start), std::begin(m_current));
            }

            virtual bool next() = 0;
    };

    class Combination : public BaseCombinatoric {
        private:
            Indice m_total;

        public:
            Combination(Indice n, Indice r) : BaseCombinatoric(r), m_total(n-1) {}
            virtual ~Combination() = default;

            virtual bool next();
    };


    class Combination_remplacement : public BaseCombinatoric {
        private:
            Indice m_total;

        public:
            Combination_remplacement(Indice n, Indice r) : BaseCombinatoric(r), m_total(n-1) {
                std::fill(std::begin(m_start), std::end(m_start), 0);
                start();
            }
            virtual ~Combination_remplacement() = default;

            virtual bool next();
    };


    class Permutation : public BaseCombinatoric {
        public:
            Permutation(Indice n) : BaseCombinatoric(n) {}
            template<typename Iterator>
            Permutation(Iterator begin, Iterator end): BaseCombinatoric(begin, end) {};

            virtual ~Permutation() = default;

            virtual bool next();
    };

    class Product: public Combination_remplacement{
        private:
            Indices m_vmax;
            Indice m_max;
        
        public:
            Product(Indice n, Indice r): Combination_remplacement(n, r), m_vmax(r) {std::fill(std::begin(m_vmax), std::end(m_vmax), n);}
            Product(const Indices& vmax): Combination_remplacement(vmax.size(), vmax.size()), m_vmax(vmax) {}
            virtual ~Product() = default;

            virtual bool next();
    };



    template<typename T>
    class OrderedRepartition {  
        public:
            typedef T Value;
            typedef std::vector<Value> Values;
        private:
            Value m_total;
            std::size_t m_r;
            Values m_current;

        public:
            OrderedRepartition(Value total, Value r): m_total(total), m_r(r), m_current(m_r, 0) {
                m_current.back() = total;
            }
            ~OrderedRepartition() = default;

            void start() {
                std::fill(std::begin(m_current), std::end(m_current), 0);
                m_current.back() = m_total;
            }
            
            const Values& get() const {
                return m_current;
            }

            bool next() {
                if(m_r == 1)
                    return false;

                std::size_t pos{0};
                Value sub{0};
                for(; pos < m_r; ++pos) {
                    if(m_current[0]+1 < m_current[pos])
                        break;
                    sub += m_current[pos];
                }
                if(pos == m_r)
                    return false;
                
                --m_current[pos--];
                auto d = sub + 1;

                do {
                    auto ref = m_current[pos+1];
                    if(d > ref) {
                        m_current[pos] = ref;
                        d -= ref;
                    }
                    else {
                        m_current[pos] = d;
                        d = 0;
                        for(std::size_t i{}; i < pos; ++i) m_current[i] = 0;
                        break;
                    }

                } while(d > 0 && pos-- !=0);
                return d == 0;
            }
    };

}


#endif