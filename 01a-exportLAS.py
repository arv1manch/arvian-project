# 1. Import module
import lasio
import easygui as eg

# 2. Membuka file .las
file = eg.fileopenbox()
las = lasio.read(file)

# 3. Melakukan Pengecakan kesesuaian file .las
print(las.header)
print(type(las.data))
print(las.data.shape)
for curve in las.curves :
    a : print(curve.mnemonic)
    b : print(curve.unit)
    c : print(curve.descr)
    d : print(curve.data)

# 4. Melakukan save file .las ke bentuk .csv
output = str(input("Save file as "))
las.to_csv(output, units_loc='[]')

