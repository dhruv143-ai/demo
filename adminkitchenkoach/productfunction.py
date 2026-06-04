def product_handle_uploaded_file(f):
    with open('adminkitchenkoach/static/assets/images/product_image/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)    
