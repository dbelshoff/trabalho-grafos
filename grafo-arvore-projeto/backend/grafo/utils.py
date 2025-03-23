import networkx as nx
from collections import deque

class Grafo:
    def __init__(self, texto):
        self.grafo = self._parse_texto(texto)
        self.g = self.criar_grafo()

    def _parse_texto(self, texto):
        grafo = {}
        for linha in texto.strip().split("\n"):
            elementos = list(map(int, linha.split(",")))
            no_raiz = elementos[0]
            filhos = elementos[1:]
            if no_raiz not in grafo:
                grafo[no_raiz] = []
            grafo[no_raiz].extend(filhos)
        return grafo

    def criar_grafo(self):
        G = nx.DiGraph()
        for no, filhos in self.grafo.items():
            for filho in filhos:
                G.add_edge(no, filho)
        return G


    def eh_arvore(self):
        return nx.is_tree(nx.DiGraph(self.grafo))  # Garante que seja direcionado

    def eh_binaria(self):
        """ Verifica se a árvore é binária (cada nó pode ter no máximo dois filhos). """
        return all(len(filhos) <= 2 for filhos in self.grafo.values())

    def eh_completa(self):
        """ Verifica se a árvore é completa (todos os níveis exceto o último estão preenchidos e o último nível está preenchido da esquerda para a direita). """
        if not self.grafo:
            return False

        fila = [(next(iter(self.grafo)))]  # Começa pelo nó raiz
        encontrou_folha = False  # Define se encontramos um nó sem filhos antes de terminar

        while fila:
            no = fila.pop(0)

            if no in self.grafo:
                filhos = self.grafo[no]

                for filho in filhos:
                    if encontrou_folha:
                        return False  # Se já encontramos um nó sem filhos, nenhum outro pode ter filhos
                    fila.append(filho)

                if len(filhos) < 2:  
                    encontrou_folha = True  # Se encontramos um nó com menos de dois filhos, ele deve ser o último nível

        return True


    def eh_cheia(self):
        """ Verifica se a árvore é cheia (todos os nós têm 0 ou 2 filhos). """
        for no, filhos in self.grafo.items():
            if len(filhos) not in [0, 2]:  
                return False  # Se algum nó tem apenas 1 filho, não é cheia
        return True



    def eh_bst(self):
        """ Verifica se a árvore binária é uma BST. """
        def bst_valido(no, min_val=float('-inf'), max_val=float('inf')):
            if no not in self.grafo:
                return True
            filhos = self.grafo[no]
            if len(filhos) > 0 and filhos[0] <= min_val:  # Filho esquerdo deve ser maior que min_val
                return False
            if len(filhos) > 1 and filhos[1] >= max_val:  # Filho direito deve ser menor que max_val
                return False
            return bst_valido(filhos[0], min_val, no) and (len(filhos) < 2 or bst_valido(filhos[1], no, max_val))

        raiz = next(iter(self.grafo))
        return bst_valido(raiz)

    def eh_avl(self):
        """ Verifica se a árvore binária é balanceada (AVL). """
        def altura(no):
            if no not in self.grafo:
                return 0
            return 1 + max((altura(filho) for filho in self.grafo[no]), default=0)

        def balanceada(no):
            if no not in self.grafo:
                return True
            filhos = self.grafo[no]
            alt_esq = altura(filhos[0]) if len(filhos) > 0 else 0
            alt_dir = altura(filhos[1]) if len(filhos) > 1 else 0
            return abs(alt_esq - alt_dir) <= 1 and all(balanceada(filho) for filho in filhos)

        raiz = next(iter(self.grafo))
        return balanceada(raiz)

    def tipo_arvore(self):
        if not self.eh_arvore():
            return "Não é uma árvore"

        if not self.eh_binaria():
            return "Árvore não binária"

        if self.eh_bst():
            if self.eh_avl():
                return "Árvore AVL (BST balanceada)"
            return "Árvore binária de busca (BST)"

        if self.eh_cheia() and self.eh_completa():
            return "Árvore binária cheia e completa"
        if self.eh_cheia():
            return "Árvore binária cheia"
        if self.eh_completa():
            return "Árvore binária completa"

        return "Árvore binária"

    
    def altura(self):
        # Verifica se o grafo é uma árvore antes de calcular a altura
        if not self.eh_arvore():
            return "Não é uma árvore"
        
        # Usando networkx para calcular a altura de uma árvore
        # A altura de uma árvore é a distância máxima de um nó raiz até o nó mais distante.
        try:
            # Encontrando a árvore mais longa a partir da raiz
            raiz = next(iter(self.grafo))  # Pega o primeiro nó
            distancias = nx.single_source_shortest_path_length(self.g, raiz)
            altura = max(distancias.values())  # A maior distância do nó raiz
            return altura
        except Exception as e:
            return {"error": f"Erro ao calcular a altura: {str(e)}"}
        
        
    def pre_ordem(self, no):
        # Percurso pré-ordem
        if no is None:
            return []
        vizinhos = list(self.g.neighbors(no))  # Converte o iterador em lista
        esquerda, direita = vizinhos if len(vizinhos) == 2 else (None, None)  # Verifica se temos dois filhos
        return [no] + self.pre_ordem(esquerda) + self.pre_ordem(direita)

    def em_ordem(self, no):
        # Percurso em-ordem
        if no is None:
            return []
        vizinhos = list(self.g.neighbors(no))  # Converte o iterador em lista
        esquerda, direita = vizinhos if len(vizinhos) == 2 else (None, None)  # Verifica se temos dois filhos
        return self.em_ordem(esquerda) + [no] + self.em_ordem(direita)

    def pos_ordem(self, no):
        # Percurso pós-ordem
        if no is None:
            return []
        vizinhos = list(self.g.neighbors(no))  # Converte o iterador em lista
        esquerda, direita = vizinhos if len(vizinhos) == 2 else (None, None)  # Verifica se temos dois filhos
        return self.pos_ordem(esquerda) + self.pos_ordem(direita) + [no]

    def caminhos(self):
        caminhos = {
            "pre_ordem": set(),
            "em_ordem": set(),
            "pos_ordem": set()
        }
        
        if not self.eh_arvore():
            return {"error": "Não é uma árvore"}
        
        try:
            # Calcular os caminhos de pré-ordem, em ordem e pós-ordem para todos os nós
            for no_origem in self.g:
                # Calculando os caminhos entre a origem e o destino
                pre_ordem = self.pre_ordem(no_origem)
                em_ordem = self.em_ordem(no_origem)
                pos_ordem = self.pos_ordem(no_origem)
                
                # Adicionando ao conjunto de caminhos (garante unicidade)
                caminhos["pre_ordem"].add(tuple(pre_ordem))
                caminhos["em_ordem"].add(tuple(em_ordem))
                caminhos["pos_ordem"].add(tuple(pos_ordem))
            
            # Convertendo os conjuntos de volta para listas
            caminhos["pre_ordem"] = list(caminhos["pre_ordem"])
            caminhos["em_ordem"] = list(caminhos["em_ordem"])
            caminhos["pos_ordem"] = list(caminhos["pos_ordem"])

        except nx.NodeNotFound as e:
            return {"error": f"Erro ao processar o grafo: {str(e)}"}
        
        return caminhos