from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from utils import csvwriter, requesthelper, filter as _

import os


def index(request):
    file_name = ''
    context = {}

    if request.method == "POST":
        url = request.POST.get('url')
        helper = requesthelper.RequestHelper(url)

        headers = ['username', 'date', 'star_rating', 'review_comment', 'link']

        if helper.getURLType() is None:
            messages.add_message(
                request, messages.ERROR,
                'Not an Amazon product link or a YouTube video link'
            )

            return render(request, 'core/index.html')

        elif helper.getURLType() is requesthelper.URLType.AMAZON:
            file_name = 'reviews-{}{}'.format(_.getASIN(url), '.csv')

            unfiltered_result = helper.getResult()
            result = _.extractReviews(unfiltered_result)

        elif helper.getURLType() is requesthelper.URLType.YOUTUBE:
            file_name = 'comments-{}{}'.format(url.split('?v=')[1], '.csv')

            unfiltered_result = helper.getResult()
            result = _.extractComments(unfiltered_result)

            while True:
                if 'nextPageToken' in unfiltered_result.keys():
                    unfiltered_result = helper.getResult(
                        unfiltered_result['nextPageToken'])
                    result += _.extractComments(unfiltered_result)
                else:
                    break

        writer = csvwriter.CSVWriter(
            os.path.join(settings.MEDIA_ROOT, file_name), headers
        )
        writer.write(result)

    context = {'file_name': file_name, 'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'core/index.html', context=context)
