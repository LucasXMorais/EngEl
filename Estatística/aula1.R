#source('~/aula1.R')
library(readxl)
Bussab <- read.delim("~/Engenharia Elétrica/UFSJ/Estatística/Bussab_Comp_MB.txt")
View(Bussab)

Bussab$NF #Variável número de filhos -- QUANT DISCRETA
f.NF <- table(Bussab$NF) #Freq. Absoluta do número de filhos
pro.NF <- prop.table(f.NF) #Freq. Relativa do número de filhos
per.NF <- pro.NF*100 #Freq. Percentual do número de filhos

df.NF <- matrix(0,6,3)

Bussab$GI #Variável grau de instrução -- QUANT ORDINAL
f.GI <- table(Bussab$GI) #Freq. Absoluta do grau de instrução
pro.GI <- prop.table(f.GI) #Freq. Relativa do grau de instrução
per.GI <- pro.GI*100 #Freq. Percentual do grau de instrução

df.GI <- matrix(0,6,3)

Bussab$Idade.anos. #Variável Idade.anos. -- QUANT CONTINUA
# TEM QUE AGRUPAR E DIVIDIR EM CLASSES ANTES
tamClass <- range(Bussab$Idade.anos.)
nClass <- nclass.Sturges(Bussab$Idade.anos.)
classe.id <- cut(Bussab$Idade.anos., breaks = seq(20,48,length.out=nClass+1))
# AGORA PODE PEGAR AS FREQUENCIAS QUE NEM ANTES
f.ID <- table(classe.id) #Freq. Absoluta do grau de instrução
pro.ID <- prop.table(f.ID) #Freq. Relativa do grau de instrução
per.ID <- pro.ID*100 #Freq. Percentual do grau de instrução