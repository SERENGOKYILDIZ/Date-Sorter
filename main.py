#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date Sorter - Dosya Sıralama Programı
Ana uygulama dosyası
"""

from tkinter import messagebox
from ui import DateSorterUI

if __name__ == "__main__":
    try:
        app = DateSorterUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Hata", f"Uygulama hatası: {str(e)}")
