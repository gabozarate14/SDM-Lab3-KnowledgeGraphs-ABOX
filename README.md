# Semantic Data Management
## Knowledge Graph Lab 3

### ABOX Graph generation


The following project contains three files:
- [11G-B2-CampeniZarate-generateData.py](11G-B2-CampeniZarate-generateData.py): Generates the data for some relations needed to create the graph ABOX
- [11G-B2-CampeniZarate-ABOX.py](11G-B2-CampeniZarate-ABOX.py): Uses the library `rdflib` to create the ABOX graph, reading the files from `data`
- [11G-B3-CampeniZarate-ABOX.py](11G-B3-CampeniZarate-ABOX.py): Uses the library `rdflib` to create the ABOX graph, reading the files from `data`, but adds the `rdfs:type` relation to link the ABOX with the TBOX

The generated graphs are exported to the [graph](graph) folder, that includes:

- [B2_abox.ttl](graph%2FB2_abox.ttl): ABOX graph from B2
- [B3_abox.ttl](graph%2FB3_abox.ttl): ABOX graph from B3, includes the `rdfs:type` relation and is the one that is uploaded

### Uploading the TBOX & ABOX graph

Then the graph is uploaded to a GraphDB leaving this structure:

#### Class hierarchy:

![class_h.png](images%2Fclass_h.png)


#### Class relations:

![class_r.png](images%2Fclass_r.png)