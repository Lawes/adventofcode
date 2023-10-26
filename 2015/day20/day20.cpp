#include "libwam.h"

#include <iostream>
#include <vector>
#include <cmath>
#include <functional>

using namespace std;
using namespace wam;

Vint fixed_primes{2, 3, 5, 7};

typedef pair<int, int> Factor;
typedef vector<Factor> Decomposition;


// https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
// https://en.wikipedia.org/wiki/Divisor_function


int robin_law(int n) {
    double dn = static_cast<double>(n);
    double exp_gamma = 1.78107241799019798523650410310717954d;
    double lln = log(log(n));

    return static_cast<int>(dn * (exp_gamma * lln + 0.6483d / lln));
}


int find_low_bound_bisec(int a, int b, function<int(int)> f) {
    auto bound = b;
    while(a < b) {
        int m = (a + b)/2;
        if(f(m) > bound)
            b = m;
        else
            a = m + 1;
    };
    return a;
}

class ErastotheneIter {
    private:
        Vshort m_v;
        int m_current, m_max;
    
    public:
        ErastotheneIter(int nmax) : m_v(nmax), m_max(nmax) {init();}
        ~ErastotheneIter() = default;

        void init() {
            m_v.resize(m_max);
            fill(begin(m_v), end(m_v), 1);
            for(int i=4; i < m_max; i += 2)
                m_v[i] = 0;
            m_current = 2;
        }

        int nextPrime() {
            if(m_v[m_current] != 1)
                while(m_current < m_max && m_v[m_current] == 0) m_current++;
            if(m_current == m_max)
                return -1;

            m_v[m_current] = 0;

            for(int j{m_current*m_current}; j < m_max; j += 2*m_current)
                m_v[j] = 0;
            // cout << "check " << m_current << " : ";
            // copy(begin(m_v), end(m_v), ostream_iterator<int>(cout, " "));
            // cout << endl;

            return m_current;
        }
};


Vint Erastothene(int limite) {
    Vint res{2};
    Vshort check(limite+1, 1);
    int i{};

    for(i=4; i <= limite; i += 2)
        check[i] = 0;
    check[1] = 0;

    i = 3;

    while(i <= limite) {
        if(check[i] == 1) {
            res.push_back(i);
            for(int j{i*i}; j <= limite; j += 2*i)
                check[j] = 0;
        }
        i++;
    };
    return res;
}


bool isPrime(int n) {
    for(auto i: fixed_primes) {
        if(n == i)
            return true;
        if( n > i && n % i == 0)
            return false;
    }

    for(int t{7}; t < static_cast<int>(sqrt(n) + 1); t += 2) {
        if(n % t == 0)
            return false;
    }

    return true;
}

int nextPrime(int n) {
    if(n == 1)
        return 2;
    if(n == 2)
        return 3;
    
    do {
        n += 2;
    } while(!isPrime(n));

    return n;
}


Decomposition factors(int n) {
    ErastotheneIter primeiter(static_cast<int>(sqrt(n)+0.5));
    Decomposition factorisation;
    int factor = primeiter.nextPrime();

    while(n != 1) {
        int e = 0;

        while(n % factor == 0) {
            n /= factor;
            e++;
        }
        if(e>0)
            factorisation.push_back({factor, e});

        factor = primeiter.nextPrime();
        if(factor < 0) break;
    }

    if(n != 1)
        factorisation.push_back({n, 1});


    return factorisation;
}


Decomposition factors_with_primes(int n, const Vint& primes) {
    size_t i{};

    Decomposition factorisation;
    int factor = primes[i++];

    while(n != 1) {
        int e = 0;

        while(n % factor == 0) {
            n /= factor;
            e++;
        }
        if(e>0)
            factorisation.push_back({factor, e});

        factor = primes[i++];
        if(i >= primes.size()) break;
    }

    if(n != 1)
        factorisation.push_back({n, 1});


    return factorisation;
}


void print_decomp(const Decomposition& decomp) {
    cout << "[" << decomp.size() << "] ";
    for(auto f: decomp) {
        cout << "(" << f.first << "," << f.second << ") ";
    }
    cout << endl;
}

