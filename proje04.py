from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import tkinter as tk

df = pd.read_csv('all_stocks_5yr.csv')

df.dropna(inplace=True)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

df['day_of_week'] = df.index.dayofweek
df['month'] = df.index.month
df['year'] = df.index.year-2000

X = df[['day_of_week', 'month', 'year', 'open']].values
Y = df['close']

X_weights = [3, 1, 3, 1]
X = np.multiply(X, X_weights)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)

def predict():
    day_of_week = int(day_of_week_entry.get())
    month = int(month_entry.get())
    year = int(year_entry.get())-2000
    open_price = float(open_price_entry.get())

    closing_value = model.predict([[day_of_week, month, year, open_price]])
    result_label.config(text=f'Öngörülmüş Kapanış Stok Değeri: {float(closing_value):.2f}')

root = tk.Tk()
root.title("Hisse Değeri Tahmincisi")

r2 = model.score(X_test, Y_test)
mse = mean_squared_error(Y_test, Y_pred)

r2_label = tk.Label(root, text=f'Belirleme Katsayısı (R^2): {r2:.2f}')
r2_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

mse_label = tk.Label(root, text=f'Ortalama Hata Karesi: {mse:.2f}')
mse_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

day_of_week_label = tk.Label(root, text="Haftanın Gününü Giriniz (0=Pzt, 1=Salı vb.))")
day_of_week_label.grid(row=2, column=0, padx=5, pady=5)

day_of_week_entry = tk.Entry(root)
day_of_week_entry.grid(row=2, column=1, padx=5, pady=5)

month_label = tk.Label(root, text="Ayı Girin (1-12)")
month_label.grid(row=3, column=0, padx=5, pady=5)

month_entry = tk.Entry(root)
month_entry.grid(row=3, column=1, padx=5, pady=5)

year_label = tk.Label(root, text="Yılı Girin")
year_label.grid(row=4, column=0, padx=5, pady=5)

year_entry = tk.Entry(root)
year_entry.grid(row=4, column=1, padx=5, pady=5)

open_price_label = tk.Label(root, text="Açılış Piyasa Fiyatını Girin")
open_price_label.grid(row=5, column=0, padx=5, pady=5)

open_price_entry = tk.Entry(root)
open_price_entry.grid(row=5, column=1, padx=5, pady=5)

predict_button = tk.Button(root, text="Tahmin", command=predict)
predict_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

result_label = tk.Label(root)
result_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

exit_button = tk.Button(root, text="Çıkış", command=root.destroy, bg='red')
exit_button.grid(row=6,column=1, columnspan=2, padx=5, pady=5)

root.mainloop()
