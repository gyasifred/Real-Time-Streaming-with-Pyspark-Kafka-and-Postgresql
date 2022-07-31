import pickle
import pandas as pd

foo = list()
df= pd.read_csv("iot.csv")
data = df.to_dict(orient='records')
for i in data:
    foo.append((str(i)))


with open("/home/kgyasi/Desktop/streaming_data.pickle", "wb") as f:
    pickle.dump((foo), f)
