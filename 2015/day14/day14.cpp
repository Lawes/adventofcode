#include "libwam.h"

using namespace std;
using namespace wam;


struct Info {
    string name;
    int speed, tfly, trest;

    int ttotal() const {
        return tfly + trest;
    }

    int dtotal() const {
        return speed * tfly;
    }

    int velocity(int t) const {
        int tremaining = t % ttotal();
        return (tremaining < tfly)? speed : 0;
    }

};

Info parse_line(const string& txt) {
    Vstring tokens = explode(txt, ' ');

    return {tokens[0], stoi(tokens[3]), stoi(tokens[6]), stoi(tokens[13])};
}

int distance_part1(const Info& flyer, int time) {
    auto nclycles = time / flyer.ttotal();
    int distance = nclycles * flyer.dtotal();
    auto tremaining = min(time % flyer.ttotal(), flyer.tfly);
    return distance + tremaining * flyer.speed;
}


void part2_point(const vector<Info>& flyers, int total_time) {

    Vint distances(flyers.size());
    Vint points(flyers.size());

    for(int t{}; t < total_time; ++t) {
        for(size_t i{}; i < flyers.size(); ++i) {
            const auto& f = flyers[i];

            distances[i] += f.velocity(t);
        }

        auto vmax = *max_element(distances.begin(), distances.end());
        for(size_t i{}; i < distances.size(); ++i) {
            if(distances[i] == vmax)
                points[i]++;
        }

    }

    for(size_t i{}; i < flyers.size(); ++i) {
        const auto& f = flyers[i];
        cout << f.name << " : " << points[i] << endl;
    }

    cout << "part2 " << *max_element(begin(points), end(points)) << endl;

}

int main() {
    Vstring lines;

    vector<Info> flyers;

    read_lines("input2", lines);
    for(auto& line: lines) {
        flyers.push_back(parse_line(line));
    }
    
    for(auto& e: flyers) {
        cout << e.name << " : speed=" << e.speed << ", tfly=" << e.tfly << ", trest=" << e.trest << " - distance=" << distance_part1(e, 1000) << endl;
    }

    part2_point(flyers, 1000);

    flyers.clear();
    read_lines("input", lines);
    for(auto& line: lines) {
        flyers.push_back(parse_line(line));
    }
    
    Vint alld;
    for(auto& e: flyers) {
        cout << e.name << " : speed=" << e.speed << ", tfly=" << e.tfly << ", trest=" << e.trest;
        auto d =  distance_part1(e, 2503);
        alld.push_back(d);
        cout << " -> distance = " << d << endl;
    }

    auto [vmin, vmax] = minmax_element(alld.begin(), alld.end());
    cout << "part1 " << *vmax << endl;

    part2_point(flyers, 2503);



}