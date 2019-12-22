from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection='mill',
            # llcrnrlat=10,
            # llcrnrlon=-100,
            # urcrnrlat=65,
            # urcrnrlon=-35,
            )

m.drawcoastlines()
m.fillcontinents()
m.drawcountries()

lat,lon = 23.0258, 72.5873
x_pt,y_pt = m(lon,lat)

m.plot(x_pt,y_pt,'c*',markersize=5)

plt.title('Geo')
plt.show()
