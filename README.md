
To use the script, first obtain a New York Times Developer API Key from https://developer.nytimes.com/apis. It's enough to enable only 'Article Search API' for the execution. APIs can be accessed free for non-commercial uses. With the API key, they monitor your usage levels. There is a limit to the number of requests in a day, but I have never run into the limit. After getting the API key, add the key to the script on the line marked "API_key = '''. You may need to install the Python3 Requests package.

You can briefly take a look how the request work at https://developer.nytimes.com/docs/articlesearch-product/1/routes/articlesearch.json/get for the 'Atricle Search API'. Kindly other APIs also provides

e.g. python headline2csv.py search-word 20220201 2022123

Begin date (^\d{8}$) (e.g. 20120101)

End date (e.g. 20121231)