#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

struct Cancion {
    string titulo;
    string artista;
    int duracionSegundos; // opcional
    Cancion* siguiente;
    Cancion* anterior;
    Cancion(const string& t, const string& a, int d)
        : titulo(t), artista(a), duracionSegundos(d), siguiente(nullptr), anterior(nullptr) {}
};

static string formatoTiempo(int s) {
    if (s < 0) return "--:--";
    int m = s / 60; s %= 60;
    ostringstream os; os << setw(2) << setfill('0') << m << ":" << setw(2) << setfill('0') << s; return os.str();
}

class Playlist {
private:
    Cancion* head;
    Cancion* tail;
    Cancion* actual; // puntero del reproductor

public:
    Playlist() : head(nullptr), tail(nullptr), actual(nullptr) {}

    ~Playlist() {
        // liberar memoria
        Cancion* p = head;
        while (p) {
            Cancion* nxt = p->siguiente;
            delete p;
            p = nxt;
        }
        head = tail = actual = nullptr;
    }

    bool vacia() const { return head == nullptr; }

    void agregarAlFinal(const string& titulo, const string& artista, int duracionSeg) {
        Cancion* nueva = new Cancion(titulo, artista, duracionSeg);
        if (!head) {
            head = tail = actual = nueva;
        } else {
            tail->siguiente = nueva;
            nueva->anterior = tail;
            tail = nueva;
        }
        cout << "Agregada: '" << titulo << "' - " << artista << " (" << formatoTiempo(duracionSeg) << ")\n";
    }

    void mostrarCompleta() const {
        cout << "\n=== Playlist Completa ===\n";
        if (!head) { cout << "(vacía)\n"; return; }
        int idx = 1;
        for (Cancion* p = head; p; p = p->siguiente, ++idx) {
            bool esActual = (p == actual);
            cout << (esActual ? "▶ " : "  ")
                 << idx << ". '" << p->titulo << "' — " << p->artista
                 << "  [" << formatoTiempo(p->duracionSegundos) << "]";
            if (p == head) cout << "  (Head)";
            if (p == tail) cout << "  (Tail)";
            cout << "\n";
        }
    }

    void reproducirActual() const {
        cout << "\n=== Reproduciendo Actual ===\n";
        if (!actual) { cout << "No hay canciones.\n"; return; }
        cout << "'" << actual->titulo << "' — " << actual->artista
             << "  [" << formatoTiempo(actual->duracionSegundos) << "]\n";
    }

    void siguiente() {
        if (!actual) { cout << "Playlist vacía.\n"; return; }
        if (!actual->siguiente) { cout << "Fin de la playlist.\n"; return; }
        actual = actual->siguiente;
        reproducirActual();
    }

    void anterior() {
        if (!actual) { cout << "Playlist vacía.\n"; return; }
        if (!actual->anterior) { cout << "Inicio de la playlist.\n"; return; }
        actual = actual->anterior;
        reproducirActual();
    }

    void eliminarActual() {
        if (!actual) { cout << "No hay canción para eliminar.\n"; return; }
        Cancion* a = actual;
        cout << "Eliminando: '" << a->titulo << "' — " << a->artista << "\n";

        Cancion* prev = a->anterior;
        Cancion* next = a->siguiente;

        // reconectar vecinos
        if (prev) prev->siguiente = next; else head = next;
        if (next) next->anterior = prev; else tail = prev;

        // decidir nueva actual
        if (next) actual = next;
        else if (prev) actual = prev;
        else actual = nullptr;

        delete a;
        if (!actual) cout << "La playlist quedó vacía.\n";
        else {
            cout << "Ahora suena: '" << actual->titulo << "' — " << actual->artista << "\n";
        }
    }

    void ordenarPorArtista() {
        if (!head || !head->siguiente) { cout << "Nada que ordenar.\n"; return; }
        bool huboCambio;
        do {
            huboCambio = false;
            for (Cancion* p = head; p && p->siguiente; p = p->siguiente) {
                if (p->artista > p->siguiente->artista) {
                    // Intercambiar datos (más simple que re-enlazar nodos)
                    swap(p->titulo, p->siguiente->titulo);
                    swap(p->artista, p->siguiente->artista);
                    swap(p->duracionSegundos, p->siguiente->duracionSegundos);
                    huboCambio = true;
                }
            }
        } while (huboCambio);
        cout << "Playlist ordenada por artista.\n";
    }
};

static int leerEnteroSeguro(const string& prompt, int defecto = -1) {
    while (true) {
        cout << prompt;
        string s; if (!getline(cin, s)) return defecto;
        try {
            if (s.empty()) return defecto;
            size_t pos = 0; int v = stoi(s, &pos); if (pos == s.size()) return v;
        } catch (...) {}
        cout << "Entrada no válida, intenta de nuevo.\n";
    }
}

static void menu() {
    cout << "\n============================\n";
    cout << "  Reproductor de Playlist\n";
    cout << "============================\n";
    cout << "1) Agregar canción (al final)\n";
    cout << "2) Mostrar playlist completa\n";
    cout << "3) Reproducir actual\n";
    cout << "4) Siguiente (Next)\n";
    cout << "5) Anterior (Prev)\n";
    cout << "6) Eliminar canción actual\n";
    cout << "7) Ordenar por artista (opcional)\n";
    cout << "0) Salir\n";
    cout << "Seleccion: ";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    Playlist pl;

    while (true) {
        menu();
        string linea; if (!getline(cin, linea)) break;
        if (linea.empty()) continue;
        int op = -1; try { op = stoi(linea); } catch (...) { op = -1; }
        if (op == 0) break;

        switch (op) {
            case 1: {
                cout << "Título: ";
                string titulo; getline(cin, titulo);
                cout << "Artista: ";
                string artista; getline(cin, artista);
                int dur = leerEnteroSeguro("Duración (segundos, opcional deja vacío): ", -1);
                pl.agregarAlFinal(titulo, artista, dur);
                break;
            }
            case 2: pl.mostrarCompleta(); break;
            case 3: pl.reproducirActual(); break;
            case 4: pl.siguiente(); break;
            case 5: pl.anterior(); break;
            case 6: pl.eliminarActual(); break;
            case 7: pl.ordenarPorArtista(); break;
            default: cout << "Opción inválida.\n"; break;
        }
    }

    cout << "Adiós!\n";
    return 0;
}
