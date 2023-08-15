# encoding:utf-8

'''
	Ant Colony Optimization for Traveling Salesman Problem
'''

import random, math
import time
from timeit import default_timer as timer

# classe que representa uma aresta
class Edge:

	def __init__(self, src, dest, cost):
		self.src = src
		self.dest = dest
		self.cost = cost
		self.pheromone = None

	def getSrc(self):
		return self.src

	def getDest(self):
		return self.dest

	def getCost(self):
		return self.cost

	def getPheromone(self):
		return self.pheromone

	def setPheromone(self, pheromone):
		self.pheromone = pheromone

# classe que representa um grafo (grafos completos)
class Graph:

	def __init__(self, num_vertices):
		self.num_vertices = num_vertices # número de vértices do grafo
		self.edges = {} # dicionário com as arestas
		self.neighbors = {} # dicionário com todos os neighbors de cada vértice


	def addEdge(self, src, dest, cost):
		edge = Edge(src=src, dest=dest, cost=cost)
		self.edges[(src, dest)] = edge
		if src not in self.neighbors:
			self.neighbors[src] = [dest]
		else:
			self.neighbors[src].append(dest)

	def getEdgeCost(self, src, dest):
		return self.edges[(src, dest)].getCost()

	def getEdgePheromone(self, src, dest):
		return self.edges[(src, dest)].getPheromone()

	def setEdgePheromone(self, src, dest, pheromone):
		self.edges[(src, dest)].setPheromone(pheromone)

	def getPathCost(self, path):
		cost = 0
		for i in range(self.num_vertices-1):
			cost += self.getEdgeCost(path[i], path[i+1])
		# adiciona o último custo
		cost += self.getEdgeCost(path[-1], path[0])
		return cost


class GraphComplete(Graph):
	# gera um grafo completo
	def generate(self):
		for i in range(self.num_vertices):
			for j in range(self.num_vertices):
				if i != j:
					peso = random.randint(0, 9)
					self.addEdge(i, j, peso)


# classe que representa uma formiga
class Ant:

	def __init__(self, city):
		self.city = city
		self.solution = []
		self.cost = None

	def getCity(self):
		return self.city

	def setCity(self, city):
		self.city = city

	def getSolution(self):
		return self.solution

	def setSolution(self, solution, cost):
		# atualiza a solução
		if not self.cost:
			self.solution = solution[:]
			self.cost = cost
		else:
			if cost < self.cost:
				self.solution = solution[:]
				self.cost = cost

	def getSolutionCost(self):
		return self.cost


