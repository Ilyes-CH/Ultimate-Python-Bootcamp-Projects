import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df =  sns.load_dataset("titanic")

df_filtered = df[df['pclass'].isin([1,3])].copy()

df_filtered['class_label'] = df_filtered['pclass'].map({1:"High Class (1st)",3:"Low Class (3rd)"})

print(df_filtered)

plt.figure(figsize=(8,5))

sns.barplot(
    data=df_filtered,
    x='class_label',
    y='survived',
    ci=None
)

plt.title("Survival Rate By Passenger Class (Titanic)")
plt.ylabel("Survival Rate (0 = Died, 1 = Survived)")
plt.xlabel("Passenger Class")
plt.ylim(0,1)

plt.show()