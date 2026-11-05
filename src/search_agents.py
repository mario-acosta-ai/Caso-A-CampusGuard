# src/search_agents.py
from collections import deque
import heapq

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def breadth_first_graph_search(problem):
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

def depth_first_graph_search(problem):
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

def astar_search(problem):
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
