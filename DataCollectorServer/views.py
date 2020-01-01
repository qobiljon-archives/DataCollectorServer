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
