import pickle
f = open("drugTree.pkl", "rb")
model = pickle.load(f)
print(model.predict([[1, 19, 1, 0]]))
