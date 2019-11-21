clear all
close all
clc



% file parameters
% binning of 6 for SAXS
folder = 'flow';
saxs_tag = 'hs104';
bkg_scan = 183;
n_frames_per_scan = 10; % number of frames per scan
ext = '.tif'; % extension of data files
sample_scans = [184];
sample_conc_arr = [0.01];
sample_conc_tag = ' ppm';
subtract_background = true;
save_figs = true;
save_data = true;
rmin = 10;
rmax = 450;

% create legend of concentrations
legend_arr = num2cell(sample_conc_arr);
for i = 1:length(legend_arr)
    legend_arr{i} = strcat(num2str(legend_arr{i}), sample_conc_tag);
end

% set parameters
set(0,'defaultAxesFontSize',20);
set(0,'defaultTextFontSize',20);
set(0,'defaultTextFontName','Helvetica');

%beam center - ORIGINAL!
row_center = 764;
col_center = 196;

% the beamtime parameters
lamda = 0.7293*10^-10; % in m
pixsize = 177.20 *10^-6; % in m  
SaDet = 8502.8 * 10^-3 ; % in m
parameters = [lamda; pixsize; SaDet];
exposure_time = 30; % seconds

%% create an average background 
bkg_sum = 0;
for i = 0:n_frames_per_scan-1
    img_filename = strcat(folder, '_', saxs_tag, '_', num2str(bkg_scan),...
        '_' , sprintf('%04d', i), ext);
    bkg = imread(img_filename);
    % median filter
    bkg = medfilt2(bkg, [3 3]);
    bkg_sum = bkg_sum + double(bkg);
end
bkg_avg = bkg_sum./n_frames_per_scan;

%% Process data

for k = 1:length(sample_scans)
    % load number of sample scan
    scan = sample_scans(k,1); 
    sample_conc = sample_conc_arr(k);
    disp (scan); 
    
    img_sum = 0;
    for i = 0:n_frames_per_scan-1
        % set the filename
        img_filename = strcat(folder, '_', saxs_tag, '_', num2str(scan),...
            '_' , sprintf('%04d', i), ext);
    
        % open the image, filter, and subtract background
        img = double(imread(img_filename)); 
        img = medfilt2(img, [3 3]);
        img_sum = img_sum + img;
    end
    img_avg = img_sum./n_frames_per_scan;
    
    % subtract background
    if subtract_background
        img_subt = img_avg - bkg_avg;
    else
        img_subt = img_avg;
    end
          
    %plot
    figure(k)
    imagesc (img_subt, [0 75]);
    axis image
    colorbar
    axis off
    colormap jet
    title (strcat('SAXS of ', {' '}, num2str(sample_conc),...
        sample_conc_tag, ' SiO_2 NP in H_2O (bkg-subt) 30s exp.'))
    
    % save image
    if save_figs
        exponent = floor(log10(sample_conc));
        coeff = sample_conc / 10^exponent;
        print(sprintf('SAXS_2D_%de%dppm_SiO2_H2O_30s_exp', coeff, exponent),'-dpdf')
    end

    %compute I(q) and I(phi) with background subtraction
    [q_1D, IvsQ_Sub(:,k)] = IvsQ_Calculator (img_subt, row_center,...
        col_center, parameters, rmin, rmax);
    [phi_1D, IvsPhi_Sub(:,k)] = IvsPhi_Calculator (img_subt, row_center,...
        col_center, parameters, rmin, rmax);
    
    %compute I(q) and I(phi) without background subtraction
    [q_1D, IvsQ(:,k)] = IvsQ_Calculator (img_avg, row_center,...
        col_center, parameters, rmin, rmax);
    [phi_1D, IvsPhi(:,k)] = IvsPhi_Calculator (img_avg, row_center,...
        col_center, parameters, rmin, rmax);
    
end

%compute I(q) and I(phi) of background
[q_1D, IvsQ(:,k+1)] = IvsQ_Calculator (bkg_avg, row_center,...
    col_center, parameters, rmin, rmax);
[phi_1D, IvsPhi(:,k+1)] = IvsPhi_Calculator(bkg_avg, row_center,...
    col_center, parameters, rmin, rmax);
 