# classe do ACO
class ACO:
	def __init__(self, graph, num_ants, alpha, beta, 
						iterations, evaporation):
		self.graph = graph
		self.num_ants = num_ants
		self.alpha = alpha # importância do feromônio
		self.beta = beta # importância da informação heurística
		self.iterations = iterations # quantidade de iterações
		self.evaporation = evaporation # taxa de evaporação
		self.ants = [] # lista de formigas

		list_cities = [city for city in range(self.graph.num_vertices)]
		# cria as formigas colocando cada uma em uma cidade
		for k in range(self.num_ants):
			city_ant = random.choice(list_cities)
			list_cities.remove(city_ant)
			self.ants.append(Ant(city=city_ant))
			if not list_cities:
				list_cities = [city for city in range(self.graph.num_vertices)]


		# calcula o custo guloso pra usar na inicialização do feromônio
		greedy_cost = 0.0 # custo guloso
		initial_vertex = random.randint(0, graph.num_vertices-1) # seleciona um vértice aleatório
		flow_vertex = initial_vertex
		visited = [flow_vertex] # lista de visited
		while True:
			neighbors = self.graph.neighbors[flow_vertex][:]
			costs, selected = [], {}
			for neighbor in neighbors:
				if neighbor not in visited:
					cost = self.graph.getEdgeCost(flow_vertex, neighbor)
					selected[cost] = neighbor
					costs.append(cost)
			if len(visited) == self.graph.num_vertices:
				break
			min_cost = min(costs) # pega o menor custo da lista
			greedy_cost += min_cost # adiciona o custo ao total
			flow_vertex = selected[min_cost] # atualiza o vértice corrente
			visited.append(flow_vertex) # marca o vértice corrente como visitado

		# adiciona o custo do último visitado ao greedy_cost
		greedy_cost += self.graph.getEdgeCost(visited[-1], initial_vertex)

		# inicializa o feromônio de todas as arestas
		for edge_key in self.graph.edges:
			pheromone = 1.0 / (self.graph.num_vertices * greedy_cost)
			self.graph.setEdgePheromone(edge_key[0], edge_key[1], pheromone)


	def run(self):
		for it in range(self.iterations):

			# lista de listas com as cidades visitadas por cada formiga
			cities_visited = []
			for k in range(self.num_ants):
				# adiciona a cidade de origem de cada formiga
				city = [self.ants[k].getCity()]
				cities_visited.append(city)

			# para cada formiga constrói uma solução
			for k in range(self.num_ants):
				for i in range(self.graph.num_vertices-1):
					# obtém todos os neighbors que não foram visited
					cities_unvisited = list(set(self.graph.neighbors[self.ants[k].getCity()]) - set(cities_visited[k]))
					
					# somatório do conjunto de cidades não visitadas pela formiga "k"
					# servirá para utilizar no cálculo da probability
					sum = 0.0
					for city in cities_unvisited:
						# calcula o feromônio
						pheromone =  self.graph.getEdgePheromone(self.ants[k].getCity(), city)
						# obtém a distância
						distance = self.graph.getEdgeCost(self.ants[k].getCity(), city)
						# adiciona no somatório
						sum += (math.pow(pheromone, self.alpha) * math.pow(1.0 / distance, self.beta))

					# probabilities de escolher um path
					probabilities = {}

					for city in cities_unvisited:
						# calcula o feromônio
						pheromone = self.graph.getEdgePheromone(self.ants[k].getCity(), city)
						# obtém a distância
						distance = self.graph.getEdgeCost(self.ants[k].getCity(), city)
						# obtém a probability
						probability = (math.pow(pheromone, self.alpha) * math.pow(1.0 / distance, self.beta)) / (sum if sum > 0 else 1)
						# adiciona na lista de probabilities
						probabilities[city] = probability

					# obtém a cidade escolhida
					selected_city = max(probabilities, key=probabilities.get)

					# adiciona a cidade escolhida a lista de cidades visitadas pela formiga "k"
					cities_visited[k].append(selected_city)

				# atualiza a solução encontrada pela formiga
				self.ants[k].setSolution(cities_visited[k], self.graph.getPathCost(cities_visited[k]))

			# atualiza quantidade de feromônio
			for edge in self.graph.edges:
				# somatório dos feromônios da aresta
				sum_pheromone = 0.0
				# para cada formiga "k"
				for k in range(self.num_ants):
					ant_edges = []
					# gera todas as arestas percorridas da formiga "k"
					for j in range(self.graph.num_vertices - 2):
						ant_edges.append((cities_visited[k][j], cities_visited[k][j+1]))
					# adiciona a última aresta
					ant_edges.append((cities_visited[k][-1], cities_visited[k][0]))
					# verifica se a aresta faz parte do path da formiga "k"
					if edge in ant_edges:
						sum_pheromone += (1.0 / self.graph.getPathCost(cities_visited[k]))
				# calcula o novo feromônio
				new_pheromone = (1.0 - self.evaporation) * self.graph.getEdgePheromone(edge[0], edge[1]) + sum_pheromone
				# seta o novo feromônio da aresta
				self.graph.setEdgePheromone(edge[0], edge[1], new_pheromone)

		# percorre para obter as soluções das formigas
		solution, cost = None, None
		for k in range(self.num_ants):
			if not solution:
				solution = self.ants[k].getSolution()[:]
				cost = self.ants[k].getSolutionCost()
			else:
				aux_cost = self.ants[k].getSolutionCost()
				if aux_cost < cost:
					solution = self.ants[k].getSolution()[:]
					cost = aux_cost
		print('Final Solution: %s | cost: %d\n' % (' -> '.join(str(i) for i in solution), cost))
		return [solution, cost]


class ExecuteACO:
	def runACO(edges):
		# start_time = time.time()
		start = timer()
		# cria um graph passando o número de vértices

		max_value = float('-inf')  # Initialize with negative infinity

		for edge in edges:
			if edge[0] > max_value:
				max_value = edge[0]
			elif edge[1] > max_value:
				max_value = edge[1]

		graph = Graph(num_vertices=max_value+1)

		# mapeando cidades para números
		# d = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
		# adiciona as edge


		for i in range(len(edges)):
			# print("EDGES", edges[i][0])
			graph.addEdge(edges[i][0], edges[i][1], edges[i][2])

		# cria uma instância de ACO
		aco = ACO(graph=graph, num_ants=10, alpha=1, beta=1, iterations=100, evaporation=0.95)
		# roda o algoritmo
		acoRun = aco.run()
		end = timer()
		acoTime = end - start 
		# acoTime = time.time() - start_time
		print("--- %s seconds ---" % acoTime)
		routeArrangement = ExecuteACO.create_cycle_queue(acoRun[0])
		print("ACO: ", [routeArrangement, acoRun[1]])

		return [routeArrangement, acoRun[1]], acoTime

		# teste com graph completo
		'''
		num_vertices = 20
		print('Teste de grafo com %d vertices...\n' % num_vertices)
		grafo_completo = GrafoCompleto(num_vertices=num_vertices)
		grafo_completo.generate()
		aco2 = ACO(grafo=grafo_completo, num_ants=grafo_completo.num_vertices, 
					alpha=1, beta=5, iterations=100, evaporation=0.5)
		aco2.run()
		'''
	def create_cycle_queue(cycle):
			queue = cycle[:]
			while queue[0] != 0:
				queue.append(queue.pop(0))
			return queue

# edges = [[0, 1, 89.26666666666667], [0, 2, 33.083333333333336], [0, 3, 65.21666666666667], [1, 0, 58.9], [1, 2, 63.5], [1, 3, 79.85], [2, 0, 24.433333333333334], [2, 1, 84.16666666666667], [2, 3, 75.76666666666667], [3, 0, 62.31666666666667], [3, 1, 90.43333333333334], [3, 2, 62.68333333333333]]

# x = ExecuteACO.runACO(edges)
# print(x)