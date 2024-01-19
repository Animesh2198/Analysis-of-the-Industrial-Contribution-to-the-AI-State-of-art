# Loop through a range.
for i in range(22):
    # here we will create columns for the names, affiliation and country we will split.
    col_name = f"Author with Affiliation {i}"
    new_col_name = f"Author {i} Name"
    new_col_affiliation = f"Author {i} Affiliation"
    new_col_country = f"Author {i} Country"

    # here we will use the delimiter to split the coulumn ", "
    split_values = df[col_name].str.split(", ")
    df[new_col_name] = split_values.str[0]

    # here we will extract the affiliation and country from the remaining parts of the split values.
    affiliation_country = split_values.str[1:].str.join(", ").str.rsplit(", ", n=1, expand=True)

    # now we will create a new column for the author's affiliation.
    df[new_col_affiliation] = affiliation_country[0]

    # here we have to apply a lambda function to map country names according to pycountry library.
    df[new_col_country] = affiliation_country[1].apply(
        lambda x: [country.name for country in pycountry.countries if country.name in str(x)] if pd.notnull(x) else None
    )
    df[new_col_country] = df[new_col_country].apply(lambda x: x[0] if (x and len(x) > 0) else None)
