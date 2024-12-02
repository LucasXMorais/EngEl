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
        self.lerPosicoes()
        self.calcularDistanciaCircuitos()
        self.calcularReatanciaMedia()
        self.convergiu = True
        self.dbarrasBackup = self.dbarras
        self.dcircuitosBackup = self.dcircuitos
        self.emContingencia = False
        self.contingencias = []
        self.usarFluxoNewton = False
        self.iteracoes = 0
        self.linearizadoSemPerdas = False

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

    # Obtendo as informaçẽos das tensões bases 
    def lerPosicoes(self):
        leitura.posicao(self)

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

    def getBarra(self, barra: int):
        for b in self.dbarras:
            if b["BARRA"] == barra: return b

    # def removerCircuito(self, circuito: int):
    #     print('removendo circuito')
    #     print(len(self.dbarras), len(self.dcircuitos))
    #     auxCircuitos = [c for c in self.dcircuitos if c["NCIR"] != circuito]
    #     if len(self.dcircuitos) == len(auxCircuitos): print("Circuito não encontrado"); return
    #     print('circuito removido')
    #     self.dcircuitos = auxCircuitos
    #     print(len(self.dbarras), len(self.dcircuitos))

    # def removerBarra(self, barra: int):
    #     print('removendo barra')
    #     print(len(self.dbarras), len(self.dcircuitos))
    #     auxBarra = [b for b in self.dbarras if b["BARRA"] != barra]
    #     if len(self.dbarras) == len(auxBarra): print("Barra não encontrada"); return
    #     self.dbarras = auxBarra
    #     circuitos_barra = [c["NCIR"] for c in self.dcircuitos if c["BDE"] == barra or c["BPARA"] == barra]
    #     for circuito in circuitos_barra: self.removerCircuito(circuito) 
    #     print('barra removida')
    #     print(len(self.dbarras), len(self.dcircuitos))

    def calcularDistanciaCircuitos(self):
        for c in self.dcircuitos:
            bDE = self.getBarra(c["BDE"])
            posDE = (bDE['x'], bDE['y'])
            bPARA = self.getBarra(c["BPARA"])
            posPARA = (bPARA['x'], bPARA['y'])
            c['distancia'] = 1.2 * np.sqrt( (posDE[0] - posPARA[0])**2 + (posDE[1] - posPARA[1])**2 )
            # print(c['BDE'], c['BPARA'], c['distancia'])

    def calcularReatanciaMedia(self):
        #inicialização dos parâmetros
        reatancia_media = 0

        #Obtem todos os niveis de tensao
        niveis_tensao = []
        for b in self.dbarras:
            if b['VBase'] not in niveis_tensao: niveis_tensao.append(b['VBase'])

        #Calcula a reatancia para cada nivel de tensão
        reatancias_medias = []
        for nivel in niveis_tensao:
            circuitos = 0 
            reatancia_media = 0
            for c in self.dcircuitos:
                if c['distancia'] == 0: continue
                #Verficiando o nivel de tensao das duas barras
                bDE = self.getBarra(c["BDE"])
                bPARA = self.getBarra(c["BPARA"])
                #Para niveis diferentes o circuito é um trafo
                if bDE['VBase'] != nivel or bDE['VBase'] != bPARA['VBase']: continue

                # Faz o cálculo da reatância
                reatancia_por_km = c['REAT(PU)'] / c['distancia']
                reatancia_media += reatancia_por_km
                circuitos += 1
            # fim circuito
            reatancias_medias.append( (nivel, reatancia_media / circuitos) )
        self.reatancias_medias = reatancias_medias
        # print(self.reatancias_medias)
        # Fim todos os niveis








