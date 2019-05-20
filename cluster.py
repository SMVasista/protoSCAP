from __future__ import division
import sys, os, re, pickle
import xlsxwriter
import sunflower_plotter as sp
import datetime
import math

cwl = os.getcwd()

def identifyClusters(bdata, idata, matrix, dmatrix, rmode):
    #A cluster is any group with atleast one common feature and N>=3

    features = matrix.keys()
    age = features.pop(features.index('Age'))
    conn = features.pop(features.index('Conn'))
    des = features.pop(features.index('Designation-Level'))
    #Age and Location will be non-zero elements and used for final groupings

    #Identifying Clusters
    elements = matrix[features[0]].keys()
    
    L1 = {}
    for feat in features:
        L1[feat] = []
        for elem in elements:
            if matrix[feat][elem] > 0:
                L1[feat].append(elem)

    L2 = {}
    for feat1 in features:
        for feat2 in features:
            if feat1 != feat2 and str(feat2)+'_+_'+str(feat1) not in L2:
                label = str(feat1)+'_+_'+str(feat2)
                L2[label] = []
                for elem in elements:
                    if matrix[feat1][elem] > 0 and matrix[feat2][elem] > 0:
                        try:
                            L2[label].append(elem)
                            for label in L1:
                                if elem in L1[label]:
                                    L1[label].pop(L1[label].index(elem))
                        except:
                            #print "label error"
                            pass
    L3 = {}
    for feat1 in features:
        for feat2 in features:
            for feat3 in features:
                if feat1 != feat2 != feat3:
                    cLabel = str(feat1)+'_+_'+str(feat2)+'_+_'+str(feat3)
                    L3[cLabel] = []
                    H1 = str(feat1)+'_+_'+str(feat2) if str(feat1)+'_+_'+str(feat2) in L2.keys() else str(feat2)+'_+_'+str(feat1)
                    H2 = str(feat2)+'_+_'+str(feat3) if str(feat2)+'_+_'+str(feat3) in L2.keys() else str(feat3)+'_+_'+str(feat2)
                    H3 = str(feat3)+'_+_'+str(feat1) if str(feat3)+'_+_'+str(feat1) in L2.keys() else str(feat1)+'_+_'+str(feat3)
                    if H1 != H2 != H3:
                        if len(L2[H1]) != 0 and len(L2[H2]) != 0:
                            for elem in L2[H1]+L2[H2]:
                                if elem in L2[H1] and elem in L2[H2]:
                                    L3[cLabel].append(elem)
                                    L2[H1].pop(L2[H1].index(elem))
                                    L2[H2].pop(L2[H2].index(elem))

                        if len(L2[H2]) != 0 and len(L2[H3]) != 0:
                            for elem in L2[H2]+L2[H3]:
                                if elem in L2[H1] and elem in L2[H2]:
                                    L3[cLabel].append(elem)
                                    L2[H2].pop(L2[H2].index(elem))
                                    L2[H3].pop(L2[H3].index(elem))

                        if len(L2[H3]) != 0 and len(L2[H1]) != 0:
                            for elem in L2[H3]+L2[H1]:
                                if elem in L2[H3] and elem in L2[H1]:
                                    L3[cLabel].append(elem)
                                    L2[H3].pop(L2[H3].index(elem))
                                    L2[H1].pop(L2[H1].index(elem))

    delete_val = []
    for element in L1:
        if len(L1[element]) < 1:
            delete_val.append(element)
    for element in delete_val:
        del L1[element]

    delete_val = []
    for element in L2:
        if len(L2[element]) < 1:
            delete_val.append(element)
    for element in delete_val:
        del L2[element]

    delete_val = []
    for element in L3:
        if len(L3[element]) < 1:
            delete_val.append(element)
    for element in delete_val:
        del L3[element]

    #Identifying groups
    G = {'Age_Group': {'age_group_1_(young)': [], 'age_group_2(mid-30)': [], 'age_group_1(35+)': []},
         'Designation_Group': {'level1(basic)': [], 'level2(intermediate)': [], 'level3(managerial)': [], 'level4(TopLevel)': []},
         'Connectedness_group': {'conn1(low)': [], 'conn2(med-low)': [], 'conn3(moderately_connected)': [], 'conn4(Highly_connected)': []}}

    for elem in elements:
        if matrix['Age'][elem] < 23:
            G['Age_Group']['age_group_1_(young)'].append(elem)
        elif 23 < matrix['Age'][elem] < 35:
            G['Age_Group']['age_group_2(mid-30)'].append(elem)
        elif matrix['Age'][elem] > 35:
            G['Age_Group']['age_group_1(35+)'].append(elem)
        else:
            continue

        if matrix['Designation-Level'][elem] == 3:
            G['Designation_Group']['level4(TopLevel)'].append(elem)
        elif matrix['Designation-Level'][elem] == 2:
            G['Designation_Group']['level3(managerial)'].append(elem)
        elif matrix['Designation-Level'][elem] == 1:
            G['Designation_Group']['level2(intermediate)'].append(elem)
        elif matrix['Designation-Level'][elem] == 0.5:
            G['Designation_Group']['level1(basic)'].append(elem)
        else:
            continue


        if 0.0001 < matrix['Conn'][elem] < 0.1:
            G['Connectedness_group']['conn1(low)'].append(elem)
        elif 0.11 < matrix['Conn'][elem] < 0.4:
            G['Connectedness_group']['conn2(med-low)'].append(elem)
        elif 0.41 < matrix['Conn'][elem] < 0.8:
            G['Connectedness_group']['conn3(moderately_connected)'].append(elem)
        elif matrix['Conn'][elem] > 0.8:
            G['Connectedness_group']['conn4(Highly_connected)'].append(elem)
        else:
            continue

    D = {}
    for elem1 in dmatrix:
        for elem2 in dmatrix:
            loc_val = dmatrix[elem1][elem2]
            if loc_val != 0:
                if loc_val not in D:
                    D[loc_val] = []
                    D[loc_val].append(elem1)
                    D[loc_val].append(elem2)
                else:
                    if elem1 not in D[loc_val]:
                        D[loc_val].append(elem1)
                    if elem2 not in D[loc_val]:
                        D[loc_val].append(elem2)
    for element in D.keys():
        D[element] = list(set(D[element]))

    clusterSet = (L1, L2, L3, G, D)

    with open(os.path.join(cwl, 'clusterset.p'), 'w') as f:
        pickle.dump(clusterSet, f)

    if rmode == 'ON':
        d = datetime.date.today()
        outLoc = os.path.join(cwl, 'clustering_report_'+str(d.year)+str(d.month)+str(d.day)+'.xlsx')
        writeReports(bdata, idata, clusterSet, outLoc)

    return clusterSet

