from django.db import models


class Locations(models.Model):
	def to_json(self):
		return {
			'timestamp': self.timestamp,
			'latitude': self.latitude,
			'longitude': self.longitude,
			'altitude': self.altitude
		}

	timestamp = models.BigIntegerField(unique=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	altitude = models.FloatField()

	@staticmethod
	def add_location(timestamp, latitude, longitude, altitude):
		if Locations.objects.filter(timestamp=timestamp).exists():
			location = Locations.objects.get(timestamp=timestamp)
			location.latitude = latitude
			location.longitude = location
			location.altitude = altitude
		else:
			Locations.objects.create(timestamp=timestamp, latitude=latitude, longitude=longitude, altitude=altitude)


class BTScans(models.Model):
	def to_json(self):
		return {
			'timestamp': self.timestamp,
			'address': self.address,
			'bound': self.bound
		}

	timestamp = models.BigIntegerField(unique=True)
	address = models.CharField(max_length=17)
	bound = models.BooleanField()

	@staticmethod
	def add_bt_scan(timestamp, address, bound):
		if BTScans.objects.filter(timestamp=timestamp).exists():
			bt_scan = BTScans.objects.get(timestamp=timestamp)
			bt_scan.address = address
			bt_scan.bound = bound
		else:
			BTScans.objects.create(timestamp=timestamp, address=address, bound=bound)


class BatteryLevels(models.Model):
	def to_json(self):
		return {
			'timestamp': self.timestamp,
			'battery_percentage': self.battery_percentage,
			'is_charging': self.is_charging
		}

	timestamp = models.BigIntegerField(unique=True)
	battery_percentage = models.FloatField()
	is_charging = models.BooleanField()

	@staticmethod
	def add_battery_level(timestamp, battery_percentage, is_charging):
		if BatteryLevels.objects.filter(timestamp=timestamp).exists():
			battery_level = BatteryLevels.objects.get(timestamp=timestamp)
			battery_level.battery_percentage = battery_percentage
			battery_level.is_charging = is_charging
		else:
			BatteryLevels.objects.create(timestamp=timestamp, battery_percentage=battery_percentage, is_charging=is_charging)