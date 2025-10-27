# Excel Solver - Workbook included (TokoKita)

File: excel/excel_solver_ready.xlsx

Sheet 'Model' contains:
- Tabel biaya (W1..W2 vs S1..S4)
- Range untuk variabel keputusan x (B6:E7)
- Rumus supply terpakai (B9:B10)
- Rumus demand terpenuhi (C12:F12)
- Sel Objective (total biaya) di sel H6 = SUMPRODUCT(cost_range, x_range)

Cara menjalankan Solver (Excel):
1. Buka tab Data → Solver.
2. Set Objective: H6 -> Min.
3. By Changing Variable Cells: B6:E7.
4. Tambah constraints:
   - B9 <= capacity W1 (cell H9)
   - B10 <= capacity W2 (cell H10)
   - C12 = demand S1 (cell H13), ... dst untuk setiap toko
   - B6:E7 >= 0 (Make Unconstrained Variables Non-Negative)
5. Pilih Solving Method: Simplex LP.
6. Klik Solve.
