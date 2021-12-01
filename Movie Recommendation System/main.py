import numpy as np
import pandas as pd
import flask
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
data = pd.read_csv("main_data.csv")
app = flask.Flask(__name__)
def create_similarity():
    data = pd.read_csv("main_data.csv")
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['combination'])
    similarity = cosine_similarity(count_matrix)
    return data,similarity
def rcmd(m):
    m.lower()
    data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l
def get_suggestions():
    data = pd.read_csv("main_data.csv")
    return list(data['movie_title'].str.capitalize())
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        suggestions = get_suggestions()
        return(flask.render_template('index.html',suggestions=suggestions))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name'].lower()
        result_final = rcmd(m_name.lower())
        print(m_name,result_final)
        if result_final == 'Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies':
            return(flask.render_template('negative.html',name=m_name))
        else:
            return flask.render_template('positive.html',movie_names=result_final,search_name=m_name)

if __name__ == "__main__":
    app.run(debug=True,port=8000)