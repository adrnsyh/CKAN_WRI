from ckanapi import RemoteCKAN
from ckanapi.errors import NotFound
from dotenv import load_dotenv
import os
import pandas as pd
import logging
import traceback


# Load the .env file
load_dotenv()

# ENV values load
ckan_api_key = os.getenv('CKAN_API_KEY')
ckan_url = os.getenv('CKAN_URL')
timeout = os.getenv('TIMEOUT')
ckan_owner_org = os.getenv('CKAN_OWNER_ORG')
ckan_maintainer = os.getenv('CKAN_MAINTAINER')
ckan_maintainer_email = os.getenv('CKAN_MAINTAINER_EMAIL')
data_source = os.getenv('DATA_SOURCE')
sheet_name = os.getenv('EXCEL_SHEET', 'Form') 

# logging
logging.basicConfig(
    filename='upload_ckan.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# dry run mode
DRY_RUN = True 
df = pd.read_excel(data_source, sheet_name=sheet_name)

# Connect to CKAN
ckan = RemoteCKAN(ckan_url, apikey=ckan_api_key)

# Loop Through Rows and Push to CKAN
for idx, row in df.iterrows():
    try:
        judul = str(row.get('Judul', '')).strip()
        kode_proyek = str(row.get('Kode Proyek', '')).strip()

        if not judul or not kode_proyek:
            logging.warning(f"Skipping row {idx}: missing 'Judul' or 'Kode Proyek'")
            continue

        dataset_name = f"{judul.replace(' ', '_').lower()}-{kode_proyek}"

        # Check if dataset already exists
        try:
            ckan.action.package_show(id=dataset_name)
            logging.info(f"Dataset already exists: {dataset_name}. Skipping...")
            continue
        except NotFound:
            pass  # Safe to proceed

        # Prepare Payload
        payload = {
            "name": dataset_name,
            "title": judul,
            "notes": row.get('Deskripsi', ''),
            "tags": [{"name": tag.strip()} for tag in str(row.get('Tags', '')).split(',') if tag.strip()],
            "license_id": row.get('Lisensi Data / Ketentuan Penggunaan', ''),
            "owner_org": ckan_owner_org,
            "private": False if str(row.get("Visibility", "")).strip().lower() == "public" else True,
            "url": row.get('URL', ''),
            "version": str(row.get('Tahun', '')) if pd.notnull(row.get('Tahun')) else '',
            "author": row.get('Nama Lengkap', ''),
            "author_email": row.get('Email', ''),
            "maintainer": ckan_maintainer,
            "maintainer_email": ckan_maintainer_email,
            "extras": [
                {"key": 'custom_id', "value": row.get('ID')},
                {"key": 'kode_proyek', "value": row.get('Kode Proyek')},
                {"key": 'Kategori_lain', "value": row.get('Kategori (Other)')},
                {"key": 'cakupan_geografi', "value": row.get('Cakupan geografi', '')},
                {"key": 'sumber_data', "value": row.get('Sumber Data/Pengelola/Walidata')},
                {"key": 'Sitasi/DOI', "value": row.get('Sitasi/DOI', '')},
                {"key": 'skala', "value": row.get('Skala atau resolusi spasial (Optional)', '')},
                {"key": 'tipe_data', "value": row.get('Tipe dan format data (Opsional) ', '')},
                {"key": 'unit_ukur', "value": row.get('Unit pengukuran (Opsional)', '')},
                {"key": 'penafian', "value": row.get('Penafian (disclaimer) penggunaan data (Opsional)', '')},
                {"key": 'file_lisensi', "value": row.get('Lampirkan file lisensi', '')},
                {"key": 'bahasa', "value": row.get('Bahasa', '')},
                {"key": 'tim', "value": row.get('Tim', '')},
                {"key": 'aplikasi', "value": row.get('Aplikasi', '')},
                {"key": 'frekuensi_update', "value": row.get('Frekuensi Update', '')},
                {"key": 'technical_notes', "value": row.get('Technical Notes', '')},
                {"key": 'temporal_coverage', "value": row.get('Temporal Coverage', '')},
            ]
        }

        # Upload or Dry Run
        if DRY_RUN:
            logging.info(f"[Dry Run] Would create dataset: {dataset_name}")
            print(f"[Dry Run] Would create: {dataset_name}")
        else:
            result = ckan.action.package_create(**payload)
            logging.info(f"Dataset created: {judul} (ID: {result.get('id')})")
            print(f"Dataset '{judul}' berhasil diinput: {result.get('id')}")

    except Exception as e:
        logging.error(f"Failed to process row {idx} ({judul}): {str(e)}")
        traceback.print_exc()