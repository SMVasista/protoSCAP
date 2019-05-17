from __future__ import division
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import parameters

interests_block = ['IT-Software',
                   'Marketing',
                   'Social-Media',
                   'Sports-Games',
                   'Cars-Automobiles',
                   'AI-Automation',
                   'Pharmaceuticals',
                   'Agriculture',
                   'Business-Financials',
                   'Entrepreneurship',
                   'Politics',
                   'Entertainment-Products'
                   ]

economic_block = {'US': 5,
                  'Japan': 5,
                  'Canada': 5,
                  'China': 4,
                  'India': 3,
                  'UK': 3.5,
                  'France': 3.5,
                  'Germany': 4,
                  'Egypt': 2,
                  'Brazil': 2.5,
                  'South Africa': 2.5,
                  'Korea': 3.5
                  }

map_influencers = {'Elon Musk': ['Cars-Automobiles', 'AI-Automation'],
    'Satya Nadella': ['IT-Software'],
    'Bill Gates': ['IT-Software', 'Social-Media'],
    'Kiran Mazumdar Shaw': ['Pharmaceuticals', 'Entrepreneurship'],
    'Sramana Mitra': ['Entrepreneurship', 'Social-Media'],
    'Warren Buffet': ['Business-Financials'],
    'Richard Branson': ['Social-Media', 'Entrepreneurship'],
    'Jessica Alba': ['Entertainment-Products', 'Entrepreneurship'],
    'Jeff Bezos': ['Marketing', 'IT-Software'],
    'Mark Cuban': [],
    'James Altucher': [],
    'Mohamed El-Erian': [],
    'Sallie Krewcheck': [],
    'Ian Bremmer': [],
    'Jill Schlesinger': [],
    'Ryan Holmes': [],
    'Donald Trump': ['Politics', 'Entertainment-Products'],
    'Justin Trudeau': ['Politics'],
    'Narendra Modi': ['Politics']
    }
map_companies = {'IBM': ['IT-Software', 'AI-Automation'],
    'Hewlett-Packard': ['IT-Software'],
    'Microsoft': ['IT-Software'],
    'Accenture': ['Marketing', 'IT-Software'],
    'Google': ['IT-Software', 'Social-Media', 'AI-Automation'],
    'Oracle': ['Social-Media'],
    'Deloitte': ['Marketing', 'IT-Software'],
    'Apple': ['IT-Software'],
    'Cisco': ['Marketing', 'IT-Software'],
    'Electronic Arts': ['Sports-Games', 'Entertainment-Products'],
    'BMW Group': ['Cars-Automobiles'],
    'Ferrari': ['Cars-Automobiles'],
    'BCCI': ['Sports-Games'],
    'National Football League': ['Sports-Games'],
    'Cellworks Life': ['Pharmaceuticals'],
    'Biocon': ['Pharmaceuticals'],
    'Khan Academy': ['Social-Media'],
    'Sony': ['Sports-Games', 'Entertainment-Products'],
    'Uber': ['Cars-Automobiles', 'Social-Media', 'Marketing'],
    'PopCap': ['Sports-Games', 'Entertainment-Products'],
    'Ubisoft': ['Sports-Games', 'Entertainment-Products'],
    'Tesla': ['Cars-Automobiles', 'AI-Automation'],
    'SpaceX': ['Cars-Automobiles', 'AI-Automation'],
    'Netflix': ['Entertainment-Products'],
    'Facebook': ['Social-Media', 'Marketing'],
    'Twitter': ['Social-Media', 'Marketing'],
    'Novartis': ['Pharmaceuticals'],
    'Nike': ['Sports-Games'],
    'Sal Agrotech': ['Agriculture'],
    'Monsanto': ['Agriculture']
    }

