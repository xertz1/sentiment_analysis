# Description: This file sentiment_analysis takes all all the file names names from main.py
# and takes the information from each file and creates a sentiment anyalsis based on each tweet.
# From the data it forms a report based on the anyalsis and gives it back to the user.
# It gets data such as: Sentiment of all tweets, Top 5 countries avg sentiment value, total favorites and retweets, etc.

# Defines read_keyword to create a dictionary with keywords and its value
def read_keywords(keyword_file_name):
    keywords_dict = {}  # Initalizes dictionary function to store keywords and value

    # Try, except to catch errors when opening files
    try:
        # Opens user filename for reading
        f = open(keyword_file_name, "r")
        line = f.readline()  # Reads firstline of file

        # Adds all keywords with its repsective value into a dictionary
        while line != "":
            lines = line.strip().split('\t')
            keywords_dict[lines[0]] = int(lines[1])
            line = f.readline()
        f.close()  # Closes file
        return keywords_dict  # Returns keyword dicttionary
    except IOError:
        # Lets user know the file could not be read
        print("Could not open file {}!".format(keyword_file_name))
        return keywords_dict  # Returns empty list

# Defines clean_tweet_text to clean the tweet from the file of all punctation


def clean_tweet_text(tweet_text):
    ALPAHABET = " abcdefghijklmnopqrstuvwxyz"  # Initalize constant with alphabet
    tweet_text = tweet_text.lower()  # Sets tweet to lower case

    # Removes all punctation and non english words to clean the tweet
    for letter in tweet_text:
        if letter not in ALPAHABET:
            tweet_text = tweet_text.replace(letter, "")

    return tweet_text  # Returns a clean tweet with not punctation

# Defines calc_sentiment to find sentiment value of tweet


def calc_sentiment(tweet_text, keyword_dict):
    sentiment_value = 0  # Initalizes sentiment value to 0
    tweet_text = tweet_text.split()  # Splits tweet into sperate words

    # Calculates sentiment value
    for x in keyword_dict:
        for y in range(0, len(tweet_text)):
            if x == tweet_text[y]:  # Compares keywords with words in tweet
                # Adds sentiment value from keyword dict
                sentiment_value += keyword_dict[x]

    return sentiment_value  # Returns sentiment value

# Defines classify function to determine what type of tweet it is


def classify(score):
    # Determines if tweet is positive, negative, or neutral depending on sentiment value
    if score > 0:
        return "positive"
    elif score == 0:
        return "neutral"
    elif score < 0:
        return "negative"

# Defines read_tweet function


def read_tweets(tweet_file_name):
    list_of_dicts = []  # Intializes list to store all tweet info in a dictionary

    try:  # Try, except to catch error when opening file to read
        # Open files for reading
        f = open(tweet_file_name, "r")
        line = f.readline()

        # Splits all tweet information into a dictionary with a key and value the into a list
        while line != "":
            data = line.strip().split(',')  # Splits tweet info into a list

            # If lan and lon are not NULL stores them as a float
            if data[10] != "NULL":
                data[10] = float(data[10])
                data[9] = float(data[9])

            # Adds all tweet info into a dictionary from list
            list_of_dicts.append({"city": str(data[8]), "country": str(data[6]), "date": str(data[0]), "favorite": int(data[4]), "lang": str(data[5]), "lat": data[9],
                                 "lon": data[10], "retweet": int(data[3]), "state": str(data[7]), "text": str(clean_tweet_text(data[1])), "user": str(data[2])})
            line = f.readline()
        f.close()  # Closes file

        return list_of_dicts  # Returns list of tweet info

    except IOError:
        # Lets user know an error occured when opening file
        print("Could not open file {}".format(tweet_file_name))
        return list_of_dicts  # Returns empty list

# Defines make_report to gather all information to include in the report


