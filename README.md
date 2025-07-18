# CKAN\_WRI

Learn Scripting and Importing Excel data into CKAN dataset using CKAN API



pip install ckanapi
import pandas as pd
from ckanapi import RemoteCKAN

#konfigurasi API CKAN
CKAN\_URL = 'https://catalog.wri-indonesia.id/'
CKAN\_API\_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3MXVsMURqeXFmUExDODB3ZHlONi1BMjhxdWxTNFY2ckVRQ1EwM2J3VkM0IiwiaWF0IjoxNzUyNzc2NzEzfQ.jG1Kl1CfZ1izQGlROrd2WJhPuKORzv96YgQLb8TtSm0'



# File Excel

df = pd.read\_excel('C:\\WRI\\Formulir Pengumpulan Data.xlsx', sheet\_name = 'Form')
df.head()

df.info()



# inisialisasi koneksi ke CKAN

ckan = RemoteCKAN(CKAN\_URL, apikey=CKAN\_API\_KEY)



# Loop data untuk mengirim ke CKAN

for idx, row in df.iterrows():
# Make sure tiap row valid
if pd.notnull(row.get('Judul')) and pd.notnull(row.get('Kode Proyek')):
dataset\_name = f"{row\['Judul'].replace(' ', '\_').lower()}-{row\['Kode Proyek']}"
#Payload untuk CKAN
payload = {
"name": dataset\_name,
"title": row\['Judul'],
"notes": row.get('Deskripsi', ''),
"tags": \[{"name": tag.strip()} for tag in row.get('Tags', '').split(',') if tag.strip()],
"license\_id": row.get('Lisensi Data / Ketentuan Penggunaan', ''),
"owner\_org": 'c9608663-1cf9-490b-9d16-2cf06eeed63e', #row.get('Afiliasi Proyek/Program/Organisasi', ''),
"private": False if str(row\["Visibility"]).strip().lower() == "public" else True,
"url": row.get('URL', ''),
"version": str(row.get('Tahun', '')) if pd.notnull(row.get('Tahun')) else '',
"author": row.get('Nama Lengkap', ''),
"author\_email": row.get('Email', ''),
"maintainer": 'Rian Prasetyo',
"maintainer\_email": '',
"extras": \[
{"key": 'custom\_id', "value": row.get('ID')},
{"key": 'kode\_proyek', "value": row.get('Kode Proyek')},
{"key": 'Kategori\_lain', "value": row.get('Kategori (Other)')},
{"key": 'cakupan\_geografi', "value": row.get('Cakupan geografi', '')},
{"key": 'sumber\_data', "value": row.get('Sumber Data/Pengelola/Walidata')},
{"key": 'Sitasi/DOI', "value": row.get('Sitasi/DOI', '')},
{"key": 'skala', "value": row.get('Skala atau resolusi spasial (Optional)', '')},
{"key": 'tipe\_data', "value": row.get('Tipe dan format data (Opsional) ', '')},
{"key": 'unit\_ukur', "value": row.get('Unit pengukuran (Opsional)', '')},
{"key": "penafian", "value": row.get('Penafian (disclaimer) penggunaan data (Opsional)', '')},
{"key": 'file\_lisensi', "value": row.get('Lampirkan file lisensi', '')},
{"key": 'bahasa', "value": row.get('Bahasa', '')},
{"key": 'tim', "value": row.get('Tim', '')},
{"key": 'aplikasi', "value": row.get('Aplikasi', '')},
{"key": 'frekuensi\_update', "value": row.get('Frekuensi Update', '')},
{"key": 'technical\_notes', "value": row.get('Technical Notes', '')},
{"key": 'temporal\_coverage', "value": row.get('Temporal Coverage', '')},
]
}
try:
result = ckan.action.package\_create(\*\*payload)
print(f"Dataset '{row\['Judul']} berhasil diinput: {result.get('id', 'Gagal')}")
except Exception as e:
print(f"Gagal input '{row\['Judul']}': {str(e)}")

