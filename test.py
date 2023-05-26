import pandas as pd
mydict = {"a":[1,2,3,4],"b":[10,12,13,14],"c":[21,22,23,24],"sensors":{"1":"test","2":"test2"}}

sensors = mydict.pop('sensors')

print(sensors)
print(mydict)

df = pd.DataFrame(mydict)
df = df.rename({'a':'log(gdp)'}, axis=1)
print(df)