%% save data
if save_data
    csvwrite ('q_1D_30s_exp.csv', q_1D);
    csvwrite (strcat('SAXS_', folder, '_IvsQ_sub_30s_exp.csv'), IvsQ_Sub);
    csvwrite (strcat('SAXS_', folder, '_IvsQ_30s_exp.csv'), IvsQ);
    csvwrite ('phi_1D_30s_exp.csv', phi_1D);
    csvwrite (strcat('SAXS_', folder, '_IvsPhi_sub_30s_exp.csv'), IvsPhi_Sub);
        csvwrite (strcat('SAXS_', folder, '_IvsPhi_30s_exp.csv'), IvsPhi);
end
%% Plot IvsQ with background subtracted

% remove NaN
i_positive = find(IvsQ_Sub>0);
IvsQ_Sub(isnan(IvsQ_Sub)) = 0;

% find peak intensity (for determining axis limits)
I_max = max(IvsQ_Sub);
xmin = q_1D(min(i_positive));
xmax = max(q_1D);
ymin = 0;
ymax = I_max*1.1;

% plot figure
figure(3000)
semilogy (q_1D, IvsQ_Sub, 'linewidth', 2)
hold on
axis ([xmin xmax ymin ymax])
xlabel ('q(1/Å)')
ylabel ('Intensity[a.u.]')
title('SAXS of 0.01 ppm 50 nm SiO_2 NPs in H_2O (bkg-subt)')
legend ([legend_arr, {'bkg'}], 'Location', 'Best', 'FontSize',12); 
box on

% save image
if save_figs
    print('SAXS_IvsQ_Sub_1e-2ppm_SiO2_H2O_30s_exp','-dpdf')
end

%% Plot IvsQ with background subtracted

% remove NaN
i_positive = find(IvsQ>0);
IvsQ(isnan(IvsQ)) = 0;

% find peak intensity (for determining axis limits)
I_max = max(max(IvsQ));
xmin = q_1D(min(i_positive));
xmax = max(q_1D);
ymin = 0;
ymax = I_max*1.1;

% plot figure
figure(3200)
semilogy (q_1D, IvsQ, 'linewidth', 2)
hold on
axis ([xmin xmax ymin ymax])
xlabel ('q(1/Å)')
ylabel ('Intensity[a.u.]')
title('SAXS of 0.01 ppm 50 nm SiO_2 NPs in H_2O (raw)')
legend ([legend_arr, {'bkg'}], 'Location', 'Best', 'FontSize',12); 
box on

% save image
if save_figs
    print('SAXS_IvsQ_1e-2ppm_SiO2_H2O_30s_exp','-dpdf')
end

%% Plot I(phi) with background subtracted

% remove NaN
IvsPhi_Sub(isnan(IvsPhi_Sub)) = 0;

% axis limits
I_max = max(IvsPhi_Sub);
xmin = -180;
xmax = 180;
ymin = 0;
ymax = I_max*1.1;

figure(4000)
plot (phi_1D, IvsPhi_Sub, 'linewidth', 2)
axis ([xmin xmax ymin ymax])
xlabel ('Phi[°]')
ylabel ('Intensity[a.u.]')
title('SAXS of 0.01 ppm 50 nm SiO_2 NPs in H_2O (bkg-subt)')
legend ([legend_arr, {'bkg'}], 'Location', 'Best'); 
box on

% save image
if save_figs
    print('SAXS_IvsPhi_sub_1e-2ppm_SiO2_H2O_30s_exp','-dpdf')
end

%% Plot I(phi) raw

% remove NaN
IvsPhi(isnan(IvsPhi)) = 0;

% axis limits
I_max = max(max(IvsPhi));
xmin = -180;
xmax = 180;
ymin = 0;
ymax = I_max*1.1;

figure(4200)
plot (phi_1D, IvsPhi, 'linewidth', 2)
axis ([xmin xmax ymin ymax])
xlabel ('Phi[°]')
ylabel ('Intensity[a.u.]')
title('SAXS of 0.01 ppm 50 nm SiO_2 NPs in H_2O (bkg-subt)')
legend ([legend_arr, {'bkg'}], 'Location', 'Best'); 
box on

% save image
if save_figs
    print('SAXS_IvsPhi_1e-2ppm_SiO2_H2O_30s_exp','-dpdf')
end