import tkinter as tk 
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import font_manager

class ỨngDụngKruskal:
    def __init__(self, cửa_sổ):
        self.cửa_sổ = cửa_sổ
        self.cửa_sổ.title("Mô phỏng Thuật toán Kruskal")

        self.ds_cạnh = []  # Danh sách các cạnh
        self.đồ_thị = nx.Graph()  # Đồ thị

        # Giao diện nhập liệu
        tk.Label(cửa_sổ, text="Nhập số lượng đỉnh:", font=("Times New Roman", 19)).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.nhập_số_đỉnh = tk.Entry(cửa_sổ, font=("Times New Roman", 19), width=20)
        self.nhập_số_đỉnh.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(cửa_sổ, text="Nhập số lượng cạnh:", font=("Times New Roman", 19)).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.nhập_số_cạnh = tk.Entry(cửa_sổ, font=("Times New Roman", 19), width=20)
        self.nhập_số_cạnh.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(cửa_sổ, text="Tạo các cạnh", font=("Times New Roman", 19), command=self.tạo_nhập_liệu_cạnh, bg='green', fg='white').grid(row=2, column=0, columnspan=2, pady=10)

        self.nút_làm_mới = tk.Button(cửa_sổ, text="Làm Mới", font=("Times New Roman", 19), command=self.làm_mới, bg='blue', fg='white')
        self.nút_làm_mới.grid(row=9, column=0, columnspan=2, pady=10)
        self.nút_làm_mới.grid_forget()  # Ẩn nút làm mới ban đầu

        self.khung_cạnh = None
        self.hiển_thị_ds_cạnh = None
        self.hiển_thị_kết_quả = None

        self.hình, self.trục = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.hình, master=self.cửa_sổ)
        self.canvas.get_tk_widget().grid(row=3, column=2, rowspan=6, padx=10, pady=10)
        self.canvas.get_tk_widget().grid_forget()

        self.mst_hình, self.mst_trục = plt.subplots(figsize=(7, 7))
        self.mst_canvas = FigureCanvasTkAgg(self.mst_hình, master=self.cửa_sổ)
        self.mst_canvas.get_tk_widget().grid(row=3, column=3, rowspan=6, padx=10, pady=10)
        self.mst_canvas.get_tk_widget().grid_forget()

        self.nhập_số_đỉnh.focus_set()

    def tạo_nhập_liệu_cạnh(self):
        try:
            self.số_đỉnh = int(self.nhập_số_đỉnh.get())
            self.số_cạnh = int(self.nhập_số_cạnh.get())
            if self.số_đỉnh <= 0 or self.số_cạnh <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên dương cho số lượng đỉnh và cạnh.")
            return

        if self.khung_cạnh:
            self.khung_cạnh.destroy()

        self.khung_cạnh = tk.Frame(self.cửa_sổ)
        self.khung_cạnh.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.khung_cạnh, text="Nhập cạnh u v w (vd: 0 1 3)\n*Nhấn Enter để tạo cạnh*", font=("Times New Roman", 19)).pack(pady=5)
        self.nhập_cạnh = tk.Entry(self.khung_cạnh, font=("Times New Roman", 19), width=30)
        self.nhập_cạnh.pack(pady=5)
        self.nhập_cạnh.bind("<Return>", self.thêm_cạnh)

        self.hiển_thị_ds_cạnh = tk.Text(self.khung_cạnh, height=10, width=35, font=("Times New Roman", 19), state="disabled")
        self.hiển_thị_ds_cạnh.pack(pady=5)

        self.hiển_thị_kết_quả = tk.Text(self.khung_cạnh, height=10, width=35, font=("Times New Roman", 19), state="disabled")
        self.hiển_thị_kết_quả.pack(pady=5)

        tk.Button(self.khung_cạnh, text="Tìm MST", font=("Times New Roman", 19), command=self.tìm_cây_khung_nhỏ_nhất, bg='red', fg='white').pack(pady=10)

        self.nút_làm_mới.grid(row=9, column=0, columnspan=2, pady=10)
        self.vẽ_đồ_thị_ban_đầu()
        self.canvas.get_tk_widget().grid(row=3, column=2, rowspan=6, padx=10, pady=10)
        self.mst_canvas.get_tk_widget().grid(row=3, column=3, rowspan=6, padx=10, pady=10)

    def vẽ_đồ_thị_ban_đầu(self):
        self.đồ_thị.clear()
        self.ds_cạnh = []
        vị_trí = self.bố_trí_đỉnh()

        self.trục.clear()
        for i in range(self.số_đỉnh):
            self.trục.plot(vị_trí[i][0], vị_trí[i][1], 'bo', markersize=16)
            self.trục.text(vị_trí[i][0], vị_trí[i][1], f'{i}', fontsize=15, ha='center', va='center', color='white', fontproperties=font_manager.FontProperties(family="Times New Roman"))

        self.trục.set_axis_off()
        self.trục.set_title("Đồ thị vô hướng với trọng số", fontproperties=font_manager.FontProperties(family="Times New Roman", size=16))
        self.canvas.draw()

    def bố_trí_đỉnh(self):
        vị_trí = {}
        góc = 2 * np.pi / self.số_đỉnh
        bán_kính = 1.5
        for i in range(self.số_đỉnh):
            x = bán_kính * np.cos(i * góc)
            y = bán_kính * np.sin(i * góc)
            vị_trí[i] = (x, y)
        return vị_trí

    def thêm_cạnh(self, event):
        if len(self.ds_cạnh) >= self.số_cạnh:
            messagebox.showerror("Lỗi", "Đã đạt số lượng cạnh tối đa.")
            return

        dữ_liệu_cạnh = self.nhập_cạnh.get().strip()
        try:
            u, v, w = map(int, dữ_liệu_cạnh.split())
            if u < 0 or v < 0 or w < 0 or u >= self.số_đỉnh or v >= self.số_đỉnh or u == v:
                raise ValueError("Cạnh không hợp lệ. u và v phải khác nhau.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu cạnh hợp lệ (vd: 0 1 3, u ≠ v).")
            return

        cạnh = tuple(sorted((u, v)))
        if cạnh in [tuple(sorted((x[0], x[1]))) for x in self.ds_cạnh]:
            messagebox.showerror("Lỗi", "Cạnh đã tồn tại.")
            return

        self.ds_cạnh.append((u, v, w))
        self.đồ_thị.add_edge(u, v, weight=w)
        self.hiển_thị_ds_cạnh.config(state="normal")
        self.hiển_thị_ds_cạnh.insert(tk.END, f"{u} -- {v} = {w}\n")
        self.hiển_thị_ds_cạnh.config(state="disabled")
        self.nhập_cạnh.delete(0, tk.END)

        self.vẽ_cạnh(u, v, w)

    def vẽ_cạnh(self, u, v, w):
        vị_trí = self.bố_trí_đỉnh()
        x_đỉnh = [vị_trí[u][0], vị_trí[v][0]]
        y_đỉnh = [vị_trí[u][1], vị_trí[v][1]]
        self.trục.plot(x_đỉnh, y_đỉnh, 'k-', lw=2)

        giữa_x = (vị_trí[u][0] + vị_trí[v][0]) / 2
        giữa_y = (vị_trí[u][1] + vị_trí[v][1]) / 2
        tựa = 0.1
        góc = np.arctan2(vị_trí[v][1] - vị_trí[u][1], vị_trí[v][0] - vị_trí[u][0])
        tựa_x = giữa_x + tựa * np.cos(góc + np.pi / 2)
        tựa_y = giữa_y + tựa * np.sin(góc + np.pi / 2)

        self.trục.text(tựa_x, tựa_y, f'{w}', fontsize=16, ha='center', va='center', color='green', fontproperties=font_manager.FontProperties(family="Times New Roman"))
        self.canvas.draw()

    def tìm_cây_khung_nhỏ_nhất(self):
        if len(self.ds_cạnh) != self.số_cạnh:
            messagebox.showerror("Lỗi", f"Số lượng cạnh bạn đã nhập chưa đủ. Vui lòng nhập đúng {self.số_cạnh} cạnh.")
            return

        mst = nx.minimum_spanning_tree(self.đồ_thị)
        kết_quả = "Các cạnh trong MST:\n"
        tổng_trọng_số = 0
        for u, v, dữ_liệu in mst.edges(data=True):
            kết_quả += f"{u} -- {v} = {dữ_liệu['weight']}\n"
            tổng_trọng_số += dữ_liệu['weight']
        kết_quả += f"\nTổng trọng số MST: {tổng_trọng_số}"

        self.hiển_thị_kết_quả.config(state="normal")
        self.hiển_thị_kết_quả.delete(1.0, tk.END)
        self.hiển_thị_kết_quả.insert(tk.END, kết_quả)
        self.hiển_thị_kết_quả.config(state="disabled")

        self.vẽ_cây_khung_nhỏ_nhất(mst)

    def vẽ_cây_khung_nhỏ_nhất(self, mst):
        self.mst_trục.clear()
        vị_trí = self.bố_trí_đỉnh()
        
        for u, v, dữ_liệu in self.đồ_thị.edges(data=True):
            x_đỉnh = [vị_trí[u][0], vị_trí[v][0]]
            y_đỉnh = [vị_trí[u][1], vị_trí[v][1]]
            
            # Color edges based on whether they are part of the MST or not
            màu = 'r' if mst.has_edge(u, v) else 'k'
            self.mst_trục.plot(x_đỉnh, y_đỉnh, color=màu, lw=2)

            # Draw weights for both MST and non-MST edges
            giữa_x = (vị_trí[u][0] + vị_trí[v][0]) / 2
            giữa_y = (vị_trí[u][1] + vị_trí[v][1]) / 2
            tựa = 0.1
            góc = np.arctan2(vị_trí[v][1] - vị_trí[u][1], vị_trí[v][0] - vị_trí[u][0])
            tựa_x = giữa_x + tựa * np.cos(góc + np.pi / 2)
            tựa_y = giữa_y + tựa * np.sin(góc + np.pi / 2)
            
            trọng_số = dữ_liệu['weight']
            màu_trọng_số = 'red' if mst.has_edge(u, v) else 'green'
            self.mst_trục.text(tựa_x, tựa_y, f'{trọng_số}', fontsize=16, ha='center', va='center', color= màu_trọng_số, fontproperties=font_manager.FontProperties(family="Times New Roman"))
        
        for i in range(self.số_đỉnh):
            self.mst_trục.plot(vị_trí[i][0], vị_trí[i][1], 'bo', markersize=16)
            self.mst_trục.text(vị_trí[i][0], vị_trí[i][1], f'{i}', fontsize=15, ha='center', va='center', color='white', fontproperties=font_manager.FontProperties(family="Times New Roman"))

        self.mst_trục.set_axis_off()
        self.mst_trục.set_title("Cây khung nhỏ nhất (MST)", fontproperties=font_manager.FontProperties(family="Times New Roman", size=16))
        self.mst_canvas.draw()
  
    def làm_mới(self):
        self.ds_cạnh = []
        self.đồ_thị.clear()
        if self.hiển_thị_ds_cạnh:
            self.hiển_thị_ds_cạnh.config(state="normal")
            self.hiển_thị_ds_cạnh.delete(1.0, tk.END)
            self.hiển_thị_ds_cạnh.config(state="disabled")

        if self.hiển_thị_kết_quả:
            self.hiển_thị_kết_quả.config(state="normal")
            self.hiển_thị_kết_quả.delete(1.0, tk.END)
            self.hiển_thị_kết_quả.config(state="disabled")

        self.nhập_số_đỉnh.delete(0, tk.END)
        self.nhập_số_cạnh.delete(0, tk.END)
        self.nhập_cạnh.delete(0, tk.END)

        self.khung_cạnh.destroy()
        self.canvas.get_tk_widget().grid_forget()
        self.mst_canvas.get_tk_widget().grid_forget()
        self.nhập_số_đỉnh.focus_set()

if __name__ == "__main__":
    cửa_sổ_chính = tk.Tk()
    ứng_dụng = ỨngDụngKruskal(cửa_sổ_chính)
    cửa_sổ_chính.mainloop()    