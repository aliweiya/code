/*
 * 编译： g++ main.cpp --std=c++17 -lstdc++fs
 */
#include<iostream>
#include<fstream>
#include<string> // getline
#include<experimental/filesystem>

using namespace std;

namespace fs = std::experimental::filesystem;

#define USAGE(prog_name) printf("usage: %s file_list source_path target_path\n", prog_name);

#ifdef _WIN32
#define PATH_SEP '\\'
#else
#define PATH_SEP '/'
#endif

int main(int argc, char* argv[]) {
    if (argc < 3) {
        USAGE(argv[0]);
        exit(EXIT_FAILURE);
    }

    ifstream fin(argv[1]);

    string line;
    if (!fin.is_open()) {
        perror(argv[1]);
        return EXIT_FAILURE;
    }

    while (getline(fin, line)) {
        string source = argv[2];
        if (source[source.length()-1] != PATH_SEP)
            source += PATH_SEP;
        source.append(line, 0, 2);
        source += PATH_SEP;
        source.append(line, 2, 2);
        source += PATH_SEP;
        source.append(line);

        string target = argv[3];
        if (target[target.length() - 1] != PATH_SEP)
            target += PATH_SEP;
        target += line;

        cout << "copy " << source << " to " << target << endl;
        
        try {
            fs::copy(source, target);
        }
        catch (const fs::filesystem_error &e) {
            // https://en.cppreference.com/w/cpp/filesystem/filesystem_error
            cout << e.what() << endl;
        }
    }

    fin.close();
}