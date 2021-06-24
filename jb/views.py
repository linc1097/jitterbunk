from django.shortcuts import render, get_object_or_404
from .models import User, Bunk
from django.template import loader
from django.views import generic
from django.utils import timezone

class AllBunksView(generic.ListView):
	template_name = 'jb/allBunks.html'
	context_object_name = 'bunks_list'

	def get_queryset(self):
		return Bunk.objects.filter(pub_date__lte=timezone.now())

def personalBunksView(request, user_id):
	user_id = int(user_id)
	user = get_object_or_404(User, pk=user_id)
	bunks = Bunk.objects.all()
	tos = []
	froms = []
	for bunk in bunks:
		if bunk.to_user.id == user_id:
			tos.append(bunk)
		elif bunk.from_user.id == user_id:
			froms.append(bunk)

	context = {
		'tos' : tos,
		'froms' : froms,
	}
	return render(request, 'jb/personalBunksView.html', context)
	
def bunk(request, user_id):
	user_id = int(user_id)
	sender = get_object_or_404(User, id=user_id)
	try:
		reciever_username = request.POST['username']
		reciever = User.objects.get(username=reciever_username)
	except (KeyError):
		return render(request, 'jb/bunk.html', {'user':sender})
	except:
		return render(request, 'jb/bunk.html', {'user':sender, 'message':'invalid username :( try again :)'})
	else:
		b = Bunk(to_user=reciever, from_user=sender, pub_date=timezone.now())
		b.save()
		return render(request, 'jb/bunk.html', {'user':sender,'message': 'Success! Send Another! :)'})