

import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

df_experts = pd.read_csv('experts.csv')

hyper_params = [100,300,1000,3000,10000]

avg_scores = []
for i in hyper_params:
    pipe = Pipeline([('tfidf',TfidfVectorizer(stop_words='english')),('lsa',TruncatedSVD(n_components= i, random_state=0)), ('reg',LinearRegression())])
    scores = cross_val_score(pipe,df_experts['review'],df_experts['score'],scoring = 'neg_root_mean_squared_error',cv = 5)
    avg_scores.append((sum(scores)/len(scores))*-1)


avg_scores   #average rmse


#To built final modle use below code after choosing hyperparameter (i)

#final_model = Pipeline([('tfidf',TfidfVectorizer(stop_words='english')),('lsa',TruncatedSVD(n_components= i, random_state=0)), ('reg',LinearRegression())])
#final_model.fit(df_experts['review'],df_experts['score'])
#final_model.predict(new_text)








