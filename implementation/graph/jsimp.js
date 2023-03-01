class Graph {
    constructor(vertices) {
        this.V = vertices;
        this.adj = new Array(vertices).fill().map(() => []);
    }
    add_edge(u, v) {
        this.adj[u].push(v);
        this.adj[v].push(u);
    }
    print_graph() {
        for (let i = 0; i < this.V; i++) {
            let str = `Vertex ${i}: `;
            for (let j of this.adj[i]) {
                str += `${j} `;
            }
            console.log(str);
        }
    }
}
