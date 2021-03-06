from requests import request, HTTPError
from django.core.files.base import ContentFile
from be_local_server.models import *
from django.core.exceptions import ObjectDoesNotExist

def save_profile_picture(strategy, user, response, details, backend,
                         is_new=False,*args,**kwargs):
    if backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            try:
                vendor, created = Vendor.objects.get_or_create(user=user)
            except ObjectDoesNotExist:
                print "No Vendor matching request found."
                return
            if(vendor and not vendor.photo):
                vendorPhoto = VendorPhoto()
                vendorPhoto.image.save('{0}_social.jpg'.format(user.username),
                                       ContentFile(response.content))

                vendorPhoto.save()
                vendor.photo = vendorPhoto
                vendor.save()

def save_user_id(strategy, user, response, details, backend,*args,**kwargs):
    if backend.name == 'facebook':
        vendor = Vendor.objects.get(user=user)

        if vendor is not None and 'link' in response.keys():
            vendor.facebook_url = response['link']
            vendor.save()

            