#include "libio.h"

#include <sstream>
#include <fstream>
#include <iostream>

using namespace std;


wam::Vstring wam::explode(string str, char delimiter)
{
    wam::Vstring output;
    stringstream ss{str};
    string token;
    while (getline(ss, token, delimiter)) {
        if (token.size() > 0)
            output.push_back(token);
    }
    return output;
}

bool wam::read_lines(const char *filename, wam::Vstring& lines) {
    string line;

    lines.clear();

    ifstream flux(filename);
    if(!flux) {
        cerr << "Unable to load " << filename << endl;
        return false;
    }

    while(getline(flux, line)) {
        if(line.size() > 0)
            lines.push_back(line);
    }
    return true;
}