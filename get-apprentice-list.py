import requests
from pathlib import Path
from pprint import pprint

api_key = Path('api-key.txt').read_text()

session = requests.Session()
session.headers.update({'Authorization': f'Bearer {api_key}'})

srs_systems = session.get('https://api.wanikani.com/v2/spaced_repetition_systems/').json()
apprentice_assignments = session.get('https://api.wanikani.com/v2/assignments', params={'srs_stages': '1,2,3,4'}).json()
apprentice_subject_ids = [str(x['data']['subject_id']) for x in apprentice_assignments['data']]
apprentice_subjects = session.get('https://api.wanikani.com/v2/subjects', params={'ids': ','.join(apprentice_subject_ids)}).json()
pprint(apprentice_subjects)