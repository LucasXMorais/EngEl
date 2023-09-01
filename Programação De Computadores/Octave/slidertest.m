hslider = uicontrol ('style', 'slider','Units', 'normalized','position', [0.1, 0.1, 0.8, 0.1],'min', 1,'max', 50,'value', 10);
res = get(hslider,'value')