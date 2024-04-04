# 25/03/24 - Lucas Xavier de Morais 
# Leitura e processamento de dados para SEP
# SEP II - Engenharia Elétrica (UFSJ)

def lerDados(arquivo):
    dbarras = []; dcircuitos = []
    with open(arquivo, 'rb') as f:
        infoType = 1
        for line in f:
            l = line.decode(errors='replace')
            l = l.split(' ')
            l = [i for i in l if i]
            if l[0][0] == '#': 
                infoType += 1
                continue
            if l[0].isnumeric():
                match infoType:
                    case 1:
                        # ['BARRA', 'PD(PU)', 'QD(PU)', 'Bsh(PU)', 'TIPO', 'Vesp(PU)', 'Oesp(�)', 'PGesp(PU)', 'Cus($/MW)', 'CGmin(PU)', 'CGmax(PU)\r\n']
                        barra = {
                            'BARRA' : int(l[0]),
                            'PD(PU)' : float(l[1]),
                            'QD(PU)' : float(l[2]),
                            'Bsh(PU)' : float(l[3]),
                            'TIPO' : l[4],
                            'Vesp(PU)' : float(l[5]),
                            'Oesp' : float(l[6]),
                            'PGesp(PU)': float(l[7]),
                            'Cus': float(l[8]),
                            'CGmin(PU)': float(l[9]),
                            'CGmax(PU)': float(l[10])
                        }
                        dbarras.append(barra)
                    case 2:
                        # BDE  BPARA  NCIR  RES(PU) REAT(PU) SUCsh(PU)  TAP(PU) DEF(GRAUS) LIG(L)DESL(D)   CAP(PU)
                        circuito = {
                            'BDE' : int(l[0]),
                            'BPARA' : int(l[1]),
                            'NCIR' : int(l[2]),
                            'RES(PU)' : float(l[3]),
                            'REAT(PU)' : float(l[4]),
                            'SUCsh(PU)' : float(l[5]),
                            'TAP(PU)' : float(l[6]),
                            'DEF(GRAUS)' : float(l[7]),
                            'LIG(L)DESL(D)' : l[8],
                            'CAP(PU)' : float(l[9])
                       }
                        dcircuitos.append(circuito)
                    case 3:
                        break
        return dbarras, dcircuitos


