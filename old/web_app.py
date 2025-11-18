import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Streamlitのタイトル
st.title('Streamlit Matplotlib Example')

# スライダーでパラメータを操作できるようにする
frequency = st.slider('Frequency', 1, 10, 3)

# グラフの生成
x = np.linspace(0, 10, 500)
y = np.sin(x * frequency)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title(f'Sin Wave with Frequency {frequency}')

# Streamlitにグラフを表示
st.pyplot(fig)