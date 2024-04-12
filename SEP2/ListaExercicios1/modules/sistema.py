# Lucas Xavier de Morais
# 09/04/24 - Criando uma classe para guardar as informações do sistema 
import numpy as np
from modules import sep

class Sistema:
    def __init__(self, dbarras: list[dict], dcircuitos: list[dict], arquivo: str, base: float) -> None:
        self.dbarras = dbarras
        self.dcircuitos = dcircuitos
        self.dados = arquivo
        self.nbarras = len(self.dbarras)
        self.ncircuitos = len(self.dcircuitos)
        self.base = base
        self.calcularMatrizes()

    # Montando as matrizes admitancia e impedancia
    def calcularMatrizes(self) -> None:
        __matrizY = sep.matrizAdmitancia(self.dbarras, self.dcircuitos)
        self.matrizY = np.copy(__matrizY)
        self.matrizZ = np.copy(np.linalg.inv(__matrizY))

    # Resolvendo o problema de fluxo de potencia e calculando os angulos e tensoes
    def resolverFluxo(self, silent: bool=False) -> None:
        self.angulos, self.tensoes = sep.calcularAngulosTensoes(self.matrizY, self.dbarras, silent)
        self.angulosGrau = [(a*180/np.pi) for a in self.angulos]

    # Calculando todas as potencias do problema, fluxop pk, perdas ... etc
    def calcularPotencias(self) -> None:
        self.fluxoPkm, self.fluxoPmk, self.fluxoQkm, self.fluxoQmk, self.fluxoSkm, self.fluxoSmk = sep.calcularFluxoBarras(self.angulos, self.tensoes, self.dcircuitos)
        self.perdasP, self.perdasQ, self.perdasAtivasTotais, self.perdasReativasTotais = sep.calcularPerdas(self.fluxoPkm, self.fluxoPmk, self.fluxoQkm, self.fluxoQmk)
        self.pG, self.qG, self.sG = sep.potencias(self.matrizY, self.angulos, self.tensoes, self.dbarras)
        pCalc = np.zeros((self.nbarras,1))
        qCalc = np.zeros((self.nbarras,1))
        self.pCalc, self.qCalc = sep.calcularFluxoKM(self.matrizY, self.angulos, self.tensoes)

