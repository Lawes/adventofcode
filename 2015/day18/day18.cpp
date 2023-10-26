#include "libwam.h"

#include "Eigen/Eigen"

#include <iostream>

using namespace wam;
using namespace std;

typedef Eigen::ArrayXXi M;

int count_neighbors(const M& grid, int x, int y) {
    int count{};

    for(int dx{-1}; dx < 2; ++dx) {
        int xx = x + dx;
        if(xx < 0 || xx >= grid.rows()) continue;
        for(int dy{-1}; dy < 2; ++dy) {
            int yy = y + dy;
            if(yy < 0 || yy >= grid.cols())
                continue;
            if(grid(xx, yy) == 1) 
                count++;
        }
    }
    return count - grid(x, y);
}


void anim(M& grid) {
    M newgrid;
    newgrid.setZero(grid.rows(), grid.cols());

    for(int x{}; x < grid.rows(); ++x) {
        for(int y{}; y < grid.cols(); ++y) {
            int count = count_neighbors(grid, x, y);
            if(grid(x, y) == 1 && (count == 2 || count == 3))
                newgrid(x, y) = 1;
            else if(grid(x, y) == 0 && count == 3)
                newgrid(x, y) = 1;
        }
    }
    grid = newgrid;
}

void light_corners(M& grid) {
    grid(0, 0) = 1;
    grid(0, grid.cols() - 1) = 1;
    grid(grid.rows() - 1, grid.cols() - 1) = 1;
    grid(grid.rows() - 1, 0) = 1;
}

void set_from_lines(const Vstring& lines, M& grid) {
    grid.resize(lines.size(), lines[0].size());
    grid.setZero();

    for(size_t i{}; i < lines.size(); ++i) {
        const auto& line = lines[i];
        for(size_t j{}; j < line.size(); ++j) {
            if(line[j] == '#')
                grid(i, j) = 1;
        }
    }
}

int main() {
    Vstring lines;
    read_lines("input2", lines);

    M grid;
    
    set_from_lines(lines, grid);

    cout << grid << endl << endl;

    for(int i{}; i< 4; ++i)
        anim(grid);

    cout << grid << endl << "count " << grid.sum() << endl;;

    read_lines("input", lines);
    set_from_lines(lines, grid);

    for(int i{}; i< 100; ++i) {
        anim(grid);
    }

    cout << "part1 " << grid.sum() << endl;

    set_from_lines(lines, grid);
    light_corners(grid);

    for(int i{}; i< 100; ++i) {    
        anim(grid);
        light_corners(grid);
    }

    cout << "part2 " << grid.sum() << endl;

    return EXIT_SUCCESS;
}

