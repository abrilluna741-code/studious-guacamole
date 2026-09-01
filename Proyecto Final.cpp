#include "raylib.h"
#include <vector>
#include <stack>
#include <queue>
#include <algorithm>

const int SIZE = 20;
const int ROWS = 25;
const int COLS = 25;

struct Cell {
    int r, c;
    bool visited = false;
    bool walls[4] = {true, true, true, true}; // arriba, derecha, abajo, izquierda
};

std::vector<std::vector<Cell>> grid;
std::stack<Cell*> st;

// BFS
std::queue<Cell*> q;
std::vector<std::vector<bool>> visitedBFS;
std::vector<std::vector<Cell*>> parent;

bool generationComplete = false;
bool solving = false;
bool solvingComplete = false;

Cell* startCell;
Cell* endCell;

std::vector<Cell*> path;

Cell* getNeighbor(Cell& current) {
    std::vector<Cell*> neighbors;

    int r = current.r;
    int c = current.c;

    if (r > 0 && !grid[r-1][c].visited) neighbors.push_back(&grid[r-1][c]);
    if (c < COLS-1 && !grid[r][c+1].visited) neighbors.push_back(&grid[r][c+1]);
    if (r < ROWS-1 && !grid[r+1][c].visited) neighbors.push_back(&grid[r+1][c]);
    if (c > 0 && !grid[r][c-1].visited) neighbors.push_back(&grid[r][c-1]);

    if (!neighbors.empty()) {
        int i = GetRandomValue(0, neighbors.size() - 1);
        return neighbors[i];
    }
    return nullptr;
}

void removeWalls(Cell* a, Cell* b) {
    int dx = a->c - b->c;
    int dy = a->r - b->r;

    if (dx == 1) {
        a->walls[3] = false;
        b->walls[1] = false;
    }
    if (dx == -1) {
        a->walls[1] = false;
        b->walls[3] = false;
    }
    if (dy == 1) {
        a->walls[0] = false;
        b->walls[2] = false;
    }
    if (dy == -1) {
        a->walls[2] = false;
        b->walls[0] = false;
    }
}

void drawMaze() {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {

            int x = j * SIZE;
            int y = i * SIZE;

            if (grid[i][j].visited)
                DrawRectangle(x, y, SIZE, SIZE, DARKGREEN);

            Cell& cell = grid[i][j];

            if (cell.walls[0]) DrawLine(x, y, x + SIZE, y, WHITE);
            if (cell.walls[1]) DrawLine(x + SIZE, y, x + SIZE, y + SIZE, WHITE);
            if (cell.walls[2]) DrawLine(x + SIZE, y + SIZE, x, y + SIZE, WHITE);
            if (cell.walls[3]) DrawLine(x, y + SIZE, x, y, WHITE);
        }
    }
}

void drawPath() {
    for (auto c : path) {
        DrawRectangle(c->c * SIZE, c->r * SIZE, SIZE, SIZE, YELLOW);
    }
}

int main() {

    InitWindow(COLS * SIZE, ROWS * SIZE, "Laberinto Animado");
    SetTargetFPS(60);

    grid.resize(ROWS, std::vector<Cell>(COLS));

    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            grid[i][j] = {i, j};
        }
    }

    Cell* current = &grid[0][0];
    current->visited = true;
    st.push(current);

    startCell = &grid[0][0];
    endCell = &grid[ROWS-1][COLS-1];

    visitedBFS.resize(ROWS, std::vector<bool>(COLS, false));
    parent.resize(ROWS, std::vector<Cell*>(COLS, nullptr));

    while (!WindowShouldClose()) {

        BeginDrawing();
        ClearBackground(BLACK);

        drawMaze();

        // 🔁 GENERACIÓN ANIMADA
        if (!generationComplete) {
            if (!st.empty()) {
                Cell* current = st.top();
                Cell* next = getNeighbor(*current);

                if (next) {
                    next->visited = true;
                    st.push(next);
                    removeWalls(current, next);
                } else {
                    st.pop();
                }

                DrawRectangle(current->c * SIZE, current->r * SIZE, SIZE, SIZE, RED);
            } else {
                generationComplete = true;

                // Iniciar BFS
                q.push(startCell);
                visitedBFS[startCell->r][startCell->c] = true;
                solving = true;
            }
        }

        // 🔍 BFS ANIMADO
        else if (solving && !solvingComplete) {
            if (!q.empty()) {
                Cell* current = q.front();
                q.pop();

                if (current == endCell) {
                    solvingComplete = true;

                    // reconstruir camino
                    Cell* p = current;
                    while (p != nullptr) {
                        path.push_back(p);
                        p = parent[p->r][p->c];
                    }
                    std::reverse(path.begin(), path.end());
                }

                int r = current->r;
                int c = current->c;

                // vecinos
                auto tryVisit = [&](int nr, int nc) {
                    if (!visitedBFS[nr][nc]) {
                        visitedBFS[nr][nc] = true;
                        parent[nr][nc] = current;
                        q.push(&grid[nr][nc]);
                    }
                };

                if (!current->walls[0]) tryVisit(r-1, c);
                if (!current->walls[1]) tryVisit(r, c+1);
                if (!current->walls[2]) tryVisit(r+1, c);
                if (!current->walls[3]) tryVisit(r, c-1);

                DrawRectangle(c * SIZE, r * SIZE, SIZE, SIZE, BLUE);
            }
        }

        if (solvingComplete) {
            drawPath();
        }

        EndDrawing();
    }

    CloseWindow();
    return 0;
}