def parse_basic_details(profile):
    C_PROFILE = {}

    #Cleaning Up details from profile
    C_PROFILE['Name'] = str(profile['Name'].encode('utf-8', 'ignore').decode('utf-8'))
    C_PROFILE['College'] = str(profile['College'].encode('utf-8', 'ignore').decode('utf-8'))

    #Identifying employment-designation level
    C_PROFILE['Company'] = str(profile['Company'].encode('utf-8', 'ignore').decode('utf-8'))
    J = profile['Job Title'].split(' at ')[0].encode('utf-8', 'ignore').decode('utf-8')
    C_PROFILE['Job-Title'] = str(J)

    if 'Founder' in C_PROFILE['Job-Title'] or 'Chief' in C_PROFILE['Job-Title'] or 'Head' in C_PROFILE['Job-Title'] :
        C_PROFILE['Designation-Level'] = 3
    elif 'Manager' in C_PROFILE['Job-Title'] or 'Lead' in C_PROFILE['Job-Title'] or 'Senior' in C_PROFILE['Job-Title'] or 'Scientist' in C_PROFILE['Job-Title']:
        C_PROFILE['Designation-Level'] = 2
    elif 'Consultant' in C_PROFILE['Job-Title'] or 'Associate' in C_PROFILE['Job-Title'] or 'Freelancer' in C_PROFILE['Job-Title']:
        C_PROFILE['Designation-Level'] = 0.5
    elif 'Employee' in C_PROFILE['Job-Title'] or 'Self' in C_PROFILE['Job-Title']:
        C_PROFILE['Designation-Level'] = 1
    else:
        C_PROFILE['Designation-Level'] = 0.005

    #Identifying geographical locations
    C_PROFILE['Location'] = []
    for element in profile['Location'].split(','):
        C_PROFILE['Location'].append(str(element).replace(' ', ''))

    #Identifying connectedness
    if profile['N_Connections'] != 'NR':
        C_PROFILE['Conn'] = int(profile['N_Connections'])/500
    else:
        C_PROFILE['Conn'] = 0.0001

    return C_PROFILE

def parse_interests_details(profile):
    #Removing Age-group details
    for element in profile:
        if type(element) == tuple:
           _age = profile.pop(profile.index(element))
    
    I_PROFILE = {}
    for element in interests_block:
        I_PROFILE[element] = 0

    try:
        I_PROFILE['Age'] = int(_age[1])
    except:
        I_PROFILE['Age'] = 27

    #Identifying general keywords
    for element in profile:
        if "social" in element.lower():
            I_PROFILE['Social-Media'] += 1

        if "marketing" in element.lower():
            I_PROFILE['Marketing'] += 1

        if "pharma" in element.lower():
            I_PROFILE['Pharmaceuticals'] += 1

        if "design" in element.lower():
            I_PROFILE['Social-Media'] += 1

        if "business" in element.lower() or "finance" in element.lower():
            I_PROFILE['Business-Financials'] += 1

        if "start-up" in element.lower() or "startup" in element.lower() or "enterpreneur" in element.lower():
            I_PROFILE['Entrepreneurship'] += 1

        if "movie" in element.lower() or "film" in element.lower() or "entertainment" in element.lower() or "theatre" in element.lower():
            I_PROFILE['Entertainment-Products'] += 1

        if "sport" in element.lower() or "games" in element.lower() or "football" in element.lower() or "cricket" in element.lower() or "tennis" in element.lower():
            I_PROFILE['Sports-Games'] += 1

        if "ai" in element.lower() or "machine learning" in element.lower() or "analytics" in element.lower():
            I_PROFILE['AI-Automation'] += 1

        if "car" in element.lower() or "bike" in element.lower() or "automob" in element.lower():
            I_PROFILE['Cars-Automobiles'] += 1

    #Identifying specific keywords
    for element in map_influencers.keys():
        if element in profile:
            for feature in map_influencers[element]:
                I_PROFILE[feature] += 1

    for element in map_companies.keys():
        if element in profile:
            for feature in map_companies[element]:
                I_PROFILE[feature] += 1

    return I_PROFILE

def generate_vo_matrix(b_profile, i_profile):
    B = b_profile
    I = i_profile

    desc1 = ['IT-Software',
            'Marketing',
            'Social-Media',
            'Sports-Games',
            'Cars-Automobiles',
            'AI-Automation',
            'Pharmaceuticals',
            'Agriculture',
            'Business-Financials',
            'Entrepreneurship',
            'Politics',
            'Entertainment-Products',
            'Age'
            ]

    desc2 = ['Designation-Level',
             'Conn'
             ]

    sample = B.keys()

    #Creating a FeatureXSample matrix for computing relative-distances
    Mx = {}
    for feature in desc1:
        Mx[feature] = {}
        for node in sample:
            Mx[feature][node] = I[node][feature]

    for feature in desc2:
        Mx[feature] = {}
        for node in sample:
            Mx[feature][node] = B[node][feature]

    Dmx = {}
    for node1 in sample:
        if node1 not in Dmx.keys():
            Dmx[node1] = {}
        for node2 in sample:
            if node1 != node2:
                if node2 not in Dmx[node1].keys():
                    Dmx[node1][node2] = 0
                    for elem1 in B[node1]['Location']:
                        for elem2 in B[node2]['Location']:
                            if elem1 == elem2:
                                Dmx[node1][node2] = 1

    return Mx, Dmx


if __name__=="__main__":
    pass
