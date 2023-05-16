import pandas as pd
import random

REVIEWS_SOURCE = 'data/review_evolved.csv'
NAMES_SOURCE = 'data/names_gen.csv'
PUBLISHES_SOURCE = 'data/publishes.csv'
PRESENTED_SOURCE = 'data/presented.csv'
PROCEEDING_SOURCE = 'data/proceeding.csv'
EDITION_SOURCE = 'data/edition.csv'
PUBLICATION_SOURCE = 'data/publication.csv'
CONFERENCES_SOURCE = 'data/conference.csv'
JOURNAL_SOURCE = 'data/journal.csv'
PAPER_SOURCE = 'data/papers.csv'


# Output routes
OUTPUT_BELONGS_TO_CONFERENCE = 'data/belongs_to_conference.csv'
OUTPUT_BELONGS_TO_JOURNAL = 'data/belongs_to_journal.csv'
OUTPUT_CHAIR_DESIGNATES = 'data/chair_designates.csv'
OUTPUT_EDITOR_DESIGNATES = 'data/editor_designates.csv'
OUTPUT_RELATED_TO = 'data/related_to.csv'
OUTPUT_PAPER_ACCEPTED = 'data/paper_accepted.csv'
OUTPUT_AREA = 'data/area.csv'

reviews = pd.read_csv(REVIEWS_SOURCE)
names = pd.read_csv(NAMES_SOURCE)
publishes = pd.read_csv(PUBLISHES_SOURCE)
presented = pd.read_csv(PRESENTED_SOURCE)
edition = pd.read_csv(EDITION_SOURCE)
publication = pd.read_csv(PUBLICATION_SOURCE)
conferences = pd.read_csv(CONFERENCES_SOURCE)
journals = pd.read_csv(JOURNAL_SOURCE)
papers = pd.read_csv(PAPER_SOURCE)
areas = pd.read_csv(OUTPUT_AREA)

random.seed(123)

name_list = list(names['names'].unique())
n = len(name_list)
chairs = name_list[:n//2]
editors = name_list[n//2:]

# # Generate chairs relations

# :belongs_to_conference
conf_list = list(conferences['name'].unique())
chair_df = pd.DataFrame(columns=['chair', 'conference'])
for chair in chairs:
    conf = random.choice(conf_list)
    row_data = {'chair': chair, 'conference': conf}
    chair_df = pd.concat([chair_df, pd.DataFrame([row_data])], ignore_index=True)

chair_df.to_csv(OUTPUT_BELONGS_TO_CONFERENCE,encoding='utf-8',index=False)

# :chair_designates
conf_merge = pd.merge(conferences, chair_df, left_on='name', right_on='conference')
conf_merge = pd.merge(conf_merge, edition, left_on='conference', right_on='conference')
conf_merge = pd.merge(conf_merge, presented, left_on='proceeding', right_on='proceeding')
conf_merge = pd.merge(conf_merge, reviews, left_on='article', right_on='article')
result_df = conf_merge.loc[:, ['chair', 'reviewer']].drop_duplicates()

unique_reviewers = result_df['reviewer'].unique()
random_chairs = [random.choice(result_df[result_df['reviewer'] == reviewer]['chair'].tolist()) for reviewer in unique_reviewers]
new_data = {'chair': random_chairs, 'reviewer': unique_reviewers}
chair_designates = pd.DataFrame(new_data)

chair_designates.to_csv(OUTPUT_CHAIR_DESIGNATES,encoding='utf-8',index=False)

# Generate editors relations

# :belongs_to_journal
jour_list = list(journals['name'].unique())
editor_df = pd.DataFrame(columns=['editor', 'journal'])
for editor in editors:
    jour = random.choice(jour_list)
    row_data = {'editor': editor, 'journal': jour}
    editor_df = pd.concat([editor_df, pd.DataFrame([row_data])], ignore_index=True)

editor_df.to_csv(OUTPUT_BELONGS_TO_JOURNAL,encoding='utf-8',index=False)

# :editor_designates
jour_merge = pd.merge(journals, editor_df, left_on='name', right_on='journal')
jour_merge = pd.merge(jour_merge, publication, left_on='journal', right_on='journal')
jour_merge = pd.merge(jour_merge, publishes, left_on='volume', right_on='volume')
jour_merge = pd.merge(jour_merge, reviews, left_on='article', right_on='article')
result_df = jour_merge.loc[:, ['editor', 'reviewer']].drop_duplicates()

unique_reviewers = result_df['reviewer'].unique()
random_editor = [random.choice(result_df[result_df['reviewer'] == reviewer]['editor'].tolist()) for reviewer in unique_reviewers]
new_data = {'editor': random_editor, 'reviewer': unique_reviewers}
editor_designates = pd.DataFrame(new_data)

editor_designates.to_csv(OUTPUT_EDITOR_DESIGNATES,encoding='utf-8',index=False)

# Generate links with area and paper, conference and journal
area_list = list(set(papers['key_words'].str.split('|', expand=True).stack()))
area_df = pd.DataFrame({'area': area_list})

area_df.to_csv(OUTPUT_AREA, index=False)

related_to_df = papers.assign(area=papers['key_words'].str.split('|')).explode('area')
related_to_df = related_to_df.reset_index(drop=True)
related_to_df = related_to_df.rename(columns={'title': 'name'})
related_to_df = related_to_df.loc[:, ['name', 'area']]
related_to_df = related_to_df.assign(type='paper')

for _,row in conferences.iterrows():
    for _ in range(random.randint(1,5)):
        area = random.choice(area_list)
        # For query 4 to have answers
        if random.choice([True, False]):
            area = 'Databases'
        row_data = {'type': 'conference', 'name': row['name'], 'area': area}
        related_to_df = pd.concat([related_to_df, pd.DataFrame([row_data])], ignore_index=True)

for _,row in journals.iterrows():
    for _ in range(random.randint(1,7)):
        area = random.choice(area_list)
        row_data = {'type': 'journals', 'name': row['name'], 'area': area}
        related_to_df = pd.concat([related_to_df, pd.DataFrame([row_data])], ignore_index=True)

related_to_df = related_to_df.drop_duplicates()
related_to_df.to_csv(OUTPUT_RELATED_TO,index=False)

# Generate paper accepted

final_decision = reviews.groupby('article')['decision'].apply(lambda x: (x == 'accepted').sum() / len(x) >= 0.5)
final_decision_df = pd.DataFrame({'article': final_decision.index, 'final_decision': final_decision.values})

final_decision_df.to_csv(OUTPUT_PAPER_ACCEPTED,encoding='utf-8',index=False)

# Generate paper subtypes
paper_subtypes = ['full paper', 'short paper', 'demo paper']

# poster will be handled only for conferences
papers_conf = presented['article'].unique()

col_type = []
for _, row in papers.iterrows():
    # if it was sent to a conference it can be poster
    type = None
    if row['title'] in papers_conf:
        if random.choice([True, False]):
            type = 'poster'
    if not type:
        type = random.choice(paper_subtypes)
    col_type.append(type)

papers["type"] = col_type
papers.to_csv(PAPER_SOURCE,index=False)







