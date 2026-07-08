function odf2VPSC(odf,filename,varargin)
  % export an ODF to the VPSC format
  %
  %% Syntax
  % export_VPSC(odf,'file.txt','points',points)
  %
  %% Input
  %  odf      - ODF to be exported
  %  filename - name of the ascii file
  %
  %% Options
  %  points    - number of orientations
  %
  %% See also
  % ODFImportExport

  % get number of points
  points = get_option(varargin,'points',5000);

% simulate orientations
orientations = calcOrientations(odf,points,varargin{:});

% export
export_VPSC(orientations,filename,varargin{:});