Vint all_factors_from_decomp(const Decomposition& decomp) {
    Vint base_power;
    for(auto& f: decomp) {
        base_power.push_back(f.second + 1);
    }

    Vint all_factors;
    Product prod{base_power};
    do {
        const auto& exponents = prod.get();
        int n = 1;
        for(size_t i{}; i < exponents.size(); ++i) {
            n *= pow(decomp[i].first, exponents[i] - 1);
        }
        all_factors.push_back(n);
    } while(prod.next());

    return all_factors;
}



int sum_n_factors_with_primes(int n, int nbr, const Vint& primes) {
    Decomposition decomp = factors_with_primes(n, primes);
    Vint allfactors = all_factors_from_decomp(decomp);
    int s{};
    for(size_t i{}; i < allfactors.size(); ++i) {
        if(n <= nbr*allfactors[i])
            s += allfactors[i];
    }
    return s;
}



int sum_factors_with_primes(int n, const Vint& primes) {
    Decomposition decomp = factors_with_primes(n, primes);
    // cout << "n : " << n << " -> ";
    int res = 1;
    for(auto& f: decomp) {
        // cout << "(" << f.first << "," << f.second << ") ";
        res *= (pow(f.first, f.second + 1) - 1)/(f.first - 1);
    }
    // cout << " = " << res << endl;
    
    return res;
}

void part1() {
    int refsum = 29000000 / 10;
    auto startnum = find_low_bound_bisec(3, refsum, [](int n){ return robin_law(n);});
    cout << "solve : " <<  startnum << endl;

    int maxfactor = static_cast<int>(sqrt(startnum*2)+1);
    auto primes = Erastothene(maxfactor);
    copy(begin(primes), end(primes), ostream_iterator<int>(cout, " "));
    cout << endl;

    int sum_factors;
    do {
        if(startnum > maxfactor*maxfactor) {
            maxfactor *= 2;
            primes = Erastothene(maxfactor);
            cout << "change max factors : " << maxfactor << endl;
        }

        sum_factors = sum_factors_with_primes(startnum++, primes);      
    } while(sum_factors <=  refsum);
    cout << sum_factors_with_primes(startnum - 1, primes) << endl;
    cout << "part1 " << startnum - 1 << endl;
}


void part2() {
    int refsum = 29000000;
    auto startnum = find_low_bound_bisec(3, refsum, [](int n){ return robin_law(n)*11;});

    int maxfactor = static_cast<int>(sqrt(startnum*2)+1);
    auto primes = Erastothene(maxfactor);
    copy(begin(primes), end(primes), ostream_iterator<int>(cout, " "));
    cout << endl;

    int sum_factors;
    do {
        if(startnum > maxfactor*maxfactor) {
            maxfactor *= 2;
            primes = Erastothene(maxfactor);
            cout << "change max factors : " << maxfactor << endl;
        }
        sum_factors = sum_n_factors_with_primes(startnum++, 50, primes) * 11;
    } while(sum_factors <=  refsum);
    cout << "part2 " << startnum - 1 << endl;
}



int main() {
    int nmax = 40;

    for(int i{2}; i < nmax; i++)
        if(isPrime(i))
            cout << i << " ";
    cout << endl;

    auto p = Erastothene(nmax);
    for(auto i: p) {
        cout << i << " ";
    }
    cout << endl;

    {
        auto d = factors(125420);
        print_decomp(d);
        auto f = all_factors_from_decomp(d);
        cout << "All factors : ";
        copy(begin(f), end(f), ostream_iterator<int>(cout, " "));
        cout << endl;
    }




    ErastotheneIter primeiter(nmax);
    int prime;
    while((prime=primeiter.nextPrime())> 0) {
        cout << prime << " ";
    }
    cout << endl;

    Vint test{1000001, 100003};
    for(auto n: test) {
        cout << n << " : ";
        auto d = factors(n);
        print_decomp(d);
    }

    part1();

    part2();


    return EXIT_SUCCESS;
}
