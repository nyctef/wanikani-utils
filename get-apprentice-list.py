import requests
from pathlib import Path
from pprint import pprint
import json

api_key = Path('api-key.txt').read_text()

session = requests.Session()
session.headers.update({'Authorization': f'Bearer {api_key}'})

path_apprentice_subjects = Path('cache/apprentice_subjects.json')

def download_apprentice_subjects():
    # srs_systems = session.get('https://api.wanikani.com/v2/spaced_repetition_systems/').json()
    apprentice_assignments = session.get('https://api.wanikani.com/v2/assignments', params={'srs_stages': '1,2,3,4'}).json()
    apprentice_subject_ids = [str(x['data']['subject_id']) for x in apprentice_assignments['data']]
    apprentice_subjects = session.get('https://api.wanikani.com/v2/subjects', params={'ids': ','.join(apprentice_subject_ids)}).text
    path_apprentice_subjects.write_text(apprentice_subjects, encoding='utf8')

def convert_subjects_to_anki():
    apprentice_subjects_json = path_apprentice_subjects.read_text(encoding='utf8')
    apprentice_subjects = json.loads(apprentice_subjects_json)
    pprint(apprentice_subjects)

if __name__ == '__main__':
    if path_apprentice_subjects.exists():
        convert_subjects_to_anki()
    else:
        download_apprentice_subjects()
