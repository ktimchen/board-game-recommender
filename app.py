import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import json


app = Flask(__name__)

with open("sorted_list_games.json", 'r') as file:
    database = json.load(file)


games_info = pd.read_csv("game_id_cat.txt")
with open("game_dict.txt", "r") as file:
    game_dict = json.load(file)
    



@app.route("/")
def home():
    return render_template("index.html")
    # return hello 
    
    
    
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = [x for x in database if search.lower() in x.lower()]
    
    results = query[:min(20, len(query))]
  
    return jsonify(matching_results=results)    
    
# making recommendations here:
    
@app.route("/predict", methods = ["POST"])

def predict():
    #takes the html input
    
    sample_name = next(request.form.values())
    
        
        
    try:
        sample = games_info.loc[games_info.primary == sample_name, "id"].iloc[0]
    except:        
        dict_exception = { "This is not a game : try again!" : [{"id": "notagame", "image": "https://via.placeholder.com/200/?text=not_a_game.png", "primary": "Not a game", "desc_1": "not a game", "desc_2": "not a game" }] }
        return render_template("index.html", info =  dict_exception.items() )
    
    #print(next(sample))
    
    
    
    games = game_dict.get(str(sample))
    
    data = games_info[games_info.id.isin(games) ].copy()
    
    data["header"] = "empty"
    df_sample = games_info[games_info.id == int(sample)].reset_index()
    
    #categories and mechanics of the sample
    cats = df_sample.boardgamecategory[0].strip("[]").replace("'","").split(", ")
    mechs = df_sample.boardgamemechanic[0].strip("[]").replace("'","").split(", ")
    
    for cat in cats:    
        x = cat
        data.loc[((data.boardgamecategory.str.contains(cat) ) & (data.header == "empty")), "header"] = x
    
    for mech in mechs:    
        x = mech
        data.loc[((data.boardgamemechanic.str.contains(mech) )& (data.header == "empty")), "header"] = x
        
    data.loc[data.header == "empty", "header"] = "Also try"
    
    dict_out = {}
    top_20 = data.sort_values(by = ["Board Game Rank"]).iloc[:20]
    dict_out["Top games"] = top_20.to_dict(orient = "records")

    for h in data.header.unique():
        dict_out[h] = data[data.header == h].to_dict(orient = "records")
        
    try:
        len_also = len(dict_out["Also try"])
        if len_also > 30:
            dict_out["Try these"] = dict_out["Also try"][20:len_also]
            dict_out["Also try"] = dict_out["Also try"][0:20]
    except:
        pass
        
            
    
    print("111111111111111111111111111111222222222222222")
    
        
    
    #data = game_info[game_info.id.isin(games)][["id", "image", "primary"]]
    
    #data = data.to_dict(orient = "records")
    
    
    
    #return the template to the html
    
    return render_template("index.html", info = dict_out.items() )














# run the app
if __name__ == "__main__":
    app.run(debug = True)