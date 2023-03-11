import pickle
f = open("drugTree.pkl", "rb")
model = pickle.load(f)
print(model.predict([[1, 5, 1, 2]]))