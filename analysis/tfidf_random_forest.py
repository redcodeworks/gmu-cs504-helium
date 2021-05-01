import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from pyathena import connect
import joblib


df_experts = pd.read_csv('experts.csv')

hyper_params = [10,30,100,300]

avg_scores = []
for i in hyper_params:
    final_model = Pipeline([('tfidf',TfidfVectorizer(stop_words='english')),('forest',RandomForestRegressor(n_estimators = i, random_state = 0))])
    final_model.fit(df_experts['review'],df_experts['score'])


    scores = cross_val_score(pipe,df_experts['review'],df_experts['score'],scoring = 'neg_root_mean_squared_error',cv = 5)
    avg_scores.append((sum(scores)/len(scores))*-1)


avg_scores   #average rmse


#To built final modle use below code after choosing hyperparameter (i)

#final_model = Pipeline([('tfidf',TfidfVectorizer(stop_words='english')),('forest',RandomForestRegressor(n_estimators = i, random_state = 0))])
#final_model.fit(df_experts['review'],df_experts['score'])
#final_model.predict(new_text)


