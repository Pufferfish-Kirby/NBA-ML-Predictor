from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

dataset = 'eoinamoore/historical-nba-data-and-player-box-scores'

api.dataset_download_files(dataset, path='data', unzip=True)

print('dataset downloaded')