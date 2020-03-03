import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import easygui as eg
from mpl_toolkits.axes_grid1 import make_axes_locatable
# from scipy.interpolate import spline

file = eg.fileopenbox()
data = pd.read_csv(file)

# Konversi Density
a = np.log(data['LD [CPS]'])
data['LD [gr/cc]'] = ((-0.424)*a+5.0491)

# Rename Columns
data.rename(columns={'DEPT [M]' : 'DEPTH'}, inplace=True)
data.rename(columns={'SD [CPS]' : 'SD'}, inplace=True)
data.rename(columns={'LD [gr/cc]' : 'LD'}, inplace=True)
data.rename(columns={'GR [CPS]' : 'GR'}, inplace=True)
data.rename(columns={'SKB [CPS]' : 'SKB'}, inplace=True)
data.rename(columns={'CL [INCH]' : 'CL'}, inplace=True)

# Batubara
batubara=((data['GR']<=51.0) & (data['LD']<=2.18))
batubara=((data['GR']<=150.0) & (data['LD']<=2.18))
# Batupasir
batupasir=((data['GR']>=52.0) & (data['LD']>=2.19))
#Batulempung
batulempung=((data['GR']>=80.0) & (data['LD']>=2.30))

# Creating interpretation data columns
intrp_awal = np.zeros(np.shape(data['DEPTH']))
intrp_awal[batubara.values] = 1
intrp_awal[batupasir.values] = 2
intrp_awal[batulempung.values] = 3
data['LFC'] = intrp_awal

# input depth & fig parameter
top_depth=float(data.DEPTH.min())
bottom_depth=float(data.DEPTH.max())
logs=data.loc[(data.DEPTH>=top_depth) & (data.DEPTH<=bottom_depth)]
logs=logs.sort_values(by='DEPTH')

# Assigning colormap
ccc = ['#B3B3B3','black','yellow','green',]
cmap_facies = colors.ListedColormap(ccc[0:len(ccc)],'indexed')
cluster = np.repeat(np.expand_dims(logs['LFC'].values,1),50,1)

# Plotting figure
f, ax = plt.subplots(nrows=1, ncols=5, figsize=(9,16))
nama_sumur=str(input("nama_sumur = "))
f.suptitle(nama_sumur, fontsize=22)
f.subplots_adjust(bottom=0.03, wspace=0.30)

# Setting axes
# for axes in ax:
#     axes.set_ylim(top_depth,bottom_depth)
#     axes.invert_yaxis()
#     axes.yaxis.grid(True)
#     axes.grid(linewidth=1)
#     axes.get_xaxis().set_visible(False)

# 1st track GR
ax01 = ax[0].twiny()
ax01.set_ylim(top_depth,bottom_depth)
ax01.invert_yaxis()
ax01.set_xlim(0,150)
ax01.spines['top'].set_position(('outward', 0))
ax01.set_xlabel("GR [CPS]")
ax01.plot(logs.GR, logs.DEPTH, label='GR [CPS]', color='red', linewidth=0.5)
ax01.set_xlabel('GR [CPS]', color='red')
ax01.tick_params(axis='x', colors='red')
ax[0].grid(True)
ax[0].get_xaxis().set_visible(False)

# 2nd track LD
ax11 = ax[1].twiny()
ax11.set_ylim(top_depth,bottom_depth)
ax11.invert_yaxis()
ax11.set_xlim(2,3)
ax11.spines['top'].set_position(('outward',0))
ax11.set_xlabel('LD [gr/cc]', color='blue')
ax11.plot(logs.LD, logs.DEPTH, label='LD [CPS]', color='blue', linewidth=0.5)
ax11.tick_params(axis='x', colors='blue')
ax[1].grid(True)
ax[1].get_xaxis().set_visible(False)

# 3rd track SD
ax21 = ax[2].twiny()
ax21.set_ylim(top_depth,bottom_depth)
ax21.invert_yaxis()
ax21.set_xlim(logs.SD.min(),logs.SD.max())
ax21.spines['top'].set_position(('outward',0))
ax21.set_xlabel('SD [CPS]',color='green')
ax21.plot(logs.SD, logs.DEPTH, label='SD [CPS]', color='green', linewidth=0.5)
ax21.tick_params(axis='x', colors='green')
ax[2].grid(True)
ax[2].get_xaxis().set_visible(False)

# 4th track CL
ax31 = ax[3]
ax31.set_ylim(top_depth,bottom_depth)
ax31.invert_yaxis()
ax31.set_xlim(2.9,3.2)
ax31.spines['top'].set_position(('outward', 0))
ax31.set_xlabel('CL [in]', color='black')
ax31.plot(logs.CL, logs.DEPTH, label='CL [in]', color='black', linewidth=0.5)
ax31.tick_params(axis='x', colors='black')
ax31.grid(True)

ax32 = ax[3].twiny()
ax32.set_ylim(top_depth,bottom_depth)
ax32.invert_yaxis()
ax32.invert_xaxis()
ax32.set_xlim(3.2,2.9)
ax32.plot(logs.CL, logs.DEPTH, label='CL [in]', color='black', linewidth=0.5)
ax[3].get_xaxis().set_visible(False)

# 5th track Interpretation
ax41 = ax[4]
ax41.set_xlim(0,4)
ax41.axes.get_yaxis().set_ticks([])
ax[4].get_xaxis().set_visible(False)
im = ax41.imshow(cluster,interpolation=None, aspect='auto',cmap=cmap_facies,vmin=0,vmax=4)
divider = make_axes_locatable(ax[4])
cax = divider.append_axes('right', size='10%', pad=0.05)
cbar=plt.colorbar(im,cax=cax)

# out = str(input("Save data file as "))
# logs.to_csv(out, index=False)

plt.show()