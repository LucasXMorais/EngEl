# Lucas X. de Morais
# 14/08/24 - Questão 1
from scipy.optimize import linprog, minimize
import numpy as np

def semana1():
    print('SEMANA 1')
    objetivo = [50, 60, 30, 45]
    g1_limites = (140, 300)
    g2_limites = (200, 450)
    g3_limites = (250, 600)
    g4_limites = (60, 250)
    igualdades = [
            [1, 1, 1, 1]
            ]
    igualdades_limites = [1020]

    resultado = linprog(objetivo, 
                        A_eq=igualdades,
                        b_eq=igualdades_limites,
                        bounds=[
                            g1_limites,
                            g2_limites,
                            g3_limites,
                            g4_limites
                            ])
    
    print(f'Despacho: G1 = {resultado.x[0]} MW | G2 = {resultado.x[1]} MW | G3 = {resultado.x[2]} MW | G4 = {resultado.x[3]} MW ')
    print(f'Geracao: {resultado.x[0] + resultado.x[1]  + resultado.x[2] + resultado.x[3]} MW')
    print(f'Valor otimo R${resultado.fun} ')
    print("Sucesso:", resultado.success)
    print("Mensagem:", resultado.message)

def semana2():
    print('SEMANA 2')
    objetivo = [50, 60, 30, 45]
    g1_limites = (140, 300)
    g2_limites = (200, 450)
    g3_limites = (250, 600)
    g4_limites = (60, 250)
    igualdades = [
            [1, 1, 1, 1]
            ]
    igualdades_limites = [900]

    resultado = linprog(objetivo, 
                        A_eq=igualdades,
                        b_eq=igualdades_limites,
                        bounds=[
                            g1_limites,
                            g2_limites,
                            g3_limites,
                            g4_limites
                            ])
    
    print(f'Despacho: G1 = {resultado.x[0]} MW | G2 = {resultado.x[1]} MW | G3 = {resultado.x[2]} MW | G4 = {resultado.x[3]} MW ')
    print(f'Geracao: {resultado.x[0] + resultado.x[1]  + resultado.x[2] + resultado.x[3]} MW')
    print(f'Valor otimo R${resultado.fun} ')
    print("Sucesso:", resultado.success)
    print("Mensagem:", resultado.message)

