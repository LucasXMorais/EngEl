# Lucas Xavier de Morais
# 09/04/24 - Criando uma classe para guardar as informações do sistema 
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
from modules import sep, leitura, newton, linearizado

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
        self.convergiu = True
        self.dbarrasBackup = self.dbarras
        self.dcircuitosBackup = self.dcircuitos
        self.emContingencia = False
        self.contingencias = []
        self.usarFluxoNewton = False
        self.iteracoes = 0

    # Montando as matrizes admitancia e impedancia
    def calcularMatrizes(self):
        __matrizY = sep.matrizAdmitancia(self)
        self.matrizY = np.copy(__matrizY)
        self.matrizZ = np.copy(np.linalg.pinv(__matrizY))
        __matYLinearizado = sep.matrizLinearizados(self)
        self.matGkmLinear = np.copy(__matYLinearizado.real)
        self.matBkmLinear = np.copy(__matYLinearizado.imag)

    # Obtendo as informaçẽos das tensões bases 
    def lerTensaoBase(self):
        leitura.tensoesBase(self)

    # Resolvendo o problema de fluxo de potencia e calculando os angulos e tensoes
    def resolverFluxo(self, silent: bool=False):
        newton.calcularFluxoNewton(self, silent)
        newton.calcularFluxoBarras(self)
        newton.calcularPerdas(self)
        newton.calcularFluxoKM(self)
        newton.potencias(self)

    # Resolvendo o problema de fluxo de potencia e calculando os angulos e tensoes
    def fluxoLinearizado(self, silent: bool=False):
        linearizado.fluxoLinear(self)

    def entrarContingencia(self, contingencias: list):
        self.dcircuitos = self.dcircuitosBackup.copy()
        self.dcircuitosBackup = self.dcircuitos.copy()
        self.emContingencia = True
        if contingencias[0] == 0: return
        self.contingencias = [int(c) for c in contingencias]
        self.dcircuitos = [b for b in self.dcircuitos if b['NCIR'] not in contingencias]
        self.calcularMatrizes()

    def sairContingencia(self):
        self.dcircuitos = self.dcircuitosBackup.copy()
        self.emContingencia = False
        self.calcularMatrizes()
        self.resolverFluxo(True)
        self.contingencias = []

    def alterarCircuito(self, circuito: int, campo: str, valor):
        self.dcircuitos[circuito][campo] = valor
        self.dcircuitosBackup[circuito][campo] = valor

    def alterarBarra(self, barra: int, campo: str, valor):
        self.dbarras[barra][campo] = valor
        self.dbarrasBackup[barra][campo] = valor







