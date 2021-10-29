from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic

from .forms import UrlsForm
from .backend import api
# from .backend import style_transfer as sty

def index(request):

    # default_portret_url = "https://image.freepik.com/free-photo/young-extraterrestrial-woman-s-portret_144627-3464.jpg"
    # default_style_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrXW-y7mU0DQW9jt7kCIXV3BQXO5CAD-Glhw&usqp=CAU"
    
    default_portret_url = "https://example1.jpg"
    default_style_url = "https://example2.jpg"
    
    photo_err = False
	# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print("\n")
            # process the data in form.cleaned_data as required
            try:
                portret, portret64 = api.get_img_and_base64(form.cleaned_data['portret_url'])
            except Exception as e:
                photo_err = True
                # print("portret err ", e, portret_err)

            try:
                style, style64 = api.get_img_and_base64(form.cleaned_data['style_url'])
            except Exception as e:
                photo_err = True
                # print(" style err ", e, style_err)

                # print("\nerror in get_img_and_base64\n")
                # form.cleaned_data['style_url'] = "Sorry! Image can't be loaded from that link);"
            
            if not photo_err:
                # print("\nmask\n")
                # mask, mask64 = api.get_person_mask_and_mask64(portret)
                result64 = api.merge_style_and_person( portret, style)
                # stylized64 = sty.get_stylized_portret(style, portret, mask)
                context = {'form': form, 'portret64': portret64, "style64": style64,\
                "new_imgs": True, "load_static_examples": False,\
                "portret_err": False, "style_err": False, "result64": result64,\
                "not_valid_form": False}
                return render(request, 'url_image/index.html', context)
            else:
                context = {'form': form, "photo_err": photo_err, \
                "load_static_examples": False, "new_imgs": False, "not_valid_form": False}
                return render(request, 'url_image/index.html', context)
        else:
            context = {'form': form, "photo_err": False, \
            "load_static_examples": False, "new_imgs": False, "not_valid_form": True}
            return render(request, 'url_image/index.html', context)


    else:
        form = UrlsForm(initial={'portret_url': default_portret_url,\
                        "style_url": default_style_url})
        context = {'form': form, "load_static_examples": True, "new_imgs": False,\
        "photo_err": False, "not_valid_form": False}

        return render(request, 'url_image/index.html', context)


