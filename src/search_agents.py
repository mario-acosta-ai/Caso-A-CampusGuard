# src/search_agents.py
from collections import deque
import heapq
from problem_model import CampusGuardProblem, State

class Node:
    """Nodo del árbol de búsqueda estilo AIMA."""
    def __init__(self, state: State, parent: Optional['Node'] = None, action: Optional[str] = None, path_cost: int = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other: 'Node') -> bool:
        return self.path_cost < other.path_cost

    def path(self) -> List[str]:
        """Reconstruye el camino de acciones desde el nodo raíz."""
        node, path_actions = self, []
        while node.parent:
            path_actions.append(node.action)
            node = node.parent
        return list(reversed(path_actions))

def breadth_first_graph_search(problem: CampusGuardProblem) -> Optional[Node]:
    """Búsqueda en Anchura (BFS). Complejidad temporal/espacial: O(b^d)."""
    node = Node(problem.initial)
    if problem.goal_test(node.state): return node
    frontier = deque([node])
    explored = set()
    
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            if child_state not in explored:
                child = Node(child_state, node, action, problem.path_cost(node.path_cost, node.state, action, child_state))
                if problem.goal_test(child.state): return child
                frontier.append(child)
    return None

def depth_first_graph_search(problem: CampusGuardProblem) -> Optional[Node]:
    """Búsqueda en Profundidad (DFS). Complejidad temporal: O(b^m), espacial: O(b*m)."""
    node = Node(problem.initial)
    if problem.goal_test(node.state): return node
    frontier = [node]
    explored = set()
    
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            if child_state not in explored:
                child = Node(child_state, node, action, problem.path_cost(node.path_cost, node.state, action, child_state))
                if problem.goal_test(child.state): return child
                frontier.append(child)
    return None

def astar_search(problem: CampusGuardProblem) -> Optional[Node]:
    """Búsqueda A* con heurística admisible. Complejidad temporal/espacial: O(b^(d-k_h))."""
    node = Node(problem.initial)
    frontier = [(node.path_cost + problem.h(node), node)]
    explored = set()
    
    while frontier:
        _, node = heapq.heappop(frontier)
        if problem.goal_test(node.state): return node
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            if child_state not in explored:
                child = Node(child_state, node, action, problem.path_cost(node.path_cost, node.state, action, child_state))
                f_cost = child.path_cost + problem.h(child)
                heapq.heappush(frontier, (f_cost, child))
    return None
