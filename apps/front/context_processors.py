from apps.cms.models import User


def frontuser(request):
    user_id = request.session.get('id')
    print(user_id)
    context = {}
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            print(user)
            context['frontuser'] = user
        except:
            print("except")
            pass
    return context