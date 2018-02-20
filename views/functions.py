def loggedIn(request):
    return 'id' in request.session

def logout(request):
    request.session.flush()
