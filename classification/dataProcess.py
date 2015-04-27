import pickle

if __name__ == "__main__": 
	test = pickle.load(open("Movie_dict", "r"))
	for key in test.keys():
		print key
		temp = test[key]
		#print temp['synopsis']
		print temp