# we will create an empty dictionary to store the organization counts
organization_counts = {}

# Loop through author columns.
for i in range(1, 22):
    column_name = f"Author {i} Affiliation Classification"

    # if the column exist in the dataframe filter the dataFrame to select rows where the author's affiliation classification is "Organization."
    if column_name in df.columns:
        filtered_df = df[df[column_name] == "Organization"]
        
        # We will Store the counts of organization
        organization_counts[column_name] = filtered_df[f"Author {i} Affiliation"].value_counts()

# here we will store the total organization count. 
total_organization_counts = pd.concat(organization_counts.values()).groupby(level=0).sum()

# now we will Select the top 10 organizations with the highest contribution counts.
top_10_organizations = total_organization_counts.nlargest(10)

# we will create a pie chart.
plt.figure(figsize=(8, 8))
plt.pie(top_10_organizations, labels=top_10_organizations.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Top 10 Organizations by Contribution')
plt.show()
