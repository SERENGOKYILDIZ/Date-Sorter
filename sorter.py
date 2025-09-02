#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date Sorter - Dosya Sıralama ve Tarih Değiştirme
Dosya işlemleri ve tarih hesaplama mantığı
"""

import os
import stat
from datetime import datetime, timedelta
import platform

class FileSorter:
    """Dosya sıralama ve tarih değiştirme sınıfı"""
    
    def __init__(self):
        # Windows uyumluluğu için 1980'den başla, saat 11:00 AM
        self.start_date = datetime(1980, 1, 1, 11, 0, 0)
        
    def set_start_date(self, year):
        """Başlangıç yılını ayarla (1 Ocak 11:00 AM)"""
        self.start_date = datetime(year, 1, 1, 11, 0, 0)
        
    def get_files(self, folder_path):
        """Klasördeki dosyaları al ve bilgilerini döndür"""
        files = []
        
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                # Sadece dosyaları al, klasörleri değil
                if os.path.isfile(file_path):
                    file_info = self.get_file_info(file_path)
                    files.append(file_info)
                    
        except PermissionError:
            raise Exception("Klasöre erişim izni yok")
        except Exception as e:
            raise Exception(f"Dosyalar okunurken hata: {str(e)}")
            
        # Dosyaları değişim tarihine göre sırala (en eski önce)
        files.sort(key=lambda x: x['datetime'])
        
        return files
        
    def get_file_info(self, file_path):
        """Dosya bilgilerini al"""
        try:
            stat_info = os.stat(file_path)
            
            # Dosya adı
            filename = os.path.basename(file_path)
            
            # Dosya boyutu
            size_bytes = stat_info.st_size
            size_str = self.format_file_size(size_bytes)
            
            # Değişim tarihi
            mod_time = stat_info.st_mtime
            mod_datetime = datetime.fromtimestamp(mod_time)
            date_str = mod_datetime.strftime("%d.%m.%Y %H:%M:%S")
            
            return {
                'name': filename,
                'size': size_bytes,  # Integer olarak döndür
                'date': mod_datetime,  # Datetime objesi olarak döndür
                'datetime': mod_datetime,
                'timestamp': mod_time,
                'path': file_path
            }
            
        except Exception as e:
            raise Exception(f"Dosya bilgileri alınırken hata ({file_path}): {str(e)}")
            
    def format_file_size(self, size_bytes):
        """Dosya boyutunu okunabilir formata çevir"""
        if size_bytes == 0:
            return "0 B"
            
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
            
        if i == 0:
            return f"{int(size)} {size_names[i]}"
        else:
            return f"{size:.1f} {size_names[i]}"
            
    def calculate_new_date(self, file_index):
        """Dosya indeksine göre yeni tarih hesapla"""
        # 1970'den başlayarak her dosya için 1 gün ilerle
        new_date = self.start_date + timedelta(days=file_index)
        return new_date
        
    def change_file_date(self, file_path, new_date):
        """Dosyanın değişim tarihini değiştir"""
        try:
            # Tarih geçerliliğini kontrol et
            min_date = datetime(1980, 1, 1)
            max_date = datetime(2099, 12, 31)
            
            if new_date < min_date:
                new_date = min_date
            elif new_date > max_date:
                new_date = max_date
            
            # Yeni tarihi timestamp'e çevir
            new_timestamp = new_date.timestamp()
            
            # Dosya var mı kontrol et
            if not os.path.exists(file_path):
                raise Exception(f"Dosya bulunamadı: {os.path.basename(file_path)}")
            
            # Dosya okunabilir mi kontrol et
            if not os.access(file_path, os.R_OK):
                raise Exception(f"Dosya okunamıyor: {os.path.basename(file_path)}")
            
            # Tarihi değiştir
            os.utime(file_path, (new_timestamp, new_timestamp))
                
        except PermissionError:
            raise Exception(f"Dosya tarihi değiştirme izni yok: {os.path.basename(file_path)}")
        except OSError as e:
            if e.errno == 22:  # Invalid argument
                raise Exception(f"Geçersiz tarih değeri: {os.path.basename(file_path)} (Tarih: {new_date.strftime('%d.%m.%Y')})")
            else:
                raise Exception(f"Dosya sistemi hatası ({os.path.basename(file_path)}): {str(e)}")
        except Exception as e:
            raise Exception(f"Dosya tarihi değiştirilemedi ({os.path.basename(file_path)}): {str(e)}")
            
    def validate_folder(self, folder_path):
        """Klasör geçerliliğini kontrol et"""
        if not os.path.exists(folder_path):
            return False, "Klasör bulunamadı"
            
        if not os.path.isdir(folder_path):
            return False, "Belirtilen yol bir klasör değil"
            
        if not os.access(folder_path, os.R_OK):
            return False, "Klasöre okuma izni yok"
            
        if not os.access(folder_path, os.W_OK):
            return False, "Klasöre yazma izni yok"
            
        return True, "Geçerli"
        
    def get_folder_stats(self, folder_path):
        """Klasör istatistiklerini al"""
        try:
            files = self.get_files(folder_path)
            
            total_files = len(files)
            total_size = 0
            
            for file_info in files:
                # Dosya boyutunu bytes olarak al
                file_path = file_info['path']
                total_size += os.path.getsize(file_path)
                
            return {
                'total_files': total_files,
                'total_size': self.format_file_size(total_size),
                'oldest_file': files[0]['date'] if files else "Yok",
                'newest_file': files[-1]['date'] if files else "Yok"
            }
            
        except Exception as e:
            raise Exception(f"Klasör istatistikleri alınırken hata: {str(e)}")
            
    def backup_file_dates(self, folder_path):
        """Dosya tarihlerini yedekle (opsiyonel özellik)"""
        try:
            files = self.get_files(folder_path)
            backup_data = []
            
            for file_info in files:
                backup_data.append({
                    'filename': file_info['name'],
                    'original_date': file_info['datetime'].isoformat(),
                    'timestamp': file_info['timestamp']
                })
                
            return backup_data
            
        except Exception as e:
            raise Exception(f"Tarih yedeği alınırken hata: {str(e)}")
            
    def restore_file_dates(self, folder_path, backup_data):
        """Dosya tarihlerini yedekten geri yükle (opsiyonel özellik)"""
        try:
            for backup_item in backup_data:
                file_path = os.path.join(folder_path, backup_item['filename'])
                
                if os.path.exists(file_path):
                    original_timestamp = backup_item['timestamp']
                    os.utime(file_path, (original_timestamp, original_timestamp))
                    
        except Exception as e:
            raise Exception(f"Tarih geri yüklenirken hata: {str(e)}")
