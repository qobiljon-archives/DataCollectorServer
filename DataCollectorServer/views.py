import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from DataCollectorServer.models import Locations
from DataCollectorServer.models import BTScans
from DataCollectorServer.models import BatteryLevels


class Result:
    OK = 0
    FAIL = 1


def extract_post_params(request):
    _files = request.FILES
    if 'username' in _files:
        return json.loads('{"username": "%s", "password": "%s"}' % (
            _files['username'].read().decode('utf-8'),
            _files['password'].read().decode('utf-8')
        ))
    _post = request.POST
    if 'username' in _post:
        return _post
    else:
        try:
            return json.loads(request.body.decode('utf-8'))
        except JSONDecodeError:
            return None


@require_http_methods(['POST'])
@csrf_exempt
def api_submit_location_data(request):
    location_data = request.POST['location_data']
    for line in location_data.split('\n'):
        array = line.split(' ')
        if len(array) == 4:
            timestamp, latitude, longitude, altitude = array
            Locations.add_location(timestamp=int(timestamp), latitude=float(latitude), longitude=float(longitude), altitude=float(altitude))
    return JsonResponse({'result': Result.OK})


@require_http_methods(['POST'])
@csrf_exempt
def api_submit_bt_scan_data(request):
    bt_scan_data = request.POST['bt_scan_data']
    for line in bt_scan_data.split('\n'):
        array = line.split(' ')
        if len(array) == 3:
            timestamp, address, bound = array
            BTScans.add_bt_scan(timestamp=int(timestamp), address=address, bound=bound.lower() == 'true')
    return JsonResponse({'result': Result.OK})


@require_http_methods(['POST'])
@csrf_exempt
def api_battery_level_data(request):
    battery_level_data = request.POST['battery_level_data']
    for line in battery_level_data.split('\n'):
        array = line.split(' ')
        if len(array) == 3:
            timestamp, battery_percentage, is_charging = array
            BatteryLevels.add_battery_level(timestamp=int(timestamp), battery_percentage=float(battery_percentage), is_charging=is_charging.lower() == 'true')
    return JsonResponse({'result': Result.OK})


@require_http_methods(['POST'])
@csrf_exempt
def api_get_data_submission_progress(request):
    return JsonResponse({
        'location_samples': Locations.objects.count(),
        'last_location': 0 if Locations.objects.count() == 0 else Locations.objects.last().timestamp,
        'bt_scan_samples': BTScans.objects.count(),
        'last_bt_scan': 0 if BTScans.objects.count() == 0 else BTScans.objects.last().timestamp,
        'battery_level_samples': BatteryLevels.objects.count(),
        'last_battery_level': 0 if BatteryLevels.objects.count() == 0 else BatteryLevels.objects.last().timestamp,
    })


@require_http_methods(['POST'])
@csrf_exempt
def api_get_lof_calculation_progress(request):
    done_lof_count = Locations.objects.exclude(lof=-1.0).count() + BTScans.objects.exclude(lof=-1.0).count() + BatteryLevels.objects.exclude(lof=-1.0).count()
    ovr_data_count = Locations.objects.count() + BTScans.objects.count() + BatteryLevels.objects.count()
    return JsonResponse({
        'lof_count': done_lof_count,
        'lof_progress': done_lof_count / ovr_data_count
    })
