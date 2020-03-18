import re


def getASIN(url):
    asin_pattern = r'(?:[/dp/]|$)([A-Z0-9]{10})'
    asin = re.search(asin_pattern, url).group()

    return asin[1:]


def extractComments(result):
    records = []
    items = result['items']

    for item in items:
        snippet = item['snippet']['topLevelComment']['snippet']

        records.append({
            'username': snippet['authorDisplayName'],
            'date': snippet['publishedAt'],
            'star_rating': snippet['viewerRating'],
            'review_comment': snippet['textOriginal'],
            'link': 'none'
        })

    for item in items:
        if 'replies' in item.keys():
            comments = item['replies']['comments']

            for comment in comments:
                snippet = comment['snippet']

                records.append({
                    'username': snippet['authorDisplayName'],
                    'date': snippet['publishedAt'],
                    'star_rating': snippet['viewerRating'],
                    'review_comment': snippet['textOriginal'],
                    'link': 'none'
                })

    return records


def extractReviews(result):
    records = []
    reviews = result['reviews']

    for review in reviews:
        records.append({
            'username': review['review_author'],
            'date': review['review_posted_date'],
            'star_rating': review['review_rating'],
            'review_comment': review['review_text'],
            'link': review['review_link']
        })

    return records
