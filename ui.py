import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime, timedelta
import threading
from sorter import FileSorter

class DateSorterUI:
    def __init__(self):
        self.root = tk.Tk()
        self.file_sorter = FileSorter()
        self.files = []
        self.sort_column = 0
        self.sort_reverse = False
        self.setup_ui()
        
    def setup_ui(self):
        """Ana UI'yi oluştur"""
        self.root.title("Date Sorter")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")
        
        # Tam ekran başlat
        self.root.state('zoomed')
        
        # Ana container
        main_container = tk.Frame(self.root, bg="#2b2b2b")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Başlık
        title_label = tk.Label(
            main_container,
            text="📅 Date Sorter",
            font=("Segoe UI", 24, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        title_label.pack(pady=(0, 20))
        
        # Kontrol paneli
        self.setup_control_panel(main_container)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Klasör seçin...")
        status_bar = tk.Label(
            main_container,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg="#3c3c3c",
            fg="white",
            relief="sunken",
            bd=1
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Progress bar - status bar'ın altında
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_container,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        # Progress bar başlangıçta gizli
        
        # Dosya tablosu
        self.setup_file_table(main_container)
        
    def setup_control_panel(self, parent):
        """Kontrol panelini oluştur"""
        control_frame = tk.Frame(parent, bg="#3c3c3c", relief="raised", bd=2)
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Sol taraf - Klasör seçimi
        left_frame = tk.Frame(control_frame, bg="#3c3c3c")
        left_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        folder_label = tk.Label(
            left_frame,
            text="📁 Klasör:",
            font=("Segoe UI", 12, "bold"),
            bg="#3c3c3c",
            fg="white"
        )
        folder_label.pack(side="left")
        
        self.folder_var = tk.StringVar()
        folder_entry = tk.Entry(
            left_frame,
            textvariable=self.folder_var,
            font=("Segoe UI", 10),
            width=50,
            bg="#4a4a4a",
            fg="white",
            insertbackground="white"
        )
        folder_entry.pack(side="left", padx=(10, 5))
        
        browse_btn = tk.Button(
            left_frame,
            text="Gözat",
            command=self.browse_folder,
            font=("Segoe UI", 10, "bold"),
            bg="#0078d4",
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=5
        )
        browse_btn.pack(side="left")
        
        # Sağ taraf - Başlangıç yılı ve işlem butonu
        right_frame = tk.Frame(control_frame, bg="#3c3c3c")
        right_frame.pack(side="right", padx=10, pady=10)
        
        year_label = tk.Label(
            right_frame,
            text="📅 Başlangıç Yılı:",
            font=("Segoe UI", 12, "bold"),
            bg="#3c3c3c",
            fg="white"
        )
        year_label.pack(side="left")
        
        self.year_var = tk.StringVar(value="1980")
        year_entry = tk.Entry(
            right_frame,
            textvariable=self.year_var,
            font=("Segoe UI", 10),
            width=8,
            bg="#4a4a4a",
            fg="white",
            insertbackground="white"
        )
        year_entry.pack(side="left", padx=(10, 5))
        
        # Tooltip için year_entry'yi sakla
        self.year_entry = year_entry
        
        update_btn = tk.Button(
            right_frame,
            text="🔄 Tarihleri Güncelle",
            command=self.update_dates,
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=8
        )
        update_btn.pack(side="left", padx=(10, 0))
        
    def setup_file_table(self, parent):
        """Dosya tablosunu oluştur"""
        # Ana container
        table_frame = tk.Frame(parent, bg="#2b2b2b")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("#", "Dosya Adı", "Boyut", "Değişim Tarihi")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Treeview renklerini ayarla
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview renkleri
        style.configure("Treeview",
                       background="#3c3c3c",  # Arka plan gri
                       foreground="#e0e0e0",  # Yazı rengi açık gri
                       fieldbackground="#3c3c3c",  # Alan arka planı gri
                       borderwidth=0)
        
        # Header renkleri
        style.configure("Treeview.Heading",
                       background="#4a4a4a",  # Header arka planı koyu gri
                       foreground="#ffffff",  # Header yazı rengi beyaz
                       borderwidth=1,
                       relief="flat")
        
        # Seçili satır renkleri
        style.map("Treeview",
                 background=[('selected', '#0078d4')],  # Seçili satır mavi
                 foreground=[('selected', '#ffffff')])  # Seçili satır yazısı beyaz
        
        # Column ayarları
        self.tree.heading("#", text="#")
        self.tree.heading("Dosya Adı", text="Dosya Adı")
        self.tree.heading("Boyut", text="Boyut")
        self.tree.heading("Değişim Tarihi", text="Değişim Tarihi")
        
        self.tree.column("#", width=50, minwidth=50)
        self.tree.column("Dosya Adı", width=400, minwidth=200)
        self.tree.column("Boyut", width=100, minwidth=80)
        self.tree.column("Değişim Tarihi", width=150, minwidth=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Event bindings - Treeview'in kendi drag & drop'unu devre dışı bırak
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<B1-Motion>", self.on_tree_drag)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_drop)
        self.tree.bind("<Shift-Button-1>", self.on_tree_shift_click)
        
        # Treeview'in kendi drag & drop'unu devre dışı bırak
        self.tree.bind("<Motion>", self.on_tree_motion)
        
        # Header click bindings
        for col in columns:
            self.tree.heading(col, command=lambda c=col: self.sort_by_column(c))
        
        # Seçim durumu
        self.selected_items = set()
        self.last_clicked_item = None
        self.drag_start_item = None
        self.drag_start_y = None
        self.is_dragging = False
        self.ctrl_was_pressed = False
        
    def browse_folder(self):
        """Klasör seçme dialogu"""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            self.load_files()
            
    def load_files(self):
        """Dosyaları yükle"""
        folder = self.folder_var.get()
        if not folder:
            return
            
        try:
            self.files = self.file_sorter.get_files(folder)
            
            # Her dosyaya orijinal sıra numarasını ekle
            for i, file_info in enumerate(self.files):
                file_info['original_number'] = i + 1
                
            self.status_var.set(f"Yüklenen dosya sayısı: {len(self.files)}")
            self.refresh_file_display()
        except Exception as e:
            messagebox.showerror("Hata", f"Dosyalar yüklenirken hata: {str(e)}")
            
    def refresh_file_display(self):
        """Dosya listesini yeniden çiz"""
        # Treeview'i temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Dosyaları ekle - orijinal sıra numaralarını koru
        for i, file_info in enumerate(self.files):
            size_str = self.format_size(file_info['size'])
            date_str = file_info['date'].strftime("%d/%m/%Y %H:%M")
            
            # Orijinal sıra numarasını kullan (dosya bilgisinde saklanan)
            original_number = file_info.get('original_number', i + 1)
            
            self.tree.insert("", "end", values=(
                original_number,
                file_info['name'],
                size_str,
                date_str
            ))
            
    def format_size(self, size_bytes):
        """Dosya boyutunu formatla"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
        
    def on_tree_click(self, event):
        """Treeview'de tıklama"""
        item = self.tree.identify_row(event.y)
        if item:
            # CTRL tuşu basılı mı kontrol et
            ctrl_pressed = event.state & 0x4
            
            # Treeview'in kendi seçim sistemini engelle
            self.tree.selection_remove(self.tree.selection())
            
            if not ctrl_pressed:
                # Normal tıklama - tek seçim
                self.tree.selection_add(item)
                self.selected_items = {item}
            else:
                # CTRL + tıklama - çoklu seçim
                if item in self.selected_items:
                    # Zaten seçili - seçimi kaldır (sadece tek öğe seçiliyse)
                    if len(self.selected_items) > 1:
                        self.selected_items.remove(item)
                else:
                    # Seçili değil - seçime ekle
                    self.selected_items.add(item)
                    
                # CTRL + tıklama ile sürükleme yapılacaksa, tıklanan öğeyi her zaman dahil et
                if len(self.selected_items) > 0 and item not in self.selected_items:
                    self.selected_items.add(item)
            
            # Seçili item'ları görsel olarak güncelle
            for selected_item in self.selected_items:
                self.tree.selection_add(selected_item)
            
            # Drag başlangıcı - her durumda ayarla
            self.drag_start_item = item  # Son tıklanan item'ı kaydet
            self.drag_start_y = event.y_root
            self.last_clicked_item = item
            
            # CTRL durumunu kaydet (sürükleme sırasında kullanmak için)
            self.ctrl_was_pressed = ctrl_pressed
            
            print(f"Click: item={item}, ctrl={ctrl_pressed}, selected_count={len(self.selected_items)}")
            
    def on_tree_motion(self, event):
        """Mouse hareketi - Treeview'in kendi drag & drop'unu engelle"""
        return "break"
            

            
    def on_tree_shift_click(self, event):
        """Shift + tıklama ile aralık seçimi"""
        item = self.tree.identify_row(event.y)
        if item and self.last_clicked_item:
            # Treeview'in kendi seçim sistemini engelle
            self.tree.selection_remove(self.tree.selection())
            self.selected_items.clear()
            
            # Aralığı seç
            start_idx = self.tree.index(self.last_clicked_item)
            end_idx = self.tree.index(item)
            
            if start_idx > end_idx:
                start_idx, end_idx = end_idx, start_idx
                
            for i in range(start_idx, end_idx + 1):
                child_item = self.tree.get_children()[i]
                self.tree.selection_add(child_item)
                self.selected_items.add(child_item)
                
            print(f"Shift click: range {start_idx}-{end_idx}, selected_count={len(self.selected_items)}")
                
    def on_tree_drag(self, event):
        """Treeview'de sürükleme"""
        # Drag başlangıcı yoksa çık
        if self.drag_start_y is None:
            return
            
        # Drag mesafesini kontrol et
        drag_distance = abs(event.y_root - self.drag_start_y)
        if drag_distance > 5:
            self.is_dragging = True
            print(f"Drag started: distance={drag_distance}, selected_items={len(self.selected_items)}")
            # Treeview'in kendi drag & drop'unu engelle
            return "break"
            
    def on_tree_drop(self, event):
        """Treeview'de bırakma"""
        print(f"Drop event: is_dragging={self.is_dragging}, start={self.drag_start_item}")
        
        if not self.is_dragging:
            self.drag_start_item = None
            self.drag_start_y = None
            self.is_dragging = False
            return
            
        # Hedef item'ı bul
        target_item = self.tree.identify_row(event.y)
        print(f"Target item: {target_item}")
        
        if target_item:
            # Tıklama anındaki CTRL durumunu kullan (sürükleme sırasındaki değil)
            ctrl_was_pressed = getattr(self, 'ctrl_was_pressed', False)
            print(f"CTRL was pressed at click: {ctrl_was_pressed}, selected_items: {len(self.selected_items)}")
            
            # Dosyaları taşı
            if ctrl_was_pressed and len(self.selected_items) > 1:
                # CTRL + sürükleme - çoklu dosyaları sıralı şekilde taşı
                print("CTRL + sürükleme - sıralı taşıma")
                self.move_multiple_files_ordered(target_item)
            elif len(self.selected_items) > 1:
                # Normal çoklu seçim - toplu taşıma
                print("Normal çoklu taşıma")
                self.move_multiple_files(target_item)
            else:
                # Tek dosya taşıma
                print("Tek dosya taşıma")
                self.move_single_file(self.drag_start_item, target_item)
                
        # Drag durumunu temizle
        self.drag_start_item = None
        self.drag_start_y = None
        self.is_dragging = False
        self.ctrl_was_pressed = False
        
    def move_single_file(self, source_item, target_item):
        """Tek dosyayı taşı"""
        source_idx = self.tree.index(source_item)
        target_idx = self.tree.index(target_item)
        
        if source_idx != target_idx:
            # Dosyayı listede taşı
            file_to_move = self.files.pop(source_idx)
            self.files.insert(target_idx, file_to_move)
            
            # Treeview'i yenile
            self.refresh_file_display()
            
    def move_multiple_files(self, target_item):
        """Çoklu dosyaları taşı"""
        target_idx = self.tree.index(target_item)
        
        # Seçili dosyaları topla
        selected_files = []
        selected_indices = []
        
        for item in self.selected_items:
            idx = self.tree.index(item)
            selected_indices.append(idx)
            selected_files.append(self.files[idx])
            
        # İndeksleri sırala (büyükten küçüğe)
        selected_indices.sort(reverse=True)
        
        # Dosyaları listeden çıkar
        for idx in selected_indices:
            self.files.pop(idx)
            
        # Hedef pozisyona ekle
        for file_info in reversed(selected_files):
            self.files.insert(target_idx, file_info)
            
        # Treeview'i yenile
        self.refresh_file_display()
        
    def move_multiple_files_ordered(self, target_item):
        """Çoklu dosyaları sıralı şekilde taşı (CTRL + sürükleme)"""
        target_idx = self.tree.index(target_item)
        
        # Seçili dosyaları orijinal sıralarına göre topla
        selected_files = []
        selected_indices = []
        
        for item in self.selected_items:
            idx = self.tree.index(item)
            selected_indices.append(idx)
            selected_files.append(self.files[idx])
            
        # Orijinal sıralarına göre sırala (küçükten büyüğe)
        selected_files.sort(key=lambda x: x.get('original_number', 0))
        
        # İndeksleri sırala (büyükten küçüğe)
        selected_indices.sort(reverse=True)
        
        # Dosyaları listeden çıkar
        for idx in selected_indices:
            self.files.pop(idx)
            
        # Hedef pozisyona sıralı şekilde ekle
        for file_info in selected_files:
            self.files.insert(target_idx, file_info)
            target_idx += 1
            
        # Treeview'i yenile
        self.refresh_file_display()
        
    def sort_by_column(self, column):
        """Kolon'a göre sırala"""
        if column == "#":
            # Sıra numarasına göre sıralama (orijinal sıra)
            pass
        elif column == "Dosya Adı":
            self.files.sort(key=lambda x: x['name'].lower(), reverse=self.sort_reverse)
        elif column == "Boyut":
            self.files.sort(key=lambda x: x['size'], reverse=self.sort_reverse)
        elif column == "Değişim Tarihi":
            self.files.sort(key=lambda x: x['date'], reverse=self.sort_reverse)
            
        self.sort_reverse = not self.sort_reverse
        self.refresh_file_display()
        
    def update_dates(self):
        """Dosya tarihlerini güncelle"""
        if not self.files:
            messagebox.showwarning("Uyarı", "Önce dosyaları yükleyin!")
            return
            
        try:
            year = int(self.year_var.get())
            if year < 1970 or year > 2030:
                raise ValueError("Yıl 1970-2030 arasında olmalı")
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz yıl: {str(e)}")
            return
            
        # Progress bar'ı göster
        self.progress_var.set(0)
        self.progress_bar.pack(pady=(5, 10))
        
        # Thread'de çalıştır
        thread = threading.Thread(target=self._update_dates_thread, args=(year,))
        thread.daemon = True
        thread.start()
        
    def _update_dates_thread(self, year):
        """Tarih güncelleme thread'i"""
        try:
            total_files = len(self.files)
            start_date = datetime(year, 1, 1, 11, 0)  # 11:00 AM başlangıç
            
            for i, file_info in enumerate(self.files):
                # Progress güncelle
                progress = (i / total_files) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                
                # Status güncelle
                if i % 10 == 0 or i == total_files - 1:  # Her 10 dosyada bir veya son dosyada
                    self.root.after(0, lambda idx=i, total=total_files: 
                        self.status_var.set(f"📅 Tarihler güncelleniyor... {idx + 1}/{total} dosya işlendi"))
                
                # Tarih güncelle
                new_date = start_date + timedelta(days=i)
                self.file_sorter.change_file_date(file_info['path'], new_date)
                
            # Tamamlandı
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.progress_bar.pack_forget())
            self.root.after(0, lambda: self.status_var.set(f"✅ Tarihler güncellendi! {total_files} dosya işlendi. Yeni sıralama yapılıyor..."))
            
            # Dosyaları yeniden yükle ve tarihe göre sırala
            self.root.after(0, self._reload_and_sort)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Tarih güncelleme hatası: {str(e)}"))
            self.root.after(0, lambda: self.progress_bar.pack_forget())
            
    def _reload_and_sort(self):
        """Dosyaları yeniden yükle ve tarihe göre sırala"""
        folder = self.folder_var.get()
        if folder:
            # Orijinal numaraları sakla (sadece referans için)
            original_numbers = {}
            for i, file_info in enumerate(self.files):
                original_numbers[file_info['name']] = file_info.get('original_number', i + 1)
            
            self.files = self.file_sorter.get_files(folder)
            
            # Tarihe göre sırala
            self.files.sort(key=lambda x: x['date'])
            
            # Yeni sıralamaya göre numaralandırmayı güncelle
            for i, file_info in enumerate(self.files):
                file_info['original_number'] = i + 1
            
            self.refresh_file_display()
            
            # Sıralama tamamlandı mesajı
            self.status_var.set(f"🎉 İşlem tamamlandı! {len(self.files)} dosya yeni tarihlere göre sıralandı.")
            
    def run(self):
        """Uygulamayı başlat"""
        self.root.mainloop()