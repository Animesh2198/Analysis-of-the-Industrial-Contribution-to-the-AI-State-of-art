# Here we create an empty dictionary to count affiliations by country and affiliation.
affiliation_counts = {}

# we will loop through a range of 0 to 20 columns.

for i in range(21):
    # For every author we need to access their country and affiliation.
    country_col_name = f"Author {i} Country"
    affiliation_col_name = f"Author {i} Affiliation Classification"

    # We then extract lists of countries and affiliations for the current author.
    countries = df[country_col_name].tolist()
    affiliations = df[affiliation_col_name].tolist()

    # we iterate through the lists of countries and affiliations for this author.
    for country, affiliation in zip(countries, affiliations):
        if isinstance(country, str) and isinstance(affiliation, str):
            # here we create a unique key to represent country and affiliation.
            key = (country, affiliation)

            # If this key is not in our dictionary, we initialize its count to 0.
            if key not in affiliation_counts:
                affiliation_counts[key] = 0

            # here we increment the count for this combination of country and affiliation.
            affiliation_counts[key] += 1

# Here we will convert our dictionary into a DataFrame for further analysis.
counts_df = pd.DataFrame(list(affiliation_counts.items()), columns=["Country_Affiliation", "Count"])

# We will split the country_Affiliation column into separate country and affiliation columns.
counts_df[['Country', 'Affiliation']] = pd.DataFrame(counts_df['Country_Affiliation'].tolist(), index=counts_df.index)

# We drop the original "Country_Affiliation" column as we have extracted its components.
counts_df.drop(columns=['Country_Affiliation'], inplace=True)

# Here we pivot the dataFrame to create a table structure for analysis.
counts_pivot = counts_df.pivot(index='Country', columns='Affiliation', values='Count')

# We add a cumulative column that sums the counts across affiliations for each country.
counts_pivot['Cumulative'] = counts_pivot.sum(axis=1)

# We will sort the table to find the top 20 countries with the highest cumulative counts.
top_10_counts = counts_pivot.sort_values(by='Cumulative', ascending=False).head(20)

# Here we will create a table visualization and save it as an image.
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')
ax.table(cellText=top_10_counts.values,
         colLabels=top_10_counts.columns,
         rowLabels=top_10_counts.index,
         cellLoc='center',
         loc='center',
         colColours=['#f2f2f2'] * len(top_10_counts.columns),
         rowColours=['#f2f2f2'] * len(top_10_counts.index))

plt.tight_layout()
plt.savefig('top_10_counts_table.png', dpi=300, bbox_inches='tight')
plt.show()
