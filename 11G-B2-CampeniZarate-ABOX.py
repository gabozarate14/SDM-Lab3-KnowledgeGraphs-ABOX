import pandas as pd
import re
from rdflib import Graph, Namespace, Literal, URIRef
from unidecode import unidecode
from rdflib.namespace import RDF, RDFS, XSD

PAPERS_SOURCE = 'data/papers.csv'
AUTHORS_SOURCE = 'data/authors.csv'
WRITES_SOURCE = 'data/writes.csv'
CONFERENCES_SOURCE = 'data/conference.csv'
JOURNAL_SOURCE = 'data/journal.csv'
VOLUME_SOURCE = 'data/volume.csv'
PROCEEDING_SOURCE = 'data/proceeding.csv'
EDITION_SOURCE = 'data/edition.csv'
PUBLICATION_SOURCE = 'data/publication.csv'
PUBLISHES_SOURCE = 'data/publishes.csv'
PRESENTED_SOURCE = 'data/presented.csv'
REVIEWS_SOURCE = 'data/review_evolved.csv'
BELONGS_TO_CONFERENCE = 'data/belongs_to_conference.csv'
BELONGS_TO_JOURNAL = 'data/belongs_to_journal.csv'
CHAIR_DESIGNATES_SOURCE = 'data/chair_designates.csv'
EDITOR_DESIGNATES_SOURCE = 'data/editor_designates.csv'
AREA_SOURCE = 'data/area.csv'
RELATED_TO_SOURCE = 'data/related_to.csv'
PAPER_ACCEPTED_SOURCE = 'data/paper_accepted.csv'


def clean_uri(text):
    reserved_chars_pattern = r'[:/¿?#\[\]@!$&\'()*+,;=."]'
    clean_text = re.sub(r"\s+", "_", unidecode(text).strip())
    return re.sub(reserved_chars_pattern, "", clean_text)


g = Graph()
mainURI = "http://www.semanticweb.org/eloic/ontologies/2023/4/untitled-ontology-4/"
ns = Namespace(mainURI)

# ABOX

# Load :author
authors = pd.read_csv(AUTHORS_SOURCE)
for _, row in authors.iterrows():
    node = clean_uri(row["author"])
    g.add((ns[node], ns.name, Literal(row["author"])))

# Load :paper
papers = pd.read_csv(PAPERS_SOURCE)
for _, row in papers.iterrows():
    node = clean_uri(row["title"])
    node_type = clean_uri(row["type"])
    g.add((ns[node], ns.title, Literal(row["title"])))

# Load :authorship
authorships = pd.read_csv(WRITES_SOURCE)
for _, row in authorships.iterrows():
    paper_node = URIRef(mainURI+clean_uri(row["title"]))
    author_node = URIRef(mainURI+clean_uri(row["author"]))
    g.add((author_node, ns.authorship, paper_node))

# Load :conference
conferences = pd.read_csv(CONFERENCES_SOURCE)
for _, row in conferences.iterrows():
    node = clean_uri(row["name"])
    node_type = clean_uri(row["type"])
    g.add((ns[node], ns.name, Literal(row["name"])))

# Load :proceeding
proceedings = pd.read_csv(PROCEEDING_SOURCE)
for _, row in proceedings.iterrows():
    node = f"proceeding_{row['proceeding']}"
    g.add((ns[node], ns.name, Literal(row["proceeding"])))
    g.add((ns[node], ns.year, Literal(row["year"])))

# Load :has_edition
editions = pd.read_csv(EDITION_SOURCE)
for _, row in editions.iterrows():
    conference = URIRef(mainURI+clean_uri(row["conference"]))
    proceeding = URIRef(f'{mainURI}proceeding_{row["proceeding"]}')
    g.add((conference, ns.has_edition, proceeding))

# Load :journal
journals = pd.read_csv(JOURNAL_SOURCE)
for _, row in journals.iterrows():
    node = clean_uri(row["name"])
    g.add((ns[node], ns.name, Literal(row["name"])))

# Load :volume
volumes = pd.read_csv(VOLUME_SOURCE)
for _, row in volumes.iterrows():
    node = f"volume_{row['volume']}"
    g.add((ns[node], ns.name, Literal(row["volume"])))
    g.add((ns[node], ns.year, Literal(row["year"])))

# Load :publish
publishes = pd.read_csv(PUBLICATION_SOURCE)
for _, row in publishes.iterrows():
    journal = URIRef(mainURI+clean_uri(row["journal"]))
    volume = URIRef(f'{mainURI}volume_{row["volume"]}')
    g.add((journal, ns.publish, volume))

