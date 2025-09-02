#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date Sorter v1.0 - File Date Management Tool
Ana uygulama dosyası

Author: Semi Eren Gökyıldız
Email: gokyildizsemieren@gmail.com
GitHub: https://github.com/SERENGOKYILDIZ
LinkedIn: https://www.linkedin.com/in/semi-eren-gokyildiz/
"""

__version__ = "1.0.0"
__author__ = "Semi Eren Gökyıldız"
__email__ = "gokyildizsemieren@gmail.com"

from tkinter import messagebox
from ui import DateSorterUI

if __name__ == "__main__":
    try:
        app = DateSorterUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Hata", f"Uygulama hatası: {str(e)}")
