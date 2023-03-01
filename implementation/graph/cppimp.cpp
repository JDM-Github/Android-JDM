#include <iostream>
#include <vector>
using namespace std;

class Graph {
    int V;
    vector<vector<int>> adj;
public:
    Graph(int V) {
        this->V = V;
        adj.resize(V);
    }
    void add_edge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    void print_graph() {
        for (int i = 0; i < V; i++) {
            cout << "Vertex " << i << ": ";
            for (auto j : adj[i]) {
                cout << j << " ";
            }
            cout << endl;
        }
    }
};
