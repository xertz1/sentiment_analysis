# Description: This main file asks the user for all the filenames of the
# keyword file, tweet file, and file to write to. After completing this it
# creates a report on the sentiment of all the tweets and gives back different peices of data.
# This data includes sentiment of top 5 countires, sentiment of all tweets, sentiment of retweeted tweets, etc.

# Imports sentiment analysis file
from sentiment_analysis import *

# Define main function


def main():
    # Asks user for keyword file name
    keyword_filename = input("Input keyword filename (.tsv file): ")
    if ".tsv" not in keyword_filename:  # Checks if .tsv is in filename, and raises exception if not
        raise Exception("Must have tsv file extension!")

    # Calls read_keywords and sets it equal to the dictionary of keywords read_keywords returns
    keywords = read_keywords(keyword_filename)

    # Asks user for tweet file name
    tweet_filename = input("Input tweet filename (.csv file): ")
    if ".csv" not in tweet_filename:  # Checks if .csv is in filename, and raises exception if not
        raise Exception("Must have txt file extension!")

    # Calls read_tweets and sets it equal to the list of tweet data read_tweets returns
    tweets_list = read_tweets(tweet_filename)

    # Asks user for output file name
    output_filename = input("Input filname to output report in (.txt file): ")
    if ".txt" not in output_filename:  # Checks if .txt is in the filename, and raises exception if not
        raise Exception("Must have txt file extension!")

    # Calls make_report and sets it equal to the dictionary of data make_report returns
    report = make_report(tweets_list, keywords)

    # Calls write_report function to create a report of all tweet information
    write_report(report, output_filename)


# Call of main function
main()
