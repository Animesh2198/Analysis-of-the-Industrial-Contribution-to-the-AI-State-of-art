# first we will create an empty dictionary to store university counts 
university_counts = {}

# Loop through author columns
for i in range(1, 22):
    column_name = f"Author {i} Affiliation Classification"

    # if the column exists in the dataFrame filter the dataFrame to select rows where the author's affiliation classification is "University."
    if column_name in df.columns:
        filtered_df = df[df[column_name] == "University"]
        
        # Store the counts of different universities for this author's affiliation classification.
        university_counts[column_name] = filtered_df[f"Author {i} Affiliation"].value_counts()

# here we will store the total counts of university 
total_university_counts = pd.concat(university_counts.values()).groupby(level=0).sum()

# here we will store the top 10 universities 
top_10_universities = total_university_counts.nlargest(10)

# we will create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(top_10_universities, labels=top_10_universities.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Top 10 Universities by Contribution')
plt.show()
