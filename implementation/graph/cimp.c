#include <stdio.h>
#include <stdlib.h>

#define MAX_VERTICES 100

typedef struct Node {
    int dest;
    struct Node* next;
} Node;

typedef struct Graph {
    Node* adj[MAX_VERTICES];
    int V;
} Graph;

Node* create_node(int dest) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->dest = dest;
    new_node->next = NULL;
    return new_node;
}

Graph* create_graph(int V) {
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    graph->V = V;
    for (int i = 0; i < V; i++) {
        graph->adj[i] = NULL;
    }
    return graph;
}

void add_edge(Graph* graph, int src, int dest) {
    Node* new_node = create_node(dest);
    new_node->next = graph->adj[src];
    graph->adj[src] = new_node;
    new_node = create_node(src);
    new_node->next = graph->adj[dest];
    graph->adj[dest] = new_node;
}

void print_graph(Graph* graph) {
    for (int i = 0; i < graph->V; i++) {
        printf("Vertex %d: ", i);
        Node* ptr = graph->adj[i];
        while (ptr != NULL) {
            printf("%d ", ptr->dest);
            ptr = ptr->next;
        }
        printf("\n");
    }
}
