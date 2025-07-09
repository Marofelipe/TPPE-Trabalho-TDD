from typing import List, Optional
import icontract

class No:
    def __init__(self, eh_folha: bool):
        self.folha = eh_folha
        self.chaves = []
        self.filhos = []

class BTree:
    def __init__(self, t: int):
        self.raiz = No(True)
        self.t = t

    def busca(self, k: int, x: Optional[No] = None):
        if x is None:
            x = self.raiz
        i = 0
        while i < len(x.chaves) and k > x.chaves[i]:
            i += 1
        if i < len(x.chaves) and k == x.chaves[i]:
            return x
        elif x.folha:
            return None
        else:
            return self.busca(k, x.filhos[i])

    @icontract.require(lambda self, k: not self.busca(k), description="Chave não deve existir na árvore")
    def inserir(self, k: int):
        r = self.raiz
        if len(r.chaves) == (2 * self.t - 1):
            s = No(False)
            self.raiz = s
            s.filhos.append(r)
            self.dividir(s, 0)
            self._inserir_nao_cheio(s, k)
        else:
            self._inserir_nao_cheio(r, k)

    def _inserir_nao_cheio(self, x: No, k: int):
        i = len(x.chaves) - 1
        if x.folha:
            x.chaves.append(0)
            while i >= 0 and k < x.chaves[i]:
                x.chaves[i+1] = x.chaves[i]
                i -= 1
            x.chaves[i+1] = k
        else:
            while i >= 0 and k < x.chaves[i]:
                i -= 1
            i += 1
            if len(x.filhos[i].chaves) == (2 * self.t - 1):
                self.dividir(x, i)
                if k > x.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(x.filhos[i], k)

    def dividir(self, x: No, i: int):
        y = x.filhos[i]
        z = No(y.folha)
        for j in range(self.t - 1):
            z.chaves.append(y.chaves[j + self.t])
        if not y.folha:
            for j in range(self.t):
                z.filhos.append(y.filhos[j + self.t])
        x.filhos.insert(i + 1, z)
        x.chaves.insert(i, y.chaves[self.t - 1])
        y.chaves = y.chaves[:self.t - 1]
        if not y.folha:
            y.filhos = y.filhos[:self.t]

    @icontract.require(lambda self, k: self.busca(k), description="Chave deve existir na árvore")
    def remover(self, k: int):
        self._remover(self.raiz, k)
        if not self.raiz.chaves and not self.raiz.folha:
            self.raiz = self.raiz.filhos[0]

    def _remover(self, x: No, k: int):
        if x.folha:
            if k in x.chaves:
                x.chaves.remove(k)
        else:
            x.chaves = list(filter(lambda c: c != k, x.chaves))

    def imprimir(self, no: Optional[No] = None, nivel: int = 0):
        if no is None:
            no = self.raiz
        print("  " * nivel + str(no.chaves))
        for f in no.filhos:
            self.imprimir(f, nivel + 1)

if __name__ == "__main__":
    arvore = BTree(3)
    for chave in [40, 20, 60, 80, 10, 15, 30, 50, 70, 90, 5, 7, 12, 18, 25, 35, 45, 55, 65, 75, 85, 92, 98, 99]:
        arvore.inserir(chave)
    arvore.imprimir()

    arvore.remover(20)
    arvore.remover(40)
    arvore.imprimir()
