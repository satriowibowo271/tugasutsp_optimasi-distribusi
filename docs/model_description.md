# Model Distribusi (Transportation Problem) - TokoKita

## Variabel keputusan
x_{i,j} = jumlah unit dikirim dari gudang i ke toko j (i ∈ {W1, W2}, j ∈ {S1..S4})

## Fungsi tujuan
Minimalkan Z = Σ_{i,j} c_{i,j} * x_{i,j}
dimana c_{i,j} adalah biaya per unit dari gudang i ke toko j.

## Kendala
1. Permintaan tiap toko harus dipenuhi:
   Σ_{i} x_{i,j} = demand_j   untuk setiap j

2. Kapasitas gudang tidak boleh terlampaui:
   Σ_{j} x_{i,j} ≤ capacity_i   untuk setiap i

3. Non-negatif:
   x_{i,j} ≥ 0 untuk semua i,j

## Varian model di repo
- continuous: variable x continuous (default)
- integer: x integer (optimize_transportation_integer.py)
- fixed-cost: ada biaya tetap per gudang yang dipakai (optimize_transportation_fixedcost.py)

## Catatan
Total supply = 100 + 150 = 250
Total demand = 80 + 60 + 50 + 40 = 230
