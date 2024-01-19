# To get top 20 highest cited count We will first select the columns "Cited by" and "Title" 
cited_by_column = df['Cited by']
title_column = df['Title']

# Here we will store the indices which contains the highest cited counts
top_10_indices = cited_by_column.nlargest(20).index

# here we will extract those indices 
top_10_cited_counts = cited_by_column.iloc[top_10_indices]
top_10_titles = title_column.iloc[top_10_indices]

# We will create a new dataFrame result_df to combine the cited Count and Title columns for the top 20 entries.
result_df = pd.DataFrame({"Cited Count": top_10_cited_counts, "Title": top_10_titles})

# Now will plot in table 
plt.figure(figsize=(10, 6))
plt.axis('off')

table = plt.table(cellText=result_df.values, colLabels=result_df.columns, cellLoc='center', loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)
table.auto_set_column_width([0, 1])

plt.title('Top 10 Highest Cited Counts with Corresponding Titles')

plt.tight_layout()
plt.savefig('top_10_cited_counts_table.png', dpi=300, bbox_inches='tight')
plt.show()
