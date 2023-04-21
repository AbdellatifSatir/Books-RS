from flask import Flask
from flask import render_template
from flask import request
from fuzzywuzzy import process
import numpy as np
import pandas as pd
import pickle


app = Flask(__name__)

popular_df = pickle.load(open('popular_df.pkl',mode='rb'))
# ['Book-Title', 'Book-Author', 'Image-URL-M', 'Num_ratings', 'Avg_ratings']

pivot = pickle.load(open('pivot.pkl',mode='rb'))
# [index='Book-Title' , columns='User-ID' , values='Book-Rating']  , (706, 810)

books = pickle.load(open('books.pkl',mode='rb'))
# ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher','Image-URL-S', 'Image-URL-M''Image-URL-L']

cos_sim = pickle.load(open('cos_sim.pkl',mode='rb'))
# 706 rows × 706 columns


@app.route('/')
def index():
    return render_template(
        'index3.html',
        lenn = len(popular_df),
        Title = list(popular_df['Book-Title'].values),
        Author = list(popular_df['Book-Author'].values),
        Image = list(popular_df['Image-URL-M'].values),
        Votes = list(popular_df['Num_ratings'].values),
        Rating = list(popular_df['Avg_ratings'].values),
        Rating_ro = [round(r,2) for r in list(popular_df['Avg_ratings'].values)]
    )



@app.route('/recommend')
def recommend():
    return render_template(
        'recommend2.html'
    )

@app.route('/recommend',methods=['POST'])
# def test_matching(name):
#     match_name = process.extractOne(name , pivot.index)[0]
#     return match_name

def similar_books():
    requested_book = request.form.get('requested_book')
    requested_book = process.extractOne(requested_book , pivot.index)[0]
    index = np.where( pivot.index == requested_book )[0][0] #get the book index
    sim_books = sorted(list(enumerate(cos_sim[index])) , key=lambda x:x[1] , reverse=True)[0:21] 
    #display the sim books 
    
    df = []
    for i in sim_books:
        book = []
        sim_books_df = books[books['Book-Title'] == pivot.index[i[0]]]
        book.extend(list(sim_books_df.drop_duplicates('Book-Title')['Book-Title'].values))
        book.extend(list(sim_books_df.drop_duplicates('Book-Title')['Book-Author'].values))
        book.extend(list(sim_books_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        df.append(book)
    #print(df)

    return render_template('recommend2.html' , data=df)





if __name__ == '__main__':
    app.run(debug=True)