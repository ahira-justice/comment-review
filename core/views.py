from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from utils import csvwriter, requesthelper, filter as _

import os


def index(request):
    if request.method == "POST":
        url = request.POST.get('url')
        helper = requesthelper.RequestHelper(url)

        headers = ['username', 'date', 'star_rating', 'review_comment', 'link']

        if helper.getURLType() is None:
            messages.add_message(
                request, messages.ERROR, 'Not an Amazon product link or a YouTube video link')
        elif helper.getURLType() is requesthelper.URLType.YOUTUBE:
            file_name = 'comments-{}{}'.format(url.split('?v=')[1], '.csv')
            writer = csvwriter.CSVWriter(
                os.path.join(settings.STATIC_ROOT, file_name), headers
            )

            unfiltered_result = helper.getResult()
            result = _.extractComments(unfiltered_result)

            while True:
                if 'nextPageToken' in unfiltered_result.keys():
                    unfiltered_result = helper.getResult(
                        unfiltered_result['nextPageToken'])
                    result += _.extractComments(unfiltered_result)
                else:
                    break

            writer.write(result)

    return render(request, 'core/index.html')