# Load :submit_to_volume
submit_to_volume = pd.read_csv(PUBLISHES_SOURCE)
for _, row in submit_to_volume.iterrows():
    paper_node = URIRef(mainURI + clean_uri(row["article"]))
    volume_node = URIRef(f'{mainURI}volume_{row["volume"]}')
    g.add((paper_node, ns.submit_to_volume, volume_node))

# Load :submit_to_proceeding
submit_to_proceeding = pd.read_csv(PRESENTED_SOURCE)
for _, row in submit_to_proceeding.iterrows():
    paper_node = URIRef(mainURI + clean_uri(row["article"]))
    proceeding_node = URIRef(f'{mainURI}proceeding_{row["proceeding"]}')
    g.add((paper_node, ns.submit_to_proceeding, proceeding_node))


# Load review
reviews = pd.read_csv(REVIEWS_SOURCE)
for index, row in reviews.iterrows():
    # :reviewer
    reviewer = clean_uri(row["reviewer"])
    g.add((ns[reviewer], ns.name, Literal(row["reviewer"])))
    # :review
    review = f"review_{index}"
    g.add((ns[review], ns.decision_result, Literal(row["decision"])))
    g.add((ns[review], ns.decision_text, Literal(row["content"])))
    # :writes_review
    reviewer_node = URIRef(mainURI + reviewer)
    review_node = URIRef(mainURI + review)
    g.add((reviewer_node, ns.writes_review, review_node))
    # :review_of_paper
    paper_node = URIRef(mainURI+clean_uri(row["article"]))
    g.add((review_node, ns.review_of_paper, paper_node))

# Load :accepted (for papers to be acknowledged as publications)
accepted = pd.read_csv(PAPER_ACCEPTED_SOURCE)
for _, row in accepted.iterrows():
    node = clean_uri(row["article"])
    decision = "accepted" if row["final_decision"] else "not accepted"
    g.add((ns[node], ns.accepted, Literal(decision)))

# Load chair
chairs = pd.read_csv(BELONGS_TO_CONFERENCE)
for _, row in chairs.iterrows():
    # :chair
    node = clean_uri(row["chair"])
    g.add((ns[node], ns.name, Literal(row["chair"])))
    # :belongs_to_conference
    chair_node = URIRef(mainURI + node)
    conference_node = URIRef(mainURI + clean_uri(row["conference"]))
    g.add((chair_node, ns.belongs_to_conference, conference_node))

# Load :chair_designates
chair_designates = pd.read_csv(CHAIR_DESIGNATES_SOURCE)
for _, row in chair_designates.iterrows():
    chair_node = URIRef(mainURI + clean_uri(row["chair"]))
    reviewer_node = URIRef(mainURI + clean_uri(row["reviewer"]))
    g.add((chair_node, ns.chair_designates, reviewer_node))

# Load editor
editors = pd.read_csv(BELONGS_TO_JOURNAL)
for _, row in editors.iterrows():
    # :editor
    node = clean_uri(row["editor"])
    g.add((ns[node], ns.name, Literal(row["editor"])))
    # :belongs_to_journal
    editor_node = URIRef(mainURI + node)
    journal_node = URIRef(mainURI + clean_uri(row["journal"]))
    g.add((editor_node, ns.belongs_to_journal, journal_node))

# Load :editor_designates
editor_designates = pd.read_csv(EDITOR_DESIGNATES_SOURCE)
for _, row in editor_designates.iterrows():
    editor_node = URIRef(mainURI + clean_uri(row["editor"]))
    reviewer_node = URIRef(mainURI + clean_uri(row["reviewer"]))
    g.add((editor_node, ns.editor_designates, reviewer_node))

# Load :area
areas = pd.read_csv(AREA_SOURCE)
for _, row in areas.iterrows():
    node = clean_uri(row["area"])
    g.add((ns[node], ns.topic, Literal(row["area"])))

# Load item related to area
related_to = pd.read_csv(RELATED_TO_SOURCE)
for _, row in related_to.iterrows():

    main_node = URIRef(mainURI + clean_uri(row["name"]))
    area_node = URIRef(mainURI + clean_uri(row["area"]))
    g.add((main_node, ns.related_area, area_node))
    # if row["type"] == 'paper':
    #     g.add((main_node, ns.paper_area, area_node))
    # elif row["type"] == 'conference':
    #     g.add((main_node, ns.conference_area, area_node))
    # elif row["type"] == 'journal':
    #     g.add((main_node, ns.journal_area, area_node))


# # Print the graph
# print(g.serialize(format="turtle"))

# Save the graph
g.serialize(format="turtle", destination="graph/B2_abox.ttl")
