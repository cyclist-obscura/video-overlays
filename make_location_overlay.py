################################################################################################
#
# file			   :		make_location_overlay.py
# date			   : 		12/09/2019
# author		   :		Cyclist Obscura
# copyright		   :		(c) 2019
# licence		   : 		GNU General Public License version 3
# description	   :		Creates HTML and map PNG for Location
# version          :        1.1 Fixes filenames
#
################################################################################################

# Import required libraries
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import geotiler
import dateutil.parser as parser
import sys
import unicodedata


### String Formatter - remove diacritics ###
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

### Get Map File ###
def getMapPngFile(lat,lon,filename):
    lats = []
    lons = []
    # Small Scale
    #bbox = (lon-0.125, lat-0.0625, lon+0.125, lat+0.0625)
    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot(111)
    #
    # download background map using OpenStreetMap
    #
    mm = geotiler.Map(center=(lon, lat), zoom=11, size=(512, 512))
    img = geotiler.render_map(mm)
    #
    # create basemap
    #
    bbox = mm.extent
    map = Basemap(llcrnrlon=bbox[0], llcrnrlat=bbox[1],
                urcrnrlon=bbox[2], urcrnrlat=bbox[3],
                projection='merc', ax=ax)
    map.imshow(img, interpolation='lanczos', origin='upper')
    lats.append(lat)
    lons.append(lon)
    x, y = map(lons,lats)
    map.scatter(x,y,125,marker='o',color='r')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

### CREATE HTML FILE ###
def createHtmlFile(htmlFile, locName, mapFile, dateStr, factStrs):
    # Create filename
    f= open(htmlFile,"w+")

    # Write header
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("  <head>\n")
    f.write("    <title>Location_template</title>\n")
    f.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
    f.write("    <meta charset=\"UTF-8\">\n")
    f.write("    <link rel=\"stylesheet\" type=\"text/css\" href=\"../css_etc/obscura.css\">\n")
    f.write("  </head>\n")
    f.write("  <body>\n")

    # Write Location
    f.write("    <div class=\"fixed-location\">\n")
    f.write("      <h1>" + locName + "</h1>\n")
    f.write("    </div>\n")

    # Write Date
    f.write("    <div class=\"fixed-date\">\n")
    f.write("      <h1>" + dateStr + "</h1>\n")
    f.write("    </div>\n")

    # Write Facts
    for i in range(len(factStrs)):
        classId = "fixed-fact" + str(i+1)
        f.write("    <div class=\"" + classId + "\" align=\"right\">\n")
        f.write("      <h3>" + factStrs[i] + "</h3>\n")
        f.write("    </div>\n")

    # Write map
    mapUrl = "../" + mapFile
    f.write("    <div id=\"mapid\" style=\"top: 50px; left: 1420px;\">\n")
    f.write("      <img src=\"" + mapUrl + "\">\n")
    f.write("    </div>\n")

    # Write footer
    f.write("  </body>\n")
    f.write("</html>")

    # Close filename
    f.close()

### MAIN FUNCTION ###
def main():
    print("Make Location Overlay v 1.0")
    print("")

    # Check Number of Args
    if(len(sys.argv) < 5):
        print("Too Few Arguments!!!!")
    else:
        # Parse Command Line
        LOCATION_NAME = sys.argv[1]
        LAT = sys.argv[2]
        LON = sys.argv[3]
        LATf = float(sys.argv[2])
        LONf = float(sys.argv[3])
        dateStr = sys.argv[4]
        dateObj = parser.parse(dateStr, dayfirst = True)
        formatDate = "%a %d %b %Y"
        DATEHR = dateObj.strftime(formatDate)
        factStrings = []
        if (len(sys.argv) == 6):
            factStrings.append(sys.argv[5])
        if (len(sys.argv) == 7):
            factStrings.append(sys.argv[5])
            factStrings.append(sys.argv[6])
        if (len(sys.argv) == 8):
            factStrings.append(sys.argv[5])
            factStrings.append(sys.argv[6])
            factStrings.append(sys.argv[7])
        if (len(sys.argv) == 9):
            factStrings.append(sys.argv[5])
            factStrings.append(sys.argv[6])
            factStrings.append(sys.argv[7])
            factStrings.append(sys.argv[8])

        # Print Details
        print("...Location Name: " + LOCATION_NAME)
        print("...Latitude:      " + LAT)
        print("...Longitude:     " + LON)
        print("...Date:          " + DATEHR)
        for i in range(len(factStrings)):
            print("...Fact " + str(i) + ":        " + factStrings[i])

        # Create Filenames
        mapFile = "maps/" + LOCATION_NAME + ".png"
        htmlFile = "html/" + LOCATION_NAME + ".html"
        mapFileSafe = strip_accents(mapFile)
        htmlFileSafe = strip_accents(htmlFile)
        mapFileSafe = "_".join( mapFileSafe.split() )
        htmlFileSafe = "_".join( htmlFileSafe.split() )

        # Create Map
        getMapPngFile(LATf,LONf,mapFileSafe)

        # Create HTML file
        createHtmlFile(htmlFileSafe, LOCATION_NAME, mapFileSafe, DATEHR, factStrings)


### IF NOT USED AS LIBRARY ###
if __name__ == '__main__':
  main()
