## Board Game Recommender <a href="http://www.findme.games">findme.games</a>

#### Looking for your next board game?
Want another game for your quarantine game nights? <br>
Use my board game recommender system to find your next favorite!
#### How did I build this? <br>
Using item-based collaborative filtering. <br>
I collected a data set of ~15mil ratings from 190,000 users for 10,500 games by scraping the www.boardgamegeek.com API. I created a sparse user-game matrix based on this data.
After taking care of the bias and using an SVD to decrease the rank of the user-game matrix, I computed the distances between games. Given a game, the system returns a 100 recommendations based on the query.
Given a game, the system returns a 100 recommendations based on the query.
#### Tools: <br>
Python, scipy.sparse and scikit-learn libraries, Flask, some CSS and jQuery.


<br>
<br>
<br>

User-game matrix and linear algebra part of the project can be found here https://github.com/ktimchen/recommender-matrix
