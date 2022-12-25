# chatbot-thai-stock-advisor

- Using DialogFlow for Line Chatbot
- Using stock_news_title_sentiment.ipynb to train and test data_set.csv file and scrapping stock news title to do sentiment analysis and save to firestore db
- Using chatbot.py for backend connect to firestore db and dialoflow
    - run with python3 chatbot.py
    - ngrok http 5001 to publish localhost to online
    - copy Forwarding Link to Fulfillment -> Webhook on DialogFlow
