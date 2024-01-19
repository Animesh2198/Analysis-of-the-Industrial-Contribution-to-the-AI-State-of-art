
# we will define a function classify_affiliation that takes an affiliation as input. This function will categorize affiliations into three groups: "University," "University/Organization," or "Organization."

def classify_affiliation(affiliation):
    # if affiliation contains keywords associated with universities it will return "univerisity".
    if isinstance(affiliation, str) and any(keyword in affiliation.lower() for keyword in ["university", "université", "college", "polytechnic", "academy", "univ", "universitaire"]):
        return "University"
    # if affiliation contains keywords associated with institutes it will return "University/Organization".
    elif isinstance(affiliation, str) and any(keyword in affiliation.lower() for keyword in ["institute", "inst"]):
        return "University/Organization"
    # if affiliation does not come under any condition it will return "Organization".
    elif isinstance(affiliation, str) and affiliation.strip() != "":
        return "Organization"
    else:

# we will loop through a range of 0 to 21.
for i in range(22):
    # Here we will create column name for affiliation and classification in range.
    affiliation_column = f"Author {i} Affiliation"
    classification_column = f"Author {i} Affiliation Classification"

    # we will Extract a list of affiliations.
    if classification_column not in df.columns:
        affiliations = df[affiliation_column].tolist()

        # here we will use the function to classify the affiliation 
        classification = [classify_affiliation(affiliation) for affiliation in affiliations]

        # here we will insert classification in dataframe
        df.insert(df.columns.get_loc(affiliation_column) + 1, classification_column, classification)
