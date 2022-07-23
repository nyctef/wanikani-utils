import requests
from pathlib import Path
from pprint import pprint
import json

path_root = Path(__file__).parent.resolve()
path_api_key = path_root.joinpath('api-key.txt')
path_apprentice_subjects = path_root.joinpath('cache/apprentice_subjects.json')

api_key = path_api_key.read_text()
session = requests.Session()
session.headers.update({'Authorization': f'Bearer {api_key}'})

def download_apprentice_subjects():
    # srs_systems = session.get('https://api.wanikani.com/v2/spaced_repetition_systems/').json()
    apprentice_assignments = session.get('https://api.wanikani.com/v2/assignments', params={'srs_stages': '1,2,3,4'}).json()
    apprentice_subject_ids = [str(x['data']['subject_id']) for x in apprentice_assignments['data']]
    apprentice_subjects = session.get('https://api.wanikani.com/v2/subjects', params={'ids': ','.join(apprentice_subject_ids)}).text
    path_apprentice_subjects.write_text(apprentice_subjects, encoding='utf8')

def convert_subjects_to_anki():
    apprentice_subjects_json = path_apprentice_subjects.read_text(encoding='utf8')
    apprentice_subjects = json.loads(apprentice_subjects_json)
    print("prompt\tresponse")
    for item in apprentice_subjects['data']:
        item_type = item['object']
        item_text = item['data']['characters']
        item_meanings = ', '.join([x['meaning'] for x in item['data']['meanings'] if x['accepted_answer']])
        item_readings = 'readings' in item['data'] and ', '.join([x['reading'] for x in item['data']['readings'] if x['accepted_answer']])
        if item_type == 'radical':
            print(f"{item_type}: {item_text}\t{item_meanings}")
        elif item_type in ('kanji', 'vocabulary'):
            print(f"{item_type} meaning: {item_text}\t{item_meanings}")
            print(f"{item_type} reading: {item_text}\t{item_readings}")
        else:
            raise Error(item['object'])
    # pprint(apprentice_subjects)

if __name__ == '__main__':
    if not path_apprentice_subjects.exists():
        download_apprentice_subjects()

    convert_subjects_to_anki()
