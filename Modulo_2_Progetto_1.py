import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


# CREAZIONE DATASET CON ERRORI

np.random.seed(42)

n = 1500
prodotti = ["T-shirt", "Cappello", "Sciarpa", "Pantalone", "Calze", "Maglione"]
date = pd.date_range(start="2026-01-01", end="2026-02-20")

df = pd.DataFrame({
    "Data": np.random.choice(date, n),
    "Prodotto": np.random.choice(prodotti, n),
    "Quantità": np.random.randint(1, 100, n),
    "Prezzo": np.round(np.random.uniform(5, 50, n), 2)
})

# Valori mancanti
for col in ["Quantità", "Prezzo"]:
    df.loc[np.random.choice(df.index, 50), col] = np.nan

# Date errate
df.loc[np.random.choice(df.index, 20), "Data"] = "data_errata"

# Quantità negative
df.loc[np.random.choice(df.index, 20), "Quantità"] = -10

# Prezzi come stringa
df.loc[np.random.choice(df.index, 20), "Prezzo"] = "errore"

# Prodotti inesistenti
df.loc[np.random.choice(df.index, 20), "Prodotto"] = "???"

# Duplicati
duplicati = df.sample(30)
df = pd.concat([df, duplicati], ignore_index=True)

# Quantità come stringa
df.loc[np.random.choice(df.index, 20), "Quantità"] = "N/A"

df.to_csv("Vendite.csv", index=False)


# CONSEGNA
# Parte 1 - Caricamento e esplorazione dati

df = pd.read_csv("Vendite.csv")

print("Prime 5 righe:")
print(df.head())

print("\nInfo dataset:")
print(df.info())

print("\nStatistiche descrittive:")
print(df.describe(include="all"))


# Parte 2 - Pulizia

# Conversione tipi
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
df["Quantità"] = pd.to_numeric(df["Quantità"], errors="coerce")
df["Prezzo"] = pd.to_numeric(df["Prezzo"], errors="coerce")

# Rimozione quantità negative
df.loc[df["Quantità"] < 0, "Quantità"] = np.nan

# Gestione valori mancanti
df["Quantità"] = df["Quantità"].fillna(0)
df["Prezzo"] = df["Prezzo"].fillna(df["Prezzo"].mean())

# Rimozione date non valide
df = df.dropna(subset=["Data"])

# Rimozione prodotti inesistenti
df = df[df["Prodotto"] != "???"]

# Rimozione duplicati
df = df.drop_duplicates()

print("\nDataset dopo pulizia:", df.shape)
print(df.info())

# Parte 3 - Analisi esplorativa

vendite_prodotto = df.groupby("Prodotto")["Quantità"].sum()

print("\nVendite totali per prodotto:")
print(vendite_prodotto)

print("\nProdotto più venduto:", vendite_prodotto.idxmax())
print("Prodotto meno venduto:", vendite_prodotto.idxmin())

# Vendite giornaliere
vendite_giornaliere = df.groupby("Data")["Quantità"].sum().sort_index()

vendite_medie_giornaliere = vendite_giornaliere.mean()
print("\nVendite medie giornaliere:", vendite_medie_giornaliere)


# EXTRA - Visualizzazione

plt.rcParams.update({
    "figure.figsize": (14, 8),
    "axes.grid": False,
    "font.size": 11
})

media_mobile_7 = vendite_giornaliere.rolling(7).mean()
media_mobile_14 = vendite_giornaliere.rolling(14).mean()

fig, axes = plt.subplots(2, 1)
fig.suptitle("Analisi vendite", fontsize=16, fontweight="bold")

axes[0].plot(vendite_giornaliere, linewidth=2, label="Vendite")
axes[0].plot(media_mobile_7, linestyle="--", label="MM 7")
axes[0].plot(media_mobile_14, linestyle=":", label="MM 14")
axes[0].set_title("Andamento vendite")
axes[0].legend(frameon=False)

vendite_prodotto.plot(
    kind="bar",
    ax=axes[1]
)
axes[1].set_title("Vendite per prodotto")

for spine in ["top", "right"]:
    axes[0].spines[spine].set_visible(False)
    axes[1].spines[spine].set_visible(False)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()


