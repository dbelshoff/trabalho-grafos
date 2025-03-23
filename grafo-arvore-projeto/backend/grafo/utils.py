class No:
    def __init__(self, valor):
        self.valor = valor
        self.filhos = []

class Grafo:
    def __init__(self, texto):
        self.grafo = self._parse_texto(texto)
        self.raiz = self._encontrar_raiz()

    def _parse_texto(self, texto):
        grafo = {}
        for linha in texto.strip().split("\n"):
            elementos = list(map(int, linha.split(",")))
            no_raiz = elementos[0]
            filhos = elementos[1:]
            if no_raiz not in grafo:
                grafo[no_raiz] = No(no_raiz)
            for filho in filhos:
                if filho not in grafo:
                    grafo[filho] = No(filho)
                grafo[no_raiz].filhos.append(grafo[filho])
        return grafo

    def _encontrar_raiz(self):
        possiveis_raizes = set(self.grafo.keys())
        for no in self.grafo.values():
            for filho in no.filhos:
                if filho.valor in possiveis_raizes:
                    possiveis_raizes.remove(filho.valor)
        return self.grafo[possiveis_raizes.pop()] if len(possiveis_raizes) == 1 else None

    def eh_arvore(self):
        if not self.raiz:
            return False

        visitados = set()
        def dfs(no):
            if no.valor in visitados:
                return False  # Encontrou ciclo
            visitados.add(no.valor)
            for filho in no.filhos:
                if not dfs(filho):
                    return False
            return True

        return dfs(self.raiz) and len(visitados) == len(self.grafo)

    def eh_binaria(self):
        return all(len(no.filhos) <= 2 for no in self.grafo.values())
        
    

    def eh_completa(self):
        if not self.eh_binaria():
            return False
        fila = [self.raiz]
        encontrou_folha = False

        while fila:
            no = fila.pop(0)
            if len(no.filhos) < 2:
                encontrou_folha = True
            elif encontrou_folha:
                return False
            fila.extend(no.filhos)
        
        return True

    def eh_cheia(self):
        return all(len(no.filhos) in [0, 2] for no in self.grafo.values())

    def altura(self, no=None):
        if not no:
            no = self.raiz
        if not no.filhos:
            return 0
        return 1 + max(self.altura(filho) for filho in no.filhos)

    def pre_ordem(self, no=None):
        if not no:
            no = self.raiz
        resultado = [no.valor]
        for filho in no.filhos:
            resultado.extend(self.pre_ordem(filho))
        return resultado

    def em_ordem(self, no=None):
        if not no:
            no = self.raiz
        resultado = []
        if len(no.filhos) >= 1:
            # Percorrer o primeiro filho
            resultado.extend(self.em_ordem(no.filhos[0]))
        
        # Adicionar o valor do nó atual
        resultado.append(no.valor)
        
        if len(no.filhos) == 2:
            # Percorrer o segundo filho
            resultado.extend(self.em_ordem(no.filhos[1]))
        
        return resultado

    def pos_ordem(self, no=None):
        if not no:
            no = self.raiz
        resultado = []
        for filho in no.filhos:
            resultado.extend(self.pos_ordem(filho))
        resultado.append(no.valor)
        return resultado

    def caminhos(self):
        if not self.eh_arvore():
            return {"error": "Não é uma árvore"}
        
        if not self.eh_binaria():
            return {"error": "Árvore não é binária e nao possui caminhos"}
    
        # Obtendo os caminhos
        pre_ordem_result = self.pre_ordem()
        em_ordem_result = self.em_ordem()
        pos_ordem_result = self.pos_ordem()

        # Retorna os resultados como listas, não como strings
        return {
            "pre_ordem": pre_ordem_result,
            "em_ordem": em_ordem_result,
            "pos_ordem": pos_ordem_result
        }
        
    def tipo_arvore(self):
        if not self.eh_arvore():
            return "Não é uma árvore"
        if not self.eh_binaria():
            return "Árvore não binária"
        """if self.eh_cheia() and self.eh_completa():
            return "Árvore binária cheia e completa"""
        if self.eh_cheia():
            return "Árvore binária cheia"
        if self.eh_completa():
            return "Árvore binária completa"
        return "Árvore binária"
