# we will create a list of column names that represent the affiliation classifications for authors.
author_classification_columns = [f"Author {i} Affiliation Classification" for i in range(21)]

# We then use the 'pd.melt' function to transform the dataFrame into a long format. This operation is useful for aggregating and analyzing data.
melted_data = pd.melt(df, id_vars=["Year"], value_vars=author_classification_columns, var_name="Author", value_name="Classification")

# Here we will group the melted data by year and classification and count of occurance.
# This will help to understand the distribution of author affiliations over the years.
grouped_data = melted_data.groupby(["Year", "Classification"]).size().unstack(fill_value=0)

# To visualize trends as percentages we will calculate the percentage distribution across classifications for each year.
percentage_data = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100

# We will create a list of all years present in the dataset.
all_years = range(df['Year'].min(), df['Year'].max() + 1)
percentage_data = percentage_data.reindex(all_years).fillna(method='ffill')

# Now we will plot an area chart 
fig, ax = plt.subplots(figsize=(10, 6))

percentage_data.plot(kind="area", ax=ax, colormap="viridis", alpha=0.7)

ax.set_xlabel("Year")
ax.set_ylabel("Percentage (%)")
ax.set_title("Trends in Percentage Distribution of Author Affiliation Classifications")

ax.legend(title="Classification", bbox_to_anchor=(1, 1))

ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))

plt.xticks(all_years)
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()
