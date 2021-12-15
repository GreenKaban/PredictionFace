from django.shortcuts import render


from .forms import UrlsForm
from .backend import api


def index(request):

    default_photo_first_url = "https://example1.jpg"
    default_photo_second_url = "https://example2.jpg"

    photo_err = False
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            try:
                photo_first, photo_first64 = api.get_img_and_base64(form.cleaned_data['photo_first_url'])
            except Exception as e:
                photo_err = True

            try:
                photo_second, photo_second64 = api.get_img_and_base64(form.cleaned_data['photo_second_url'])
            except Exception as e:
                photo_err = True

            if not photo_err:
                result64 = api.match_photo(photo_first, photo_second)
                context = {'form': form, 'photo_first64': photo_first64, "photo_second64": photo_second64,
                           "new_imgs": True, "load_static_examples": False,
                           "portret_err": False, "style_err": False, "result64": result64,
                           "not_valid_form": False}
                return render(request, 'url_image/index.html', context)
            else:
                context = {'form': form, "photo_err": photo_err,
                           "load_static_examples": False, "new_imgs": False, "not_valid_form": False}
                return render(request, 'url_image/index.html', context)
        else:
            context = {'form': form, "photo_err": False,
                       "load_static_examples": False, "new_imgs": False, "not_valid_form": True}
            return render(request, 'url_image/index.html', context)

    else:
        form = UrlsForm(initial={'photo_first_url': default_photo_first_url,
                                 "photo_second_url": default_photo_second_url})
        context = {'form': form, "load_static_examples": True, "new_imgs": False,
                   "photo_err": False, "not_valid_form": False}

        return render(request, 'url_image/index.html', context)
