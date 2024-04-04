clear all; close all; clc;

% Construção da matriz admitancia Y completa
function matrizY = matAdm(infoLinhas)
    Max = 0
    for linha = infoLinhas:
        if linha[0] > Max: Max = int(linha[0])
        if linha[1] > Max: Max = int(linha[1])
    matrizY = np.zeros((Max,Max),dtype=np.complex_)

    for linha = infoLinhas:
        k = int(linha[0]) - 1
        m = int(linha[1]) - 1
        admitancia = 1/(linha[2] + (1j*linha[3]))
        susceptancia = 1j*linha[4]/2
        tap = linha[5]
        defasagem = linha[6]*np.pi/180
        if k == m :
            matrizY[k][k] = matrizY[k][k] + admitancia
            continue
        matrizY[k][k] = matrizY[k][k] + (tap**2)*admitancia + susceptancia
        matrizY[k][m] = -tap*np.exp(1j*defasagem)*admitancia
        matrizY[m][k] = -tap*np.exp(-1j*defasagem)*admitancia
        matrizY[m][m] = matrizY[m][m] + admitancia + susceptancia

% Construir aqui as tabelas para as linhas para cada sequencia
% infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

infoLinhasPos = [[1, 1, 0.0, 0.20, 0.0, 1.0, 0.0];
                 [1, 3, 0.0, 0.10, 0.0, 1.0, 0.0];
                 [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0];
                 [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0];
                 [4, 5, 0.0, 0.20, 0.0, 1.0, 0.0];
                 [2, 2, 0.0, 0.20, 0.0, 1.0, 0.0];
                 [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0];]

infoLinhasPos

A = matAdm(infoLinhasPos)

Ybus = zeros(nbus,nbus);
for i = 1 : nlin
  k = barraDE(i);
  m = barraPA(i);
  ykm = 1/(rkm(i) + 1j*xkm(i));
  Ybus(k, k) = Ybus(k, k) + (akm(i)^2)*ykm + j*bkmsh(i);
  Ybus(m, m) = Ybus(m, m) + ykm + j*bkmsh(i);
  Ybus(k, m) = Ybus(k, m) - akm(i)*ykm*(cos(-phikm(i)) + 1j*sen(-phikm(i)));
  Ybus(m, k) = Ybus(m, k) - akm(i)*ykm*(cos(+phikm(i)) + 1j*sen(+phikm(i)));
end

for k = 1 : nbus
  Ybus(k, k) = Ybus(k, k) + j*bksh(k);
end
