
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

    #def eh_arvore(self):
    #    if not self.raiz:
    #        return False

    #    visitados = set()
    #    def dfs(no):
    #        if no.valor in visitados:
    #            return False  # Encontrou ciclo
    #        visitados.add(no.valor)
    #        for filho in no.filhos:
    #            if not dfs(filho):
    #                return False
    #        return True

    #    return dfs(self.raiz) and len(visitados) == len(self.grafo)

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
    
    def eh_bst(self, no=None, min_val=float('-inf'), max_val=float('inf')):
        if not no:
            no = self.raiz
        if not self.eh_binaria():
            return False  # Só faz sentido verificar BST em árvores binárias
        if not (min_val < no.valor < max_val):
            return False
        left_check = self.eh_bst(no.filhos[0], min_val, no.valor) if len(no.filhos) > 0 else True
        right_check = self.eh_bst(no.filhos[1], no.valor, max_val) if len(no.filhos) > 1 else True
        return left_check and right_check

    def eh_avl(self, no=None):
        if not no:
            no = self.raiz
        if not self.eh_bst():
            return False  # Uma AVL precisa ser uma BST primeiro

        def altura_e_balanceada(no):
            if not no:
                return 0, True
            altura_esq, balanceada_esq = altura_e_balanceada(no.filhos[0]) if len(no.filhos) > 0 else (0, True)
            altura_dir, balanceada_dir = altura_e_balanceada(no.filhos[1]) if len(no.filhos) > 1 else (0, True)
            balanceada = abs(altura_esq - altura_dir) <= 1
            return 1 + max(altura_esq, altura_dir), balanceada and balanceada_esq and balanceada_dir

        _, balanceada = altura_e_balanceada(self.raiz)
        return balanceada

    def tipo_arvore(self):
        #if not self.eh_arvore():
        #    return "Não é uma árvore"
        if not self.eh_binaria():
            return "Árvore não binária"
        if self.eh_avl():
            return "Árvore AVL (Balanceada)"
        if self.eh_bst():
            return "Árvore BST"
        if self.eh_cheia():
            return "Árvore binária cheia"
        if self.eh_completa():
            return "Árvore binária completa"
        return "Árvore binária"

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
        #if not self.eh_arvore():
        #   return {"error": "Não é uma árvore"}
        
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


    
