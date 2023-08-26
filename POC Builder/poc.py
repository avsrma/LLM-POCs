import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data
data = {
    "A": np.random.rand(10),
    "B": np.random.rand(10),
    "C": np.random.rand(10),
    "D": np.random.rand(10),
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.title("Sample Streamlit App")

st.header("Dataframe")
st.write(df)

st.header("Static Table")
st.table(df)

st.header("Line Chart")
fig, ax = plt.subplots()
ax.plot(df.index, df["A"], label="A")
ax.plot(df.index, df["B"], label="B")
ax.plot(df.index, df["C"], label="C")
ax.plot(df.index, df["D"], label="D")
ax.set_xlabel("Index")
ax.set_ylabel("Values")
ax.set_title("Line Chart")
ax.legend()
st.pyplot(fig)

st.header("Scatterplot")
fig2, ax2 = plt.subplots()
ax2.scatter(df["A"], df["B"], label="A vs B")
ax2.scatter(df["C"], df["D"], label="C vs D")
ax2.set_xlabel("X-axis")
ax2.set_ylabel("Y-axis")
ax2.set_title("Scatterplot")
ax2.legend()
st.pyplot(fig2)
