
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from apyori import apriori
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title('Market Basket Analysis')

st.set_option('deprecation.showPyplotGlobalUse', False)
file_bytes = st.file_uploader("Upload a file", type="csv")
words = st.sidebar.selectbox("No.of Words", range(10,1000,10))
if file_bytes is not None:
    dataset = pd.read_csv(file_bytes, header = None)
    dim = dataset.shape
    rows = dim[0]
    cols = dim[1]
    print(rows, cols)
    transactions = []
    for i in range(0, rows):
        transactions.append([str(dataset.values[i,j]) for j in range(0, cols)])
    rule_list = apriori(transactions, min_support = 0.003, min_confidence = 0.1, min_lift = 3, min_length = 2)
    results = list(rule_list)
    bought_item = [tuple(result[2][0][0])[0] for result in results]
    will_buy_item = [tuple(result[2][0][1])[0] for result in results]
    support_values = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lift_values = [result[2][0][3] for result in results]
    new_data = list(zip(bought_item,will_buy_item,support_values,confidences,lift_values))
    new_df=pd.DataFrame(new_data,columns=["Boungt Item", "Expected To Be Bought", "Support", "Confidence","Lift"])
  
    st.sidebar.header("Select Item")
    Input = st.sidebar.selectbox('Object Variables', new_df["Boungt Item"])
    print(Input)
    sample = new_df[new_df['Boungt Item'] == Input]
    lis1 = []
    for i in sample["Expected To Be Bought"]:
        lis1.append(i)
    space = " "
    output = space.join(lis1)
    output_final = output.replace("nan", "")
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 32px;">Recommended Items for above selected Item</p>'
    st.markdown(new_title, unsafe_allow_html=True)

    #st.markdown("Recommended Items for above selected Item")
    st.write(output_final)
    st.write("Word Cloud Plot")
    wordcloud = WordCloud(background_color="white", max_words=words).generate(output_final)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()







