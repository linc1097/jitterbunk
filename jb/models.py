import datetime
from django.db import models
from django.utils import timezone

class User(models.Model):
	username = models.CharField(max_length=200)
	photo_string = models.CharField(max_length=200)

	def __str__(self):
		return self.username

	def setPhotoString(self, photo_string):
		self.photo_string = photo_string

class Bunk(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_bunks')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_bunks')
	pub_date = models.DateTimeField('date_of_bunk')

	def __str__(self):
		users = str(self.from_user) + ', ' +  str(self.to_user) +  ', '
		return '(' +  users + str(self.pub_date.date()) + self.time() + ')'

	def time(self):
		hour = timezone.localtime(self.pub_date).time().hour
		hour12 = hour % 12
		ampm = 'PM'
		if hour == hour12:
			ampm = 'AM'
		if hour12 == 0:
			hour12 = 12
		minutes = str(self.pub_date.time().minute)
		if len(minutes) == 1:
			minutes = '0' + minutes
		return ', ' + str(hour12) + ':' + minutes + ' ' + ampm

	def was_published_recently(self):
		now = timezone.now()
		return now >= self.pub_date >= now - datetime.timedelta(days=1)