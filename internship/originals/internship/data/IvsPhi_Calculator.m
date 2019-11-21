function [phi_1D, IvsPhi] = IvsPhi_Calculator (image, bc_row, bc_col,...
    parameters, varargin)

    % This script generates IvsQ and IvsPhi (phi = azimuthal angle on image) by
    % "unwrapping" an image, that is transforming the pattern from polar
    % coordinates to cartesian coordinates by interpolation on a grid of chosen
    % dimensions. The summation along the x axis
    % gives the IvsQ and the summation along the theta axis gives IvsPhi

    set(0,'defaultAxesFontSize',18);
    set(0,'defaultTextFontSize',18);
    set(0,'defaultTextFontName','Times');
    set(0,'defaultTextFontWeight','bold');

    % the beamtime parameters
    lamda = parameters(1,1);
    pixsize = parameters(2,1);
    SaDet = parameters(3,1); 
    Np = size(image,1);
    xc = bc_col; % corrected values from BeamCenter code
    yc = bc_row;  % corrected values from BeamCenter code
    w = Np * pixsize;

    % the parameters that set the number of points and the range of the summation
    if isempty(varargin)
        rmin = 250; % adjust for q_min
        rmax = 450; % adjust for q_max
        th1 = -pi/2; % mask streaks from capillary walls
        th2 = 3*pi/2; 
    elseif length(varargin) == 2
        rmin = varargin{1};
        rmax = varargin{2};
        th1 = -pi/2;
        th2 = 3*pi/2; % full circle
    elseif length(varargin) == 4
        rmin = varargin{1};
        rmax = varargin{2};
        th1 = varargin{3};
        th2 = varargin{4};
    else
        error('Only accepts 0, 2, or 4 additional arguments.\n');
    end
    nt = round(2*pi*rmax); % number of theta points
    nr = rmax-rmin;

    %read the files
    im = image;

    %create the mesh in x, y 
    [x,y] = meshgrid(1:size(im,2),1:size(im,1)); 

    % create the mesh in phi and r
    [phi_1D, radius] = meshgrid(linspace(th1,th2,nt), linspace(rmin,rmax,nr));
    xi = xc+radius.*cos(phi_1D); % these are the cartesian coordinates of each pixel
    yi = yc+radius.*sin(phi_1D);

    % 2D interpolation: interpolate the values at (xi, yi) of the original
    % the image im so that each pixel corresponds to an (xi, yi) of the unwrapped image
    mapping = interp2(x, y, double(im), xi, yi); 
    mapping(isnan(mapping)) = 0; % fill out the NaN values with zero
    
    % The summations give the IvsQ and IvsPhi
    IvsPhi = mean(mapping, 1);
    
%     figure(105)
%     imagesc (mapping)

    qq = 4 * 10^-10*pi*sin(0.5*atan(radius*pixsize/SaDet))/lamda; % the Q grid
    Q = qq(:,1); %the q range for this IvsQ, confirm that it's the same length for all analysis
    phi_1D = phi_1D(1,:)*180/pi-90; % azimuthal angle on detector    
end



