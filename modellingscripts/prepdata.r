source("util.r")

febtweets <- loadtweets("../data/Metoo_Feb262018.csv")
mar06tweets <- loadtweets("../data/MeToo_March062018.csv")
mar08tweets <- loadtweets("../data/MeToo_March082018.csv")
mar10tweets <- loadtweets("../data/Metoo0310_2017.csv")
tweets = bind_rows(febtweets, mar06tweets, mar08tweets, mar10tweets)

tweets