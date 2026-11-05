# src/search.py
import heapq
from collections import deque

def bfs(problem):
    node = (problem.initial_state, [], 0) # (estado, camino, costo)
    if problem.goal_test(node[0]): return node
    frontier = deque([node])
    explored = set()
    while frontier:
        state, path, cost = frontier.popleft()
        explored.add(state)
        for action in problem.actions(state):
            child_state = problem.result(state, action)
            if child_state not in explored:
                child_node = (child_state, path + [action], cost + problem.step_cost(state, action))
                if problem.goal_test(child_state): return child_node
                frontier.append(child_node)
    return None

def dfs(problem):
    node = (problem.initial_state, [], 0)
    if problem.goal_test(node[0]): return node
    frontier = [node]
    explored = set()
    while frontier:
        state, path, cost = frontier.pop()
        explored.add(state)
        for action in problem.actions(state):
            child_state = problem.result(state, action)
            if child_state not in explored:
                child_node = (child_state, path + [action], cost + problem.step_cost(state, action))
                if problem.goal_test(child_state): return child_node
                frontier.append(child_node)
    return None

def a_star(problem):
    # Heurística admisible: costo mínimo estimado para resolver el estado actual
    def h(state):
        nivel, causa, _ = state
        if nivel == "Bajo": return 0
        if causa == "Academico": return 1 # Mínimo costo (Tutoría)
        if causa == "Socioemocional": return 3 # Mínimo costo (Bienestar)
        if causa == "Carga": return 1 # Mínimo costo (Tutoría)
        return 1

    node = (problem.initial_state, [], 0)
    frontier = [(0 + h(problem.initial_state), node)]
    explored = set()
    
    while frontier:
        f_cost, (state, path, cost) = heapq.heappop(frontier)
        if problem.goal_test(state): return (state, path, cost)
        explored.add(state)
        
        for action in problem.actions(state):
            child_state = problem.result(state, action)
            if child_state not in explored:
                child_cost = cost + problem.step_cost(state, action)
                child_node = (child_state, path + [action], child_cost)
                f_child = child_cost + h(child_state)
                heapq.heappush(frontier, (f_child, child_node))
    return None
