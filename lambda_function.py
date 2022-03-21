import json
import boto3
from PIL import Image
from urllib.parse import parse_qs, urlencode, unquote
from base64 import b64encode
from io import BytesIO


BUCKET_NAME = 'animalgo-pet-profiles'
s3 = boto3.client('s3')

def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    response = event['Records'][0]['cf']['response']
    
    if int(response['status']) != 200:
        return response
    
    uri = request['uri']
    s3_key = uri.lstrip('/')
    params = {k : v[0] for k, v in parse_qs(request['querystring']).items()}
    
    try:
        resp = s3.get_object(Bucket=BUCKET_NAME, Key=unquote(s3_key))
    except:
        return response

    src_img = Image.open(resp['Body'])
    src_size = src_img.size
    W = params.get('w', src_size[0])
    H = params.get('h', src_size[1])
    
    try:
        W, H = int(W), int(H)
    except:
        response['status'] = 503
        response['statusDescription'] = 'Request size is invalid'
        return response

    resized_img = src_img.resize((W, H))
    
    if W * H > 1024 * 1024:
        response['status'] = 503
        response['statusDescription'] = 'Request file too large'
        return response

    buffer = BytesIO()
    resized_img.save(buffer, format='png')
    img_data = b64encode(buffer.getvalue()).decode()
    buffer.close()
    
    response['status'] = 200
    response['body'] = img_data
    response["bodyEncoding"] = "base64"
    response["headers"]["content-type"] = [
        {'key': 'Content-Type', 'value': 'image/png'}
    ]
    
    return response
