from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from .models import QueryRecord, SentimentRecord
from .serializers import QueryRecordSerializer, SentimentRecordSerializer

# stub utils ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def get_sentiment_for_query(query, existing_data):
    print('getting new data...')
    return {"test":"success"}



def save_new_query(query):

    print('saving new query: ', query)

    data = {
        "query": query,
        "last_updated": '2021-02-10'
    }

    serializer = QueryRecordSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
    else:
        print('failed to serialize query!')
    return


def seven_days_prior(day):
    # stub
    return day

def get_days_prior(start, lookback):
    retval = [start.strftime('%Y-%m-%d')]
    for i in range(lookback - 1):
        components = retval[i].split('-')
        yyyy, mm, dd = components
        retval.append((datetime(int(yyyy), int(mm), int(dd)) - timedelta(1)).strftime('%Y-%m-%d'))

    return retval


def are_records_up_to_date(records):
    print('checked if records up to date: ', records)

    n_days_lookback = 7
    today = datetime.today()
    expected_days = get_days_prior(today, n_days_lookback)

    for record in records:
        if record.date in expected_days:
            days_expected.pop(record.date)

    if expected_days:
        return False

    return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# GET all queries (POST new query exists but will not be needed)
@csrf_exempt
def query_record_list(request):

    if request.method == 'GET':
        queries = QueryRecord.objects.all()
        serializer = QueryRecordSerializer(queries, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = QueryRecordSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

    return 'test'



# GET sentiment records for query (POST new sentiment record exists but will not be needed)
@csrf_exempt
def query_record_detail(request, query=None):

    if request.method == 'GET':

        #  Search database for records matching query
        existing_query = QueryRecord.objects.filter(query=query)

        print('existing_query', existing_query)

        if not existing_query:
            print('no existing query found!')
            save_new_query(query)

        records = SentimentRecord.objects.filter(query=query)
        serializer = SentimentRecordSerializer(records, many=True)

        # expects last 7 days (incl. today) to be recorded
        if not are_records_up_to_date(records):
            print('records not up to date!')
            # send existing data to api to be patched
            records = get_sentiment_for_query(query, records)
            records = JSONParser().parse(records)
            serializer = SentimentRecordSerializer(data=records)

            if not serializer.is_valid():
                return JsonResponse({'error': 'internal server error'}, status=500)

        return JsonResponse(serializer.data, status=200, safe=False)

