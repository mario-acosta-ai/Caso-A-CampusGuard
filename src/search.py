# src/search.py
from collections import deque
import heapq
from problem import CampusGuardProblem, State

class Node:
    def __init__(self, state: State, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = cost
        
    def path(self) -> list:
        n, p = self, []
        while n.parent: 
            p.append(n.action)
            n = n.parent
        return p[::-1]
        
    def __lt__(self, other):
        return self.path_cost < other.path_cost

def bfs(problem: CampusGuardProblem) -> Node:
    node = Node(problem.initial)
    if problem.goal_test(node.state): 
        return node
        
    frontier, explored = deque([node]), set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child_s = problem.result(node.state, action)
            if child_s not in explored:
                child = Node(child_s, node, action, problem.path_cost(node.path_cost, node.state, action, child_s))
                if problem.goal_test(child.state): 
                    return child
                frontier.append(child)
    return None

def dfs(problem: CampusGuardProblem) -> Node:
    node = Node(problem.initial)
    if problem.goal_test(node.state): 
        return node
        
    frontier, explored = [node], set()
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child_s = problem.result(node.state, action)
            if child_s not in explored:
                child = Node(child_s, node, action, problem.path_cost(node.path_cost, node.state, action, child_s))
                if problem.goal_test(child.state): 
                    return child
                frontier.append(child)
    return None

def a_star(problem: CampusGuardProblem) -> Node:
    node = Node(problem.initial)
    frontier = [(node.path_cost + problem.h(node.state), node)]
    explored = set()
    while frontier:
        _, node = heapq.heappop(frontier)
        if problem.goal_test(node.state): 
            return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child_s = problem.result(node.state, action)
            if child_s not in explored:
                child = Node(child_s, node, action, problem.path_cost(node.path_cost, node.state, action, child_s))
                heapq.heappush(frontier, (child.path_cost + problem.h(child.state), child))
    return None
