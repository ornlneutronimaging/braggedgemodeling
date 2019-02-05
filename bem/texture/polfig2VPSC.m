function polfig2VPSC(polfigpath, hkls, outpath, points)
  %% Import Script for PoleFigure Data

  %% Specify Crystal and Specimen Symmetries
  % crystal symmetry
  CS = crystalSymmetry('1', [1 1 1], [90,90,90]*degree, 'X||a', 'Y||b*', 'Z||c*', 'color', 'light blue');

% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
fname = [polfigpath];

%% Specify Miller Indice
nhkl = size(hkls, 1);
h = arrayfun( @(IDX) Miller(mat2cell(hkls(IDX,:), 1, ones(1, 3)), CS), (1:nhkl).', 'uniform', 0);

%% Import the Data

% create a Pole Figure variable containing the data
pf = loadPoleFigure(fname,h,CS,SS,'interface','siemens');

odf = calcODF(pf);
odf2VPSC(odf, outpath, 'points', points);
