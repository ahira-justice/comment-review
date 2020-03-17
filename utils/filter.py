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
