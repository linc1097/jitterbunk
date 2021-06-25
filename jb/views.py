from django.shortcuts import render, get_object_or_404
from .models import User, Bunk
from django.template import loader
from django.views import generic
from django.utils import timezone
import datetime

class AllBunksView(generic.ListView):
	template_name = 'jb/allBunks.html'
	context_object_name = 'bunks_list'

	def get_queryset(self):
		return Bunk.objects.filter(pub_date__lte=(timezone.now()-datetime.timedelta(hours=5)))

def personalBunksView(request, username):
	user = get_object_or_404(User, username=username)
	try:
		photo_string = request.POST['photo_string']
		user.photo_string = photo_string
		user.save()
	except:
		pass
	bunks = Bunk.objects.all()
	tos = []
	froms = []
	for bunk in bunks:
		if bunk.to_user.username == username:
			tos.append(bunk)
		elif bunk.from_user.username == username:
			froms.append(bunk)

	context = {
	    'user' : user,
		'tos' : tos,
		'froms' : froms,
	}
	return render(request, 'jb/personalBunksView.html', context)

def signup(request):
	try:
		username = request.POST['username']
		photo_string = request.POST['photo_string']
		print(User.objects.filter(username=username))
		if User.objects.filter(username=username) or username == 'signup':
			message = 'username ' + username + ' already taken, try again!'
			return render(request, 'jb/signup.html', {'message': message})
		else:
			u = User(username=username, photo_string=photo_string)
			u.save()
			message = 'Successfully registered ' + username + "! add another?"
			return render(request, 'jb/signup.html', {'message': message})
	except:
		return render(request, 'jb/signup.html', {})

	
def bunk(request, username):
	sender = get_object_or_404(User, username=username)
	try:
		reciever_username = request.POST['username']
		reciever = User.objects.get(username=reciever_username)
	except (KeyError):
		return render(request, 'jb/bunk.html', {'user':sender})
	except:
		return render(request, 'jb/bunk.html', 
			{'users':User.objects.all(), 'user':sender, 'message':'That user doesn\'t exist . . . YET, maybe one day!'})
	else:
		b = Bunk(to_user=reciever, from_user=sender, pub_date=(timezone.now()-datetime.timedelta(hours=5)))
		b.save()
		return render(request, 'jb/bunk.html', {'users':User.objects.all(), 'user':sender,'message': 'Success! Send Another! :)'})
