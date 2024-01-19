# Here we will create an empty dictionary 

conference_counts = {}

# we will iterate through the unique conferences present in the conference column. 
for conference in df['conference'].unique():
    conference_counts[conference] = {}

    # We loop through the range of 0 to 20.
    for i in range(21):
        column_name = f'Author {i} Affiliation Classification'

        # We will count the occurrences of each affiliation classification for the current conference and author.
        counts = df[df['conference'] == conference][column_name].value_counts()
        for affiliation, count in counts.items():
            if affiliation not in conference_counts[conference]:
                conference_counts[conference][affiliation] = 0
            conference_counts[conference][affiliation] += count

# Here we will iterate through each conference and its corresponding affiliation classification counts.
for conference, counts in conference_counts.items():
    print(f"Conference: {conference}")

    for affiliation, count in counts.items():
        print(f"{affiliation}: {count}")
    print()
