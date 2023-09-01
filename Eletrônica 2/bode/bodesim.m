clear all; close all; clc; clf;

function ret = mPrim(wn) %Modelo de primeira ordem
  str = @(s) (wn / ( s + wn ));
endfunction

function ret = mSeg(wn, csi) %Modelo de segunda ordem
  ret = @(s) ( (wn^2) / ((s^2) + (2*csi*wn*s) + (wn^2)));
endfunction

function ret = Gs(s)
  #Modelos de primeira orderm
  #wo = 1200;
  wo = 2*pi*1200;
  ret = wo / (s + wo);

  a = 1; b = 1; c = 1; d = 1;
  #ret = (a*s + b)  / (c*s + d);

  #Modelos segunda orderm
  #wo = 1200; csi = 0.5; 
  wo = 2*pi*1200; csi = 0.5;
  #ret = (wo^2) / ((s^2) + (2*csi*wo*s) + (wo^2));

  a = 1; b = 1; c = 1; d = 1; f = 1; g = 1;
  #ret = ( (a*(s^2)) + (b*s) + c)  / ( (d*(s^2)) + (f*s) + g);
endfunction

f1 = str2func("@(s)2.999e+43/((s+6.773e+04)*(s^2+2.329e+04*s+4.587e+09)*(s^2+6.281e+04*s+4.587e+09)*(s^2+8.855e+04*s+4.587e+09)*(s^2+1.022e+05*s+4.587e+09)*(s^2+1.064e+05*s+4.587e+09))");
f2 = str2func("@(s) 100/(s+100)");

function ret = bode(H)
  ret.omegas = logspace(-1, 6, 1000);

  ret.modules = ones(1,length(ret.omegas));
  ret.angles = ones(1,length(ret.omegas));

  for i = [1:length(ret.omegas)]
    s = j*(ret.omegas(i));
    aux = H(s);
    ret.modules(i) = 20*log10(abs(aux));
    ret.angles(i) = angle(aux);
  endfor
endfunction

bodes = bode(f1);

subplot (2, 1, 1)
semilogx(bodes.omegas, bodes.modules);
title('Módulo');
subplot (2, 1, 2)
semilogx(bodes.omegas, bodes.angles);
title('Fase');