import json
import requests

def push(result):
    API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpNzZjZTVmdG5ad1Nwc2hOc1dzS3lZIiwiaWF0IjoxNzI5NjY5NzkwLCJleHAiOjE3MzE1OTY0MDAsInR5cGUiOiJhcGlfa2V5In0.eYHCyQlrTHsg6XHS0BHEcXS03LPN8oAgyMACnkCUPCE'
    result = {
        'submit_result' : result
    }
    success = requests.post('https://research-api.solarkim.com/submissions/cmpt-2024',
                        data=json.dumps(result),
                        headers={
                            'Authorization': f'Bearer {API_KEY}'
                        }).json()
    print(success)
