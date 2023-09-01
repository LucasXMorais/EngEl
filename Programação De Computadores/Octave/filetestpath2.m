[filename,pathname]=uigetfile('*.jpg','Select the image');
B= imread(fullfile(pathname,filename), 'jpg'); 
figure(1);
imshow(B);