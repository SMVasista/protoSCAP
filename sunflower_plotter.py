from __future__ import division
import sys, os, re, random, math
import utils
import subprocess

cwl = os.getcwd()

def dToR(theta):
    return float(theta/180)*3.14159

def rtoD(theta):
    return float(theta*180)/3.14159

def parseConnectors(cDict):
    nodes = cDict.keys()

    node_i = []
    for node in nodes:
        for elem in node.split('_+_'):
            if elem not in node_i:
                node_i.append(elem)

    l_nodes = len(node_i)

    spe = []
    for elem in nodes:
        for entry in cDict[elem]:
            if entry not in spe:
                spe.append(entry)
    l_spe = len(spe)

    spe_matrix = {}
    for s in spe:
        spe_matrix[s] = []
        for elem in nodes:
            if s in cDict[elem]:
                for quant in elem.split('_+_'):
                    spe_matrix[s].append(quant)
        spe_matrix[s] = list(set(spe_matrix[s]))

    return node_i, spe, l_nodes, l_spe, spe_matrix

def computeNodesAndCord(nodes, spe, l_nodes, l_spe, spe_matrix):
    NODES = {}
    TEXTS = {}
    T_CIRCLES = {}
    
    node_angle = dToR(180/l_nodes)
    r = 50
    
    for i, elem in enumerate(nodes):
        NODES[elem] = (r*math.cos((i+1)*node_angle), r*math.sin((i+1)*node_angle), (i+1)*node_angle)

    for spe in spe_matrix:
        if len(spe_matrix[spe]) == 1:
            r = 100
            theta = NODES[spe_matrix[spe][0]][2]
            TEXTS[spe] = (r*math.cos(theta)+random.randint(-7, 7), r*math.sin(theta)+random.randint(-7, 7), theta)

        if len(spe_matrix[spe]) > 1:
            v = []
            for h in spe_matrix[spe]:
                v.append(NODES[h][2])
            a = max(v)
            b = min(v)
            r = 95*len(spe_matrix[spe]) + 20*math.sin(a+b)/2
            theta = (a+b)/2
            TEXTS[spe] = (r*math.cos(theta)+random.randint(-7, 7), r*math.sin(theta)+random.randint(-7, 7), theta)
        T_CIRCLES[spe] = (TEXTS[spe][0]+5, TEXTS[spe][1], str(len(spe)/5))

    return NODES, TEXTS, T_CIRCLES

def writePlotFiles(NODES, TEXTS, T_CIRCLES, spe_matrix, bName):
    with open(os.path.join(cwl, 'nodes'), 'w') as f:
        for elem in NODES:
            f.write(str(NODES[elem][0])+' '+str(NODES[elem][1])+' '+'5'+'\n')
    with open(os.path.join(cwl, 'texts'), 'w') as f:
        cy = []
        for i, elem in enumerate(TEXTS):
            name_lookup = bName[elem]['Name']
            f.write('set label '+str(i+1)+' "'+str(name_lookup)+'" at '+str(TEXTS[elem][0]-5)+', '+str(TEXTS[elem][1])+',0 left norotate back nopoint offset character 0, 0, 0\n')
            cy.append('set label '+str(i+1)+' "'+str(name_lookup)+'" at '+str(TEXTS[elem][0]-5)+', '+str(TEXTS[elem][1])+',0 left norotate back nopoint offset character 0, 0, 0')
        for i, elem in enumerate(NODES):
            f.write('set label '+str(len(TEXTS)+i+1)+' "'+str(elem)+'" at '+str(NODES[elem][0]-5)+', '+str(NODES[elem][1])+',0 left norotate back nopoint offset character 0, 0, 0\n')
            cy.append('set label '+str(len(TEXTS)+i+1)+' "'+str(elem)+'" at '+str(NODES[elem][0]-5)+', '+str(NODES[elem][1])+',0 left norotate back nopoint offset character 0, 0, 0')
    with open(os.path.join(cwl, 'circle'), 'w') as f:
        for elem in T_CIRCLES:
            f.write(str(T_CIRCLES[elem][0])+' '+str(T_CIRCLES[elem][1])+' '+str(T_CIRCLES[elem][2])+'\n')
    with open(os.path.join(cwl, 'lines'), 'w') as f:
        for elem in spe_matrix:
            for conn in spe_matrix[elem]:
                f.write(str(T_CIRCLES[elem][0]-5)+' '+str(T_CIRCLES[elem][1])+' '+str(NODES[conn][0])+' '+str(NODES[conn][1])+'\n')
    #Writing plotter.plg
    PLG=['set datafile separator " "',
         'set grid',
         'unset key',
         'set terminal png size 2800,1080 enhanced background rgb "white"',
         'set term png transparent truecolor',
         'set style fill transparent solid 0.15 noborder',
         'set output "out.png"',
         'if (!exists("filename")) filename="default.dat"',
         ]
    with open(os.path.join(cwl, 'auto_plotter.plg'), 'w') as f:
        for line in PLG:
            f.write(line+'\n')
        for line in cy:
            f.write(line+'\n')
        f.write("plot '"+str(os.path.join(cwl, 'lines'))+"' u 1:2:($3-$1):($4-$2) w vectors nohead lc \"grey\" lw 0.25"+", '"+str(os.path.join(cwl, 'nodes'))+"' u 1:2:3 w circle, '"+str(os.path.join(cwl, 'circle'))+"' u 1:2:3 w circle")
    drawHalfViz(spe_matrix, bName)

def drawPlot():
    if sys.platform == 'win32':
        command = '\"C:\\Program Files\\gnuplot\\bin\\gnuplot.exe\" -e \"filename=\'lines\'\" auto_plotter.plg'
        p = subprocess.Popen(command, shell=True)
        selDList, errval = p.communicate()
    elif sys.platform == 'linux':
        command = 'gnuplot -e "filename=\'lines\'" auto_plotter.plg'
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        selDList, errval = p.communicate()

def loadHalfviz(strg):
    cwl = os.getcwd()
    driverpath = str(os.path.join(cwl, 'geckodriver'))
    cap = {"marionette": True}
    driver = utils.loadUrl(driverpath, cap, 'http://arborjs.org/halfviz/')
    driver.find_element_by_id("code").clear()
    driver.find_element_by_id("code").send_keys(strg)
    print("Data loaded into half-viz... Waiting. To save the image right-click and click save-image...")


def drawHalfViz(matrix, bname):
    colorSet = ['#EA961C', '#2D9F89', '#69C60C', '#3A2261', '#AD062A', '#6B9B9B', '#C5C8C8', '#F41907', '#6100FF', '#289A72']
    colored = []
    strg = ''
    with open(os.path.join(cwl, 'halfviz'), 'w') as f:
        for element in matrix:
            color = colorSet[random.randint(0, len(colorSet)-1)]
            #Setting keynode
            for key in matrix[element]:
                name = bname[element]['Name']
                f.write(str(name)+'->'+str(key)+' {length: '+str(len(matrix[element])**2)+'}\n')
                strg = strg+' '+str(name)+'->'+str(key)+' {length: '+str(len(matrix[element])**2)+'}\n'
                strg = strg+' '+str(name)+' {color: black}\n'
                if key not in colored:
                    f.write(str(key)+' {shape: dot, color: '+str(color)+'}\n')
                    strg = strg+' '+str(key)+' {shape: dot, color: '+str(color)+'}\n'
                    colored.append(key)
    loadHalfviz(strg)

if __name__=="__main__":
    pass
