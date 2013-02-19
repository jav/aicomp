class EloRater:
    """
       Accepts player rating and player scores and returns two new
       suggested ratings for the players.

       Example: call with getRatings((1000,1000),(1,0)) to simulate
       two new players where one player won against the other. 
    """
    @staticmethod
    def getRatings(ratings, scores):
        p1_rating,p2_rating = map(float, ratings)
        p1_score,p2_score = map(float, scores)
        E_a = 1/(1+10**((p2_rating-p1_rating)/400))
        E_b = 1-E_a
        K = 32
        p1_new = p1_rating + K*(p1_score-E_a)
        p2_new = p2_rating + K*(p2_score-E_b)
        return (p1_new, p2_new)
