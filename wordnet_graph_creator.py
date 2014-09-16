# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 15:25:19 2014

@author: aitor
"""


import networkx as nx
from nltk.corpus import wordnet


def build_graphs():
    print "Recovering synsets..."
    syns = list(wordnet.all_synsets())
    total_syns = len(syns)
    print "Total synsets: " + str(total_syns)
    
    G_hypo = nx.DiGraph()
    G_mero = nx.Graph()
    G_holo = nx.DiGraph()
    G_complete = nx.Graph()

    
    print "Building graph..."
    for i, syn in enumerate(syns):
        if i % 100 == 0:
            print str(i) + " of " + str(total_syns)
            
        base_syn = syn.name
    
        #Hyponyms      
        hypos = [h.name for h in syn.hyponyms()]
        for hypo_syn in hypos:
            G_hypo.add_edge(base_syn, hypo_syn)
            G_complete.add_edge(base_syn, hypo_syn)
        
        #Hyperonyms        
    #    hypers = [h.name for h in syn.hypernyms()]        
    #    for hyper_syn in hypers:
    #        if not G.has_edge(hyper_syn, base_syn):
    #            G.add_edge(hyper_syn, base_syn)
    
        #Meronyms
        meros = [m.name for m in syn.member_meronyms()]
        for mero_syn in meros:
            G_mero.add_edge(base_syn, mero_syn)
            G_complete.add_edge(base_syn, mero_syn)
            
        #holonyms
        holos = [m.name for m in syn.member_holonyms()]
        for holo_syn in holos:
            G_holo.add_edge(base_syn, holo_syn)
            G_complete.add_edge(base_syn, holo_syn)
 
    
    return G_hypo, G_mero, G_holo, G_complete
    
def write_graphs(G_hypo, G_mero, G_holo, G_complete):
    print "Writing graphs..."
    print "  - hyponyms"            
    nx.write_gexf(G_hypo, 'wordnet_hyponyms.gexf')
    print "  - meronyms"  
    nx.write_gexf(G_mero, 'wordnet_meronyms.gexf')
    print "  - holonyms"  
    nx.write_gexf(G_holo, 'wordnet_holonyms.gexf')
    print "  - complete"  
    nx.write_gexf(G_complete, 'wordnet_complete.gexf')
    print "...done"
    
    
def get_statistics(G):
    
    centralities = {}
    centralities['eigenvector'] = nx.eigenvector_centrality(G)
    centralities['degree'] = nx.degree_centrality(G)
    centralities['betweenness'] = nx.betweenness_centrality(G)
    centralities['closeness'] = nx.closeness_centrality(G)
    
    for cent in centralities:
        values = centralities[cent]
        for node in values:
            G.node[node][cent] = values[node]
            
    return G
    
if __name__=='__main__':
    G_hypo, G_mero, G_holo, G_complete = build_graphs()
    G_hypo = get_statistics(G_hypo)
    G_mero = get_statistics(G_mero)
    G_holo = get_statistics(G_holo)
    G_complete = get_statistics(G_complete)
    write_graphs(G_hypo, G_mero, G_holo, G_complete)
    
    
    