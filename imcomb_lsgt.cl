noao
imred
ccdred

ls reac*-B-*.fits > B.list
ls reac*-V-*.fits > V.list
ls reac*-R-*.fits > R.list
ls reac*-I-*.fits > I.list
ls reac*-Ha-*.fits > Ha.list
ls reac*-OIII-*.fits > OIII.list

imcombine @B.list output=comb_B_avg.fits combine=average reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode 
imcombine @V.list output=comb_V_avg.fits combine=average reject=avsigclip rdnois
e=10.0 gain=1.42 scale=none zero=mode
imcombine @R.list output=comb_R_avg.fits combine=average reject=avsigclip rdnois
e=10.0 gain=1.42 scale=none zero=mode
imcombine @I.list output=comb_I_avg.fits combine=average reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode
imcombine @Ha.list output=comb_Ha_avg.fits combine=average reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode
imcombine @OIII.list output=comb_OIII_avg.fits combine=average reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode

imcombine @B.list output=comb_B_med.fits combine=median reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode
imcombine @V.list output=comb_V_med.fits combine=median reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode
imcombine @R.list output=comb_R_med.fits combine=median reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode
imcombine @I.list output=comb_I_med.fits combine=median reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode
imcombine @Ha.list output=comb_Ha_med.fits combine=median reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode
imcombine @OIII.list output=comb_OIII_med.fits combine=median reject=avsigclip rdnoise=10.0 gain=1.42 scale=none zero=mode



