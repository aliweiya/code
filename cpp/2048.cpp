#include<iostream>
#include<iomanip> // setw
#include<ctime>
#include<vector>

#ifdef _WIN32
#include<conio.h> // getch
#else
#include<ncurses.h> // getch
#include<cstring> // memset
#endif

using namespace std;

struct Point {
    int x;
    int y;

    Point(int x, int y) :x(x), y(y) {};
};

class Game {
public:
    Game();
    int main();

private:
    const static int rows = 4;
    const static int cols = 4;
    unsigned seed;

    unsigned long score = 0;

    int panel[rows][cols] = { { 0 } };
    int new_choices[2] = { 2, 4 };
    string tab[12] = { "┌", "─", "┬", "┐", "│", "├", "┤",  "└", "┴", "┘", "┼" };


    void show();
    void reset();
    void add();
    int get_num_length();
    Point get_empty_location();

    void merge(vector<int>& vec, int i, int j);

    bool check_if_movable();

    void move_w();
    void move_a();
    void move_s();
    void move_d();
};

Game::Game() {
    seed = time(0);
    srand(seed);
}

int Game::main() {
    reset();
    show();

    char c;

    // Esc to exit
    while ((c = getch()) != 0x1B) {
        switch (c) {
        case 'w':
        case 'W':
            move_w();
            break;
        case 'a':
        case 'A':
            move_a();
            break;
        case 's':
        case 'S':
            move_s();
            break;
        case 'd':
        case 'D':
            move_d();
            break;
        default:
            cerr << "invalid key " << c;
        }
        cout << endl;
    }
    return 0;
}

int Game::get_num_length() {
    int result = 1;
    int max_num = 0;

    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            max_num = max(max_num, panel[i][j]);

    while (max_num >= 10) {
        max_num /= 10;
        result++;
    }

    return result;
}

void Game::reset() {
    memset(panel, 0, sizeof(panel));

    for (int i = 0; i < 2; i++) {
        add();
    }
}

void Game::add() {
    try {
        Point point = get_empty_location();
        panel[point.x][point.y] = new_choices[rand() % sizeof(new_choices) / (sizeof(int))];
    }
    catch (runtime_error& err) {
        if (!check_if_movable())
            throw;
    }
}

void Game::move_w() {
    for (int j = 0; j < cols; j++) {
        vector<int> vec;
        for (int i = 0; i < rows; i++) {
            merge(vec, i, j);
        }

        size_t vec_index = 0;
        for (int i = 0; i < rows; i++) {
            if (vec_index < vec.size())
                panel[i][j] = vec[vec_index++];
            else {
                panel[i][j] = 0;
            }
        }
    }
    add();
    show();
}

void Game::move_a() {
    for (int i = 0; i < rows; i++) {
        vector<int> vec;
        for (int j = 0; j < cols; j++) {
            merge(vec, i, j);
        }

        size_t vec_index = 0;
        for (int j = 0; j < cols; j++) {
            if (vec_index < vec.size())
                panel[i][j] = vec[vec_index++];
            else {
                panel[i][j] = 0;
            }
        }
    }
    add();
    show();
}

void Game::move_s() {
    for (int j = 0; j < cols; j++) {
        vector<int> vec;
        for (int i = rows - 1; i >= 0; i--) {
            merge(vec, i, j);
        }

        size_t vec_index = 0;
        for (int i = rows - 1; i >= 0; i--) {
            if (vec_index < vec.size())
                panel[i][j] = vec[vec_index++];
            else {
                panel[i][j] = 0;
            }
        }
    }
    add();
    show();
}

void Game::move_d() {
    for (int i = 0; i < rows; i++) {
        vector<int> vec;
        for (int j = cols - 1; j >= 0; j--) {
            merge(vec, i, j);
        }

        size_t vec_index = 0;
        for (int j = cols - 1; j >= 0; j--) {
            if (vec_index < vec.size())
                panel[i][j] = vec[vec_index++];
            else {
                panel[i][j] = 0;
            }
        }
    }
    add();
    show();
}

Point Game::get_empty_location() {
    vector<Point> vec;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (panel[i][j] == 0) {
                vec.push_back(Point(i, j));
            }
        }
    }

    if (vec.size() == 0) {
        throw runtime_error("no point available");
    }

    return vec[rand() % vec.size()];
}

void Game::merge(vector<int>& vec, int i, int j) {
    if (panel[i][j] == 0)
        return;
    int current = panel[i][j];
    while (vec.size() > 0 && vec[vec.size() - 1] == current) {
        current *= 2;
        score += current;
        vec.pop_back();
    }
    vec.push_back(current);
}

/*
* 判断是否还能移动
* 1. 有空位
* 2. 没有空位，但是相邻的有相同的
*/
bool Game::check_if_movable()
{
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (panel[i][j] == 0)
                return true;
        }
    }

    for (int i = 0; i < rows - 1; i++) {
        for (int j = 0; j < cols - 1; j++) {
            if (panel[i][j] == panel[i][j + 1] || panel[i][j] == panel[i + 1][j])
                return true;
        }
    }
    return false;
}

void Game::show() {
    system("cls");
    int length = get_num_length() + 1;

    // 输出第一行
    cout << tab[0];
    for (int i = 0; i < cols; i++) {
        for (int k = 0; k < length; k++) {
            cout << tab[1];
        }

        if (i == cols - 1)
            cout << tab[3];
        else
            cout << tab[2];
    }

    cout << endl;

    // 行和列各分为4组
    for (int i = 0; i < rows; i++) {

        // 输出数字
        cout << tab[4];
        for (int j = 0; j < cols; j++) {
            if (panel[i][j] == 0)
                cout << setw(length) << " ";
            else
                cout << setw(length) << panel[i][j];
            cout << tab[4];
        }
        cout << endl;

        if (i == rows - 1)
            cout << tab[7];
        else {
            cout << tab[5];
        }

        // 输出制表符
        for (int j = 0; j < cols; j++) {
            for (int k = 0; k < length; k++) {
                cout << tab[1];
            }

            if (i == rows - 1 && j == cols - 1)
                cout << tab[9];
            else if (i == rows - 1)
                cout << tab[8];
            else
                cout << tab[6];
        }

        cout << endl;
    }

    cout << "score: " << score << endl;
}

int main() {
    Game game;
    try {
        game.main();
    }
    catch (runtime_error& err) {
        cout << "game over!" << endl;
    }
}