def writeReports(bdata, idata, clusterSet, outFile):
    
    workbook = xlsxwriter.Workbook(outFile)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': '$#,##0'})

    #Adding clusters-worksheet
    ws = workbook.add_worksheet('Plots|Summary')
    ws.write('A1', 'Plots - Clusters identified from scraped nodes (profiles)', bold)
    row = 3
    col = 0

    ws.write('A3', 'Interests', bold)
    #Passing data to plotter and fetching image
    U = clusterSet[0]
    U.update(clusterSet[1])
    U.update(clusterSet[2])
    try:
        A, B, C, D, E = sp.parseConnectors(U)
        X, Y, Z = sp.computeNodesAndCord(A, B, C, D, E)
        sp.writePlotFiles(X, Y, Z, E, bdata)
        sp.drawPlot()
        try:
            os.rename('halfviz', 'Interests.viz')
            os.rename('out.png', 'Interests.png')
        except:
            os.remove('Interests.png')
            os.remove('Interests.viz')
            os.rename('out.png', 'Interests.png')
            os.rename('halfviz', 'Interests.viz')
        ws.insert_image('B3', 'Interests.png')
    except:
        pass

    ws.write('A60', 'Location', bold)
    try:
        A, B, C, D, E = sp.parseConnectors(clusterSet[4])
        X, Y, Z = sp.computeNodesAndCord(A, B, C, D, E)
        sp.writePlotFiles(X, Y, Z, E, bdata)
        sp.drawPlot()
        try:
            os.rename('out.png', 'Location.png')
            os.rename('halfviz', 'Location.viz')
        except:
            os.remove('Location.png')
            os.remove('Location.viz')
            os.rename('out.png', 'Location.png')
            os.rename('halfviz', 'Location.viz')
        ws.insert_image('B61', 'Location.png')
    except:
        pass

    ws.write('A120', 'Groups', bold)
    B = clusterSet[3]['Age_Group']
    for elem in clusterSet[3]:
        B.update(clusterSet[3][elem])
    try:
        A, B, C, D, E = sp.parseConnectors(B)
        X, Y, Z = sp.computeNodesAndCord(A, B, C, D, E)
        sp.writePlotFiles(X, Y, Z, E, bdata)
        sp.drawPlot()
        try:
            os.rename('out.png', 'Groups.png')
            os.rename('halfviz', 'Groups.viz')
        except:
            os.remove('Groups.viz')
            os.remove('Groups.png')
            os.rename('out.png', 'Groups.png')
            os.rename('halfviz', 'Groups.viz')
        ws.insert_image('B121', 'Groups.png')
    except:
        pass

    ws = workbook.add_worksheet('Clusters')
    ws.write('A1', 'Clusters identified from scraped nodes (profiles) - Interests', bold) 
    row = 3
    col = 0
    
    #Writing clusters
    for element in clusterSet[0]:
        L = clusterSet[0][element]
        ws.write(row, col, str(element), bold)
        row += 1
        for entry in L:
            name_lookup = bdata[entry]['Name']
            ws.write(row, col+1, str(name_lookup)+' ('+str(entry)+')')
            row += 1
        row += 1
    row += 1

    for element in clusterSet[1]:
        L = clusterSet[1][element]
        ws.write(row, col, str(element.replace('_+_', ' & ')), bold)
        row += 1
        for entry in L:
            name_lookup = bdata[entry]['Name']
            ws.write(row, col+1, str(name_lookup)+' ('+str(entry)+')')
            row += 1
        row += 1
    row += 1

    for element in clusterSet[2]:
        L = clusterSet[2][element]
        ws.write(row, col, str(element.replace('_+_', ' & ')), bold)
        row += 1
        for entry in L:
            name_lookup = bdata[entry]['Name']
            ws.write(row, col+1, str(name_lookup)+' ('+str(entry)+')')
            row += 1
        row += 1
    row += 1

    #writing groups
    ws = workbook.add_worksheet('Groups')
    ws.write('A1', 'Scraped nodes (profiles) grouped based on specific criteria', bold) 

    row = 3
    col = 0

    for element in clusterSet[3]:
        L = clusterSet[3][element]
        ws.write(row, col, str(element), bold)
        row += 1
        for J in L.keys():
            ws.write(row, col+1, str(J))
            row += 1
            for entry in L[J]:
                name_lookup = bdata[entry]['Name']
                ws.write(row, col+2, str(name_lookup)+' ('+str(entry)+')')
                row += 1
            row += 1
        row += 1
    row += 1

    ws.write(row, col, 'Geographical-Location', bold)
    row += 1
    for element in clusterSet[4]:
        L = clusterSet[4][element]
        ws.write(row, col+1, str(element), bold)
        row += 1
        for entry in L:
            name_lookup = bdata[entry]['Name']
            ws.write(row, col+2, str(name_lookup)+' ('+str(entry)+')')
            row += 1
        row += 1
    row += 1


    workbook.close()
                
if __name__=="__main__":
    pass
