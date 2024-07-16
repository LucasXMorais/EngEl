# Lucas Xavier de Morais
# 09/04/24 - Criando uma classe para guardar as informações do sistema 
import numpy as np
from modules import sep, leitura

class Sistema:
    def __init__(self, dbarras: list[dict], dcircuitos: list[dict], arquivo: list[str], base: float):
        self.dbarras = dbarras
        self.dcircuitos = dcircuitos
        self.dados = arquivo
        self.nbarras = len(self.dbarras)
        self.ncircuitos = len(self.dcircuitos)
        self.base = base
        self.calcularMatrizes()
        self.lerTensaoBase()

    # Montando as matrizes admitancia e impedancia
    def calcularMatrizes(self):
        __matrizY = sep.matrizAdmitancia(self)
        self.matrizY = np.copy(__matrizY)
        self.matrizZ = np.copy(np.linalg.pinv(__matrizY))

    # Obtendo as informaçẽos das tensões bases 
    def lerTensaoBase(self):
        leitura.tensoesBase(self)

    # Resolvendo o problema de fluxo de potencia e calculando os angulos e tensoes
    def resolverFluxo(self, silent: bool=False):
        sep.calcularAngulosTensoes(self, silent)

    # Calculando todas as potencias do problema, fluxop pk, perdas ... etc
    def calcularPotencias(self):
        sep.calcularFluxoBarras(self)
        sep.calcularPerdas(self)
        sep.calcularFluxoKM(self)
        sep.potencias(self)


