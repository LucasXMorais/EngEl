%Função que calcula dy/dt de um sistema com uma entrada 

function dy = exercicio5(t,y,u1, u2)
  u = u1*((-2)*cos(0.5*t)) + u2*(3*sin(3*t));
  dy = (-3)*y + 2*u;
end