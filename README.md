
# Data Loader to CKAN
## Preparation
Scripting and Importing Excel data into CKAN dataset using CKAN API

Create python env

    conda create --name ckan-data-loader python=3.12
    conda activate ckan-data-loader
    pip install -r requirements.txt


## API configuration
.env file

    CKAN_URL=https://catalog.wri-indonesia.id/
    CKAN_API_KEY=
    TIMEOUT=30
    CKAN_OWNER_ORG=
    CKAN_MAINTAINER=admin
    CKAN_MAINTAINER_EMAIL=admin@example.com
    DATA_SOURCE=C:\\Formulir Pengumpulan Data dibimbing.xlsx
    EXCEL_SHEET=Form

## Load Data
To check connection and data load before actually store the data, use:

    DRY_RUN= True

If all checks and tests have no issue, you can use

    DRY_RUN= False

 To actually store the data