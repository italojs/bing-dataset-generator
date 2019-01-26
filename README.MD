# bing-dataset-generator

It's a package to download images from [bing.com](https://www.bing.com/?scope=images&FORM=Z9LH1)

## Install
```
pip intall -r requirements.txt
```

## Bing API
Before use this package, create a bing api key [here](https://azure.microsoft.com/en-us/try/cognitive-services/?api=bing-image-search-api), it's easy, just choose the *free* plan --> login with some [Microsoft, Facebook, Linkedin, Github] account --> get your *key2*

## Basic usage
```
python3 request.py --query "<YOUR_QUERY>" --output <YOUR_OUTPUT_IMAGE_PATH> --key <YOUR_BING_API_KEY2>
```

## Full usage
```
python3 request.py --query "<YOUR_QUERY>" --output <YOUR_OUTPUT_IMAGE_PATH> --key <YOUR_BING_API_KEY2> --max_results <Number> --group_size <Number>"
```

### Example
```
python3 request.py -query "faces" --output dataset/faces --key f182e89c48a894f453a32a171c43cb8702 --max_results 250 --group_size 50
```

### Parameters
To know more about parameters use `python3 request.py -h`:

```
usage: request.py [-h] -q QUERY -o OUTPUT -k KEY [-m MAX_RESULTS]
                  [-g GROUP_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        search query to search Bing ImageAPI for
  -o OUTPUT, --output OUTPUT
                        path to output directory of images
  -k KEY, --key KEY     bing api key
  -m MAX_RESULTS, --max_results MAX_RESULTS
                        maximum images to download | default=250
  -g GROUP_SIZE, --group_size GROUP_SIZE
                        results per request | default=50
```
