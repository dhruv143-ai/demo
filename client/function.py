def handle_uploaded_file(f):
    with open('adminkitchenkoach/static/assets/images/recipeimage/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)    
    