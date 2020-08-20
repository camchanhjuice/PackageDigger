import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from Search_File_Content import Searching, first_patch, filedir

class Plotting:
    def __init__(self,Network, DataFrame,Choosen_Module = None):
        self.network = Network
        self.dataframe = DataFrame
        self.Filename = self.dataframe['Filename'].values.tolist()
        self.Module = Choosen_Module


    def networking(self):
        weight = list()
        nopy = [x[:x.rfind('.py')] for x in self.Filename]
        for x in self.network['from'].values.tolist():
            if x in nopy:
                weight.append(3)
            else:
                weight.append(0.1)

        self.network['weight'] =weight
        if self.Module and self.Module in nopy:
            df = self.network[self.network.to == self.Module] #Single Module
        elif self.Module == 'OnlyMain':
            df = self.network.iloc[[x for x in range(len(self.network))
                                     if self.network.iloc[x]['from'] in nopy],:]  # Main Module in Packages
        else:
            df= self.network


        G = nx.from_pandas_edgelist(df=df, source='from',target = 'to', edge_attr='weight')
        # Plot it
        nx.draw(G, with_labels=True,node_size=150, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=10)
        plt.show()

Test1 = Searching(FirstHalfTable=first_patch,AllPyContainer=filedir)
table, nw = Test1.Merging()
test2 = Plotting(Network=nw, DataFrame=table, Choosen_Module='OnlyMain')
test2.networking()

