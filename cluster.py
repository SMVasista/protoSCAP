from __future__ import division
import sys, os, re
import math

def identifyClusters(matrix, dmatrix):
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
                            print "label error"
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

    #Identifying groups
    G = {'Age_Group': {'ag1': [], 'ag2': [], 'ag3': []}, 'Des_Group': {'h1': [], 'h2': [], 'h3': [], 'h4': []}, 'Conn_group': {'c1': [], 'c2': [], 'c3': [], 'c4': []}}

    for elem in elements:
        if matrix['Age'][elem] < 23:
            G['Age_Group']['ag1'].append(elem)
        elif 23 < matrix['Age'][elem] < 35:
            G['Age_Group']['ag2'].append(elem)
        elif matrix['Age'][elem] > 35:
            G['Age_Group']['ag3'].append(elem)
        else:
            continue

        if matrix['Designation-Level'][elem] == 3:
            G['Des_Group']['h4'].append(elem)
        elif matrix['Designation-Level'][elem] == 2:
            G['Des_Group']['h3'].append(elem)
        elif matrix['Designation-Level'][elem] == 1:
            G['Des_Group']['h2'].append(elem)
        elif matrix['Designation-Level'][elem] == 0.5:
            G['Des_Group']['h1'].append(elem)
        else:
            continue

        if 0.0001 < matrix['Conn'][elem] < 0.1:
            G['Conn_group']['c1'].append(elem)
        elif 0.11 < matrix['Conn'][elem] < 0.4:
            G['Conn_group']['c2'].append(elem)
        elif 0.41 < matrix['Conn'][elem] < 0.8:
            G['Conn_group']['c3'].append(elem)
        elif matrix['Conn'][elem] > 0.8:
            G['Conn_group']['c4'].append(elem)
        else:
            continue

    for key in G:
        print key
        for elem in G[key]:
            print elem, G[key][elem]
    return (L1, L2, L3)

    

                
if __name__=="__main__":
    pass
