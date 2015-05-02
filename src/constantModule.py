
MovieSearch_base = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=x6usx7bn33cdn9vverg9f2v7&q="
ReviewSearch_base = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s/reviews.json?apikey=x6usx7bn33cdn9vverg9f2v7&page_limit=50&review_type=all&page=%s"
RelationSearch_base = "http://api.rottentomatoes.com/api/public/v1.0/movies/#ID HERE#/similar.json?apikey=x6usx7bn33cdn9vverg9f2v7"
Genre_base = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s.json?apikey=x6usx7bn33cdn9vverg9f2v7"

# MovieSearch_base = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=ytrwhcgkgpqbcgcvyugqcmbw&q="
# ReviewSearch_base = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s/reviews.json?apikey=ytrwhcgkgpqbcgcvyugqcmbw&page_limit=50&review_type=all&page=%s"
# RelationSearch_base = "http://api.rottentomatoes.com/api/public/v1.0/movies/#ID HERE#/similar.json?apikey=ytrwhcgkgpqbcgcvyugqcmbw"
# Genre_base = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s.json?apikey=ytrwhcgkgpqbcgcvyugqcmbw"

def MovieSearch(movietitle):
  tofetch = MovieSearch_base + movietitle.replace(" ", "%20")
  return tofetch

def ReviewSearch(movieID, pagenume):
  tofetch = ReviewSearch_base %(movieID,pagenume)
  return tofetch

def GenreSearch (movieID):
	tofetch = Genre_base %(movieID)
	return tofetch