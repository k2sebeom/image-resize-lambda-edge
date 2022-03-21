# On-the-fly Image Resize using Lambda@Edge

## Installing dependencies
```
pip install -t package/. pillow
```

## Build package for Lambda
```
./make_zip.sh
```

## Deploy Lambda@Edge
Upload created zip file to make Lambda function.
