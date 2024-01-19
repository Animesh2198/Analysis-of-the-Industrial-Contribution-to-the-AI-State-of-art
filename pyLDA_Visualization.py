#Importing library for lda visualization 
!pip install pyLDAvis

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

#This will allow to visualize the data 
vis_data = gensimvis.prepare(lda_model, corpus, dictionary, n_jobs=1)
pyLDAvis.display(vis_data)
