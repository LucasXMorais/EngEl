M = 100;   % rows
N = 100;  % columns

% initialize the world randomly
world = rand(M,N) > 0.1;

kernel = [1 1 1; 1 0 1; 1 1 1];  % define neighbors

while (1),
  % count the number of neighbors using convolution
  neighbors = filter2(kernel, world);
        
  % advance to the next generation
  world = (world & (neighbors==2)) | (neighbors==3);

  % draw it
  imagesc(world);
  drawnow; 
end