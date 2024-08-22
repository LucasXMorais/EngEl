# Lucas X. Morais
# 21/08/24 - Programa pra calcular tensao eficaz harmonica
import sys
import numpy as np

def argumentos(argv: list) -> dict:
    Vin = 400
    maxOrder = 50
    fundamental = 60

    c = 0 
    for arg in argv:
        if c == 0: c+=1; continue

        match arg[0]:
            case 'f':
                fundamental = int(arg[1:])
            case 'v':
                Vin = float(arg[1:])
            case 'o':
                maxOrder = int(arg[1:])
            case _:
                pass

    paramaters = {
            'Vin' : Vin,
            'maxOrder': maxOrder,
            'fundamental': fundamental
            }

    return paramaters

def main():

    def lerArquivo():
        with open('FFT.txt', 'r') as f:
            c = 0
            for line in f:
                if c == 0: c+=1; continue

                line = line.split('\t')
                linha = {
                        "order" : line[0],
                        "frequency" : int(np.trunc(float(line[1]))),
                        "value" : float(line[2].split('\n')[0])
                        }

                fft.append(linha)

                c+=1

    def lerHarmoincas():
        return [f for f in fft if f["frequency"] != 0 and f["frequency"] % fundamental == 0]

    def calcularHarmonicas(maxOrder: int):

        def fourier(order: int):
            return (4*Vin)/(order*np.pi)

        def par(n):
            return n % 2

        harm = []
        for o in range(maxOrder):
            o+=1
            freq = o * fundamental
            tensaoCarga_n = 0
            if par(o): tensaoCarga_n = fourier(o)
            freq_atual = {
                    "frequency" : int(freq),
                    "value" : tensaoCarga_n
                    }
            harm.append(freq_atual)
        return harm

    def calcularPico(harmonics: list, maxOrder=None):
        eff = 0
        for h in harmonics:
            if maxOrder and h["frequency"]/fundamental > maxOrder: break
            eff += h["value"]**2
        return np.sqrt(eff)

    def eficaz(valor_max):
        return (valor_max / np.sqrt(2))

    param = argumentos(sys.argv)
    Vin = param["Vin"]
    maxOrder = param['maxOrder']
    fundamental = param['fundamental']

    fft = []
    lerArquivo()
    harmonicas_psim = lerHarmoincas()

    print('--------')
    print('TENSÃO TOTAL')
    print('--------')
    Vmax_medido  = calcularPico(harmonicas_psim, maxOrder)
    Veff_medido = eficaz(Vmax_medido)
    string = f'V_max = {Vmax_medido:.6f} V | V_eff = {Veff_medido:.6f} V'
    print("VALORES PSIM")
    print(string)

    harmonicas_calculado = calcularHarmonicas(maxOrder)
    Vmax_calculado  = calcularPico(harmonicas_calculado, maxOrder)
    Veff_calculado = eficaz(Vmax_calculado)
    string = f'V_max = {Vmax_calculado:.6f} V | V_eff = {Veff_calculado:.6f} V'
    print("VALORES CALCULADOS")
    print(string)

    string = f'Diferença PSIM e Cálculos: {np.abs(Veff_medido - Veff_calculado):.8f}'
    print(string)

    print('--------')
    print('TENSÃO FUNDAMENTAL')
    print('--------')
    Vmax_psim_fundamental  = calcularPico(harmonicas_psim, 1)
    Veff_psim_fundamental = eficaz(Vmax_psim_fundamental)
    string = f'V_max = {Vmax_psim_fundamental:.6f} V | V_eff = {Veff_psim_fundamental:.6f} V'
    print("VALORES PSIM")
    print(string)

    harmonicas_fundamental_calc = calcularHarmonicas(1)
    Vmax_fundamental_calc  = calcularPico(harmonicas_fundamental_calc, 1)
    Veff_fundamental_calc = eficaz(Vmax_fundamental_calc)
    string = f'V_max = {Vmax_fundamental_calc:.6f} V | V_eff = {Veff_fundamental_calc:.6f} V'
    print("VALORES CALCULADOS")
    print(string)

    string = f'Diferença PSIM e Cálculos: {np.abs(Veff_psim_fundamental - Veff_fundamental_calc):.8f}'
    print(string)

    # FIM MAIN

if __name__ == '__main__':
    main()
