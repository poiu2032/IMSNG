### read psfex.xml file and return values in it, like FWHM. 
### 2014.12.30 Changsu Choi

### this code needs astropy


from astropy.io.votable import parse
votable=parse("psfex.xml")

table=votable.get_first_table()
data= table.array

"""
masked_array(data = [ ('test_9.cat', 'PG0934p13', 1, 45, 45, 45.0, 45, 41, 41, 41, 41, 4.600130081176758, 4.600130081176758, 4.600130081176758, 0.9787520170211792, 0.9787520170211792, 0.9787520170211792, 0.999442994594574, 0.999442994594574, 0.999442994594574, 3.6838200092315674, 3.8885200023651123, 4.064889907836914, 1.107740044593811, 1.1374599933624268, 1.221250057220459, 0.011516699567437172, 0.03222360089421272, 0.045263998210430145, -0.011792800389230251, 0.028808699920773506, 0.03767060115933418, -0.02638860046863556, -0.014436700381338596, -0.0071466900408267975, 3.0891098976135254, 3.3071300983428955, 3.5271799564361572, 0.013358999975025654, 0.01991889998316765, 0.029099799692630768, 3.593630075454712, 3.8044400215148926, 3.9852499961853027, 1.0806100368499756, 1.1112300157546997, 1.1972600221633911, 0.011938500218093395, 0.03310079872608185, 0.04642999917268753, -0.01218200009316206, 0.029593100771307945, 0.038685400038957596, -0.027143599465489388, -0.014829600229859352, -0.007391550112515688, 2.9629499912261963, 3.1808199882507324, 3.3971099853515625, 0.013145100325345993, 0.019690999761223793, 0.028807800263166428, 0.016054099425673485, 0.034606900066137314, 0.05415960028767586, 50.49250030517578, 54.26129913330078, 57.87779998779297, 0.30074599385261536, 0.30074599385261536, 0.30074700713157654, 'counts_test_9.png', 'countfrac_test_9.png', 'fwhm_test_9.png', 'ellipticity_test_9.png')],
             mask = [ (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)],
       fill_value = ('?', '?', 999999, 999999, 999999, 1.0000000200408773e+20, 999999, 999999, 999999, 999999, 999999, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, 1.0000000200408773e+20, '?', '?', '?', '?'),
            dtype = [('Catalog_Name', 'O'), ('Image_Ident', 'O'), ('NExtensions', '<i4'), ('NStars_Loaded_Total', '<i4'), ('NStars_Loaded_Min', '<i4'), ('NStars_Loaded_Mean', '<f4'), ('NStars_Loaded_Max', '<i4'), ('NStars_Accepted_Total', '<i4'), ('NStars_Accepted_Min', '<i4'), ('NStars_Accepted_Mean', '<i4'), ('NStars_Accepted_Max', '<i4'), ('FWHM_FromFluxRadius_Min', '<f4'), ('FWHM_FromFluxRadius_Mean', '<f4'), ('FWHM_FromFluxRadius_Max', '<f4'), ('Sampling_Min', '<f4'), ('Sampling_Mean', '<f4'), ('Sampling_Max', '<f4'), ('Chi2_Min', '<f4'), ('Chi2_Mean', '<f4'), ('Chi2_Max', '<f4'), ('FWHM_Min', '<f4'), ('FWHM_Mean', '<f4'), ('FWHM_Max', '<f4'), ('FWHM_WCS_Min', '<f4'), ('FWHM_WCS_Mean', '<f4'), ('FWHM_WCS_Max', '<f4'), ('Ellipticity_Min', '<f4'), ('Ellipticity_Mean', '<f4'), ('Ellipticity_Max', '<f4'), ('Ellipticity1_Min', '<f4'), ('Ellipticity1_Mean', '<f4'), ('Ellipticity1_Max', '<f4'), ('Ellipticity2_Min', '<f4'), ('Ellipticity2_Mean', '<f4'), ('Ellipticity2_Max', '<f4'), ('MoffatBeta_Min', '<f4'), ('MoffatBeta_Mean', '<f4'), ('MoffatBeta_Max', '<f4'), ('Residuals_Min', '<f4'), ('Residuals_Mean', '<f4'), ('Residuals_Max', '<f4'), ('FWHM_PixelFree_Min', '<f4'), ('FWHM_PixelFree_Mean', '<f4'), ('FWHM_PixelFree_Max', '<f4'), ('FWHM_PixelFree_WCS_Min', '<f4'), ('FWHM_PixelFree_WCS_Mean', '<f4'), ('FWHM_PixelFree_WCS_Max', '<f4'), ('Ellipticity_PixelFree_Min', '<f4'), ('Ellipticity_PixelFree_Mean', '<f4'), ('Ellipticity_PixelFree_Max', '<f4'), ('Ellipticity1_PixelFree_Min', '<f4'), ('Ellipticity1_PixelFree_Mean', '<f4'), ('Ellipticity1_PixelFree_Max', '<f4'), ('Ellipticity2_PixelFree_Min', '<f4'), ('Ellipticity2_PixelFree_Mean', '<f4'), ('Ellipticity2_PixelFree_Max', '<f4'), ('MoffatBeta_PixelFree_Min', '<f4'), ('MoffatBeta_PixelFree_Mean', '<f4'), ('MoffatBeta_PixelFree_Max', '<f4'), ('Residuals_PixelFree_Min', '<f4'), ('Residuals_PixelFree_Mean', '<f4'), ('Residuals_PixelFree_Max', '<f4'), ('Asymmetry_Min', '<f4'), ('Asymmetry_Mean', '<f4'), ('Asymmetry_Max', '<f4'), ('Area_Noise_Min', '<f4'), ('Area_Noise_Mean', '<f4'), ('Area_Noise_Max', '<f4'), ('PixelScale_WCS_Min', '<f4'), ('PixelScale_WCS_Mean', '<f4'), ('PixelScale_WCS_Max', '<f4'), ('Plot_Counts', 'O'), ('Plot_Count_Fraction', 'O'), ('Plot_FWHM', 'O'), ('Plot_Ellipticity', 'O')])
"""


data['FWHM_Mean']
"""
masked_array(data = [3.8885200023651123],
             mask = [False],
       fill_value = 1e+20)
"""


fm=data['FWHM_Mean'][0]
fmw=data['FWHM_WCS_Mean'][0] 
      ##value

ps=data['PixelScale_WCS_Mean'][0]
"""
Fa = (1+Ellipticity_Mean) × FWHM_Mean
Fb = (1-Ellipticity_Mean) × FWHM_Mean
"""
em=data['Ellipticity_Mean'][0]

print "FWHM in pixel, ",fm, " FWHM in Arcsec, ",fmw, " pixel scale, ",ps


