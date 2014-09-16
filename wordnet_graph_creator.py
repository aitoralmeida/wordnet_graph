# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 15:25:19 2014

@author: aitor
"""


import networkx as nx
from nltk.corpus import wordnet

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