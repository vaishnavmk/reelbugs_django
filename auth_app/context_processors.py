from auth_app.models import User

def base_processor(request):
	if request.user.is_authenticated():
		return {'base':'writers_block/base.html'}
	else:
		return {'base':'writers_block/base2.html'}