def make_report(tweet_list, keyword_dict):

    country_sentiment = {}  # Initalizes dictionary for country setniment values
    country_apperances = {}  # Initalizes dicionary for country appearences
    country_avg_sentiment = {}  # Initalizes dicionary for country avg sentiment values
    dict_report = {}  # Initalizes dictionary to store report values
    average_fav = 0  # Initalizes average_fav to store average sentiment values for tweets with favorites
    count_fav = 0  # Initalizes count_fav to store the amount of tweets with a favorite
    # Initalizes average_retweet to store average sentiment of tweets with retweets
    average_retweet = 0
    count_retweet = 0  # Initalizes variable to store amount of tweets that have a retweet
    # Intializes variable to store average sentiment values of all tweets
    average_sentiment = 0
    countries = ""  # Intializes variable to store a string of top 5 countries in order

    # Initalizes dictionary values for report
    dict_report["num_positive"] = 0
    dict_report["num_neutral"] = 0
    dict_report["num_negative"] = 0
    dict_report["num_tweets"] = 0
    dict_report["avg_sentiment"] = 0

    # Initalizes two dictionaries without NULL in it for their sentiment and number of appearences
    for x in range(0, len(tweet_list)):
        if (tweet_list[x]["country"] != "NULL"):
            country_sentiment[tweet_list[x]["country"]] = 0
            country_apperances[tweet_list[x]["country"]] = 0

    if (len(tweet_list)) > 0:  # Checks if list contains any tweets

        for i in range(0, len(tweet_list)):

            # Performs calculations only if there is more than one favorite
            if int(tweet_list[i]["favorite"]) > 0:
                average_fav += calc_sentiment(
                    tweet_list[i]["text"], keyword_dict)  # Calculates average sentiment value of favorites
                count_fav += 1  # Calculates total amount of favorites

            # Performs calculations only if there is more than one retweet
            if int(tweet_list[i]["retweet"]) > 0:
                average_retweet += calc_sentiment(
                    tweet_list[i]["text"], keyword_dict)  # Calculates average sentiment value of retweets
                count_retweet += 1  # Calculates total amount of retweets

            # Finds total number of positive, neutral, and negative tweets and adds them to the dicitonary
            if (classify(calc_sentiment(tweet_list[i]["text"], keyword_dict))) == "positive":
                # Adds to toal positive tweets
                dict_report["num_positive"] += 1
            elif (classify(calc_sentiment(tweet_list[i]["text"], keyword_dict))) == "neutral":
                dict_report["num_neutral"] += 1  # Adds to total netural tweets
            elif (classify(calc_sentiment(tweet_list[i]["text"], keyword_dict))) == "negative":
                # Adds to total negative tweets
                dict_report["num_negative"] += 1

            # Calculates average sentiment value of all tweets
            average_sentiment += calc_sentiment(
                tweet_list[i]["text"], keyword_dict)

            # Adds total number of tweets to dictionary
            dict_report["num_tweets"] += 1

            if (tweet_list[i]["country"] != "NULL"):  # Checks if the country exists
                country_sentiment[tweet_list[i]["country"]  # Finds all countries sentiment values
                                  ] += calc_sentiment(tweet_list[i]["text"], keyword_dict)

                # Finds total amount of country appearences
                country_apperances[tweet_list[i]["country"]] += 1

        # Finds average sentiment values of all countries only if there is a country
        for y in range(0, len(tweet_list)):
            if tweet_list[y]["country"] != "NULL":
                if country_apperances[tweet_list[y]["country"]] != 0:
                    # Calculates average sentiment values of countries
                    country_avg_sentiment[tweet_list[y]["country"]] = (
                        country_sentiment[tweet_list[y]["country"]]/country_apperances[tweet_list[y]["country"]])

    # Adds avg amount of favorites if there is more than one favorite otherwise returns NAN
    if count_fav > 0:
        dict_report["avg_favorite"] = round((average_fav/count_fav), 2)
    else:
        dict_report["avg_favorite"] = "NAN"

    # Adds avg amount of retweets if there is more than one retweet otherwise returns NAN
    if count_retweet > 0:
        dict_report["avg_retweet"] = round((average_retweet/count_retweet), 2)
    else:
        dict_report["avg_retweet"] = "NAN"

    # Checks amount of if there is more than one tweet
    if dict_report["num_tweets"] != 0:
        # Adds sentiment avg to dictionary report
        dict_report["avg_sentiment"] = round(
            (average_sentiment/dict_report["num_tweets"]), 2)
    else:
        # If there are 0 tweets it returns NAN
        dict_report["avg_sentiment"] = "NAN"

    # Adds total number of tweets to dict
    dict_report["num_favorite"] = count_fav
    # Adds total number of retweets to dict
    dict_report["num_retweet"] = count_retweet

    # Sorts top 5 countries from greatest to least
    sorted_country_sentiment = sorted(
        country_avg_sentiment.items(), key=lambda x: x[1], reverse=True)
    converted_country_sentiment = list(sorted_country_sentiment)
    converted_country_sentiment = converted_country_sentiment[:5]

    # Adds ordered list of top 5 countries from a list into one string
    for j in range(0, len(converted_country_sentiment)):
        if (j == len(converted_country_sentiment)-1):
            countries = countries + converted_country_sentiment[j][0]
        elif (j != len(converted_country_sentiment)-1):
            countries = countries + converted_country_sentiment[j][0] + ", "

    # Adds top 5 countires into dict_report
    dict_report["top_five"] = countries

    return dict_report  # Returns dictionary report

# Defines write_report function


def write_report(report, output_file):
    # Try, except to catch errors with file not opening
    try:
        # Opens file for writing
        f = open(output_file, "w")
        # Writes all information collected and processed about tweets to file
        f.write("Average sentiment of all tweets: " +
                str(report["avg_sentiment"]) + "\nTotal number of tweets: " + str(report["num_tweets"]) + "\nNumber of positive tweets: " + str(report["num_positive"]) + "\nNumber of negative tweets: " + str(report["num_negative"]) + "\nNumber of netural tweets: " + str(report["num_neutral"]) + "\nNumber of favorited tweets: " + str(report["num_favorite"]) + "\nAverage sentiment of favorited tweets: " + str(report["avg_favorite"]) + "\nNumber of retweeted tweets: " + str(report["num_retweet"]) + "\nAverage sentiment of retweeted: " + str(report["avg_retweet"]) + "\nTop five countries by average sentiment: " + report["top_five"])
        print("Wrote reoprt to {}".format(output_file))
        f.close()  # Closes file
    except IOError:
        # Tells user if file could not be opened
        print("Count not open file {}".format(output_file))
