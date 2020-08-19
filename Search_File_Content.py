import os
import pandas as pd
import re
import random
#                   Need the DataFrame from main.py as first_patch and the Extraction from Modify_Packages

first_patch = pd.read_excel(r'E:\Coding 1 Project\Pycharm 101\content-pyppepeer.xlsx')

filedir= r'E:\Coding 1 Project\Pycharm 101\.\pyppeteer\pyppeteer' # equal Extraction (path) as global varible (Copies Files)
class Searching:
    def __init__(self, FirstHalfTable, AllPyContainer):
        self.dataFrame = FirstHalfTable
        self.link_to_folder = AllPyContainer

    def Search_Content(self):
        con = self.dataFrame['Filename'].values.tolist()
        con = [x[:x.rfind('.')] for x in con]
        second_patch = pd.DataFrame(
            columns=('Filename', 'Inner Module', 'Outer Module', 'Inner Attribute', 'Outer Attribute'))

        second_patch.Filename = con
        os.chdir(self.link_to_folder)
        container = list()
        for e, file in enumerate(con):  # replace with list of filesname no py (Global variable from main)
            f = open(file=os.path.join(self.link_to_folder, file), mode='r')
            get = re.findall(r'from\s*([.\w]+)\s*import\s*([.\w]+)\s*|import\s*([.\w]+)\s*',
                             f.read())  # from *import or import
            container.append([file, get])  # from Module import Attribute
            # import Module
        return container, second_patch

    def Unpack(self):
        container, second_patch = self.Search_Content()
        network_from = list()
        network_to = list()
        second_patch = second_patch.set_index('Filename')
        for nesting_list in container:  # nesting_list contains Filename[0] and list of tup[1]-[(mod,attr,attr)...]
            inner_module = []
            outer_module = []
            inner_attribute = []
            outer_attribute = []

            for tup in nesting_list[1]:
                if tup[0] != '':  # Module
                    if 'pyppeteer' in tup[0]:  # get the folder name "pyppeteer" from extraction
                        network_from.append(tup[0][tup[0].rfind('.') + 1:])
                        network_to.append(nesting_list[0])
                        inner_module.append(tup[0])
                    else:
                        network_from.append(tup[0])
                        network_to.append(nesting_list[0])
                        outer_module.append(tup[0])
                if tup[1] != '':  # Attribute
                    if 'pyppeteer' in tup[1]:
                        inner_attribute.append(tup[1])
                    else:
                        outer_attribute.append(tup[1])
                if tup[2] != '':  # Module
                    if 'pyppeteer' in tup[2]:
                        network_from.append(tup[2][tup[2].rfind('.') + 1:])
                        network_to.append(nesting_list[0])
                        inner_module.append(tup[2])
                    else:
                        network_from.append(tup[2])
                        network_to.append(nesting_list[0])
                        outer_module.append(tup[2])

            second_patch.loc[nesting_list[0], 'Inner Module'] = ','.join(inner_module)
            second_patch.loc[nesting_list[0], 'Inner Attribute'] = ','.join(inner_attribute)
            second_patch.loc[nesting_list[0], 'Outer Module'] = ','.join(outer_module)
            second_patch.loc[nesting_list[0], 'Outer Attribute'] = ','.join(outer_attribute)

        #                                    Testing properties
        #     print(type(','.join(module)))
        #     print(type(','.join(attribute)))
        #     print(type(module))
        #     print(type(attribute))
        return second_patch, network_from, network_to

    def Merging(self):
        second_patch, network_from, network_to = self.Unpack()
        second_patch = second_patch.reset_index()
        second_patch.Filename = [''.join([x, '.py']) for x in second_patch['Filename'].values.tolist()]
        #print(self.dataFrame)
        #print(second_patch)
        com_list = second_patch.merge(self.dataFrame, how='inner', left_on='Filename', right_on='Filename')
        #print(com_list)
        #print(com_list.iloc[random.randrange(start=0, stop=1, step=1)])
        os.chdir(r'E:\Coding 1 Project\Pycharm 101')
        # com_list.to_excel('checkthis.xlsx')
        # print(set(zip(network_from,network_to)))

        df = pd.DataFrame({'from': [x[0] for x in set(zip(network_from, network_to))],
                           'to': [x[1] for x in set(zip(network_from, network_to))]})
        df.to_excel('network.xlsx')



#Merging(dataFrame=first_patch,link_to_folder=filedir)
Test1 = Searching(FirstHalfTable=first_patch,AllPyContainer=filedir)
Test1.Merging()








