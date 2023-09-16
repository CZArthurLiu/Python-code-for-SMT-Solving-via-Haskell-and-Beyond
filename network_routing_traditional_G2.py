import time
from collections import defaultdict
from collections import deque
class WeightedGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.edge = list()

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
        self.edge.append([u,v,weight])

    def print_adj_list(self):
        for vertex in self.graph:
            print(f"Adjacency list of vertex {vertex}: {self.graph[vertex]}")

def hard_constraint_check(state,max_load):
    for vertex in state.graph:
        cur_sum = 0
        for edge in state.graph[vertex]:
            cur_sum += edge[1]
        if cur_sum > max_load[vertex]:
            return False
    total = 0
    for edge in state.edge:
        total += edge[2]
    return total
def soft_constraint_check(state):
    ratio = 0;
    for node in state:
        ratio = max(ratio,node[1]/node[2])
    return ratio
if __name__ == '__main__':
    # create graph
    wg = WeightedGraph()
    with open("graph.txt", "r") as file:
        for line in file:
            # Split each line into two nodes
            pair = line.strip().split()
            if len(pair) == 2:
                node1, node2 = map(int, pair)
                wg.add_edge(node1, node2, 0)
            elif len(pair) > 1:
                max_load = list(map(int, pair))
            else:
                total_load = int(pair[0])
    queen = deque()
    flag = False
    start_time = time.time()
    # state init
    for i in range(len(wg.edge)):
        temp = WeightedGraph()
        for j in range(len(wg.edge)):
            cur_edge = wg.edge[j]
            if i == j:
                # to accelerate search process, set step to 10
                temp.add_edge(cur_edge[0],cur_edge[1],cur_edge[2]+10)
            else:
                temp.add_edge(cur_edge[0],cur_edge[1],cur_edge[2])
        queen.append(temp)
    cnt = 0
    # find solution
    while len(queen) > 0:
        cur_state = queen.popleft()
        cnt += 1
        hard_constraint = hard_constraint_check(cur_state,max_load)
        if not hard_constraint:
            continue
        if hard_constraint == total_load:
            flag = True
            cur_state.print_adj_list()
            break
        for i in range(len(cur_state.edge)):
            temp = WeightedGraph()
            for j in range(len(cur_state.edge)):
                cur_edge = cur_state.edge[j]
                # to accelerate search process, set step to 10
                if i == j:
                    temp.add_edge(cur_edge[0], cur_edge[1], cur_edge[2] + 10)
                else:
                    temp.add_edge(cur_edge[0], cur_edge[1], cur_edge[2])
            queen.append(temp)
    end_time = time.time()
    if not flag:
        print("find no solution")
    else:
        print(f"traditional G2 method find solution via {cnt} search process")
    print(f"the running time for traditional G2 method: {end_time - start_time} ")







