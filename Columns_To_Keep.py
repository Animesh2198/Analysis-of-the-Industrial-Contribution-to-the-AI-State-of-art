# We will keep only those columns which we want in our dataframe. 
columns_to_keep = ['Title', 'Year', 'Source title', 'Cited by', 'Authors with affiliations',
                   'Abstract', 'Author Keywords', 'Index Keywords', 'Conference name',
                   'Conference location', 'Language of Original Document']


df = df[columns_to_keep]
