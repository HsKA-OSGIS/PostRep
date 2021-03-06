import shapefile
import csv
from random import uniform, random, choice
from string import ascii_uppercase, ascii_lowercase
from time import time

initial_time = time()
#-----------------------------------------------------------------------------
#----------------------------      Functions      ----------------------------
def polygon_coord_from_shp(file):
    """ Reads shapefile and extracts the coordinates of the polygon
        - Uses first feature
        - file: shapefile with path"""
    shape = shapefile.Reader(file)
    # first feature of the shapefile
    feature = shape.shapeRecords()[0]
    first = feature.shape.__geo_interface__  # GeoJSON format
    polygon = list(first['coordinates'][0])
    return polygon

def point_in_polygon(x, y, polygon):
    """ Check if a point is inside a polygon
        - x,y - Coordinates of the point
        - polygon - List of the vertices of the polygon [(x1, x2), (x2, y2), ..., (xn, yn)]"""
    i = 0
    j = len(polygon) - 1
    res = False
    for i in range(len(polygon)):
        if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
            if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (
                    polygon[j][0] - polygon[i][0]) < x:
                res = not res
        j = i
    return res
#-----------------------------------------------------------------------------
""" Times to upscale data: """
times = 100000

# Empty lists and others variables
all_data_list, date_list, city_list = [], [],  []
new_list_city, new_list_x, new_list_y, new_list_z = [], [], [], []
x_min, y_min, z_min = 99999, 99999, 99999
x_max, y_max, z_max = -99999, -99999, -99999

""" Open the original file from \home\user\PostRep\input
	Is delimited by coma (,). The header has to be added manually. 
	 - Format for header: 
	id,city,x,y,z,date,time,value 
"""

f = open(" \home\user\PostRep\input\data.csv", "r")

reader = csv.DictReader(f, delimiter=',')
for row in reader:
    # Random values for erroneous data for column 'values', in this case more than two
    if float(row['value']) > 2:
        row['value'] = "{0:.12f}".format(random())
    # Creating the list with date-time to add in new data
    if row['date']+' ' + row['time'] not in date_list:
        date_list.append( row['date'] +' ' + str(row['time']))
    # Defining max and min for new coordinates
    if x_min >= float(row['x']): x_min = float(row['x'])
    if x_max <= float(row['x']): x_max = float(row['x'])
    if y_min >= float(row['y']): y_min = float(row['y'])
    if y_max <= float(row['y']): y_max = float(row['y'])
    if z_min >= float(row['z']): z_min = float(row['z'])
    if z_max <= float(row['z']): z_max = float(row['z'])

    # Creating a new dictionary with correct data
    data = {'id': row['id'], 'city': row['city'], 'x':row['x'], 'y': row['y'], 'z': row['z'], 'date': row['date'], 'time': row['time'], 'value': row['value']}
    all_data_list.append(data)

""" Since the original bourder of Germany  has too much borders to check, it has been simplified."""
file2 = "\home\user\PostRep\Upscaled_data\Simplified_boundary_Germany\germany2.shp"
polygon = polygon_coord_from_shp(file2) # Creating dictionary from shapefile

# Creating new random points coordinates and City's names:
while len(new_list_x)!=times:
    x, y = uniform(x_min, x_max), uniform(y_min, y_max)
    # Check if new created point is inside of the boundary
    if point_in_polygon(x, y, polygon)==True:
        new_list_x.append(x)
        new_list_y.append(y)
        new_list_z.append(uniform(z_min, z_max))
        new_list_city.append(choice(ascii_uppercase) + choice(ascii_lowercase) + choice(ascii_lowercase) + choice(ascii_lowercase) + choice(ascii_lowercase))

# Number of new points
num_total_new_points=len(date_list)
# Id for new points
cont2=len(all_data_list)-1
# The names of resulting columuns for upscaled data
csv_columns = ['id','city','x','y','z','date','time','value']

# Creating new csv file with results
with open('new_test_'+str(times)+'.csv', 'wb') as f2:
    # Creating the header
    writer = csv.DictWriter(f2,fieldnames=csv_columns)
    writer.writeheader()
    # Original data
    for row in all_data_list:
        writer.writerow(row)
    # Adding new data to the file
    for k in range(times):
        for m in range(len(date_list)):
            cont2 += 1
            line = {'city': new_list_city[k],
                             'value': "{0:.12f}".format(random()),
                              'y': "{0:.3f}".format(new_list_y[k]),
                              'date': date_list[m][0:10],
                              'time':date_list[m][11:],
                              'x': "{0:.3f}".format(new_list_x[k]),
                              'z': "{0:.3f}".format(new_list_z[k]),
                              'id': cont2}
            writer.writerow(line)
# Close the csv files
f.close()
f2.close()
print ('The process is finished.')
final_time = time()
execution_time = final_time - initial_time
print ('The execution time was: '+ str(execution_time) + ' seconds.')  # In seconds

