from django.shortcuts import render


from .forms import UrlsForm
from .backend import api, email_sender
from django.core.mail import send_mail, EmailMessage

def index(request):

    photo_err = False
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlsForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            try:
                image1 = form.cleaned_data['photo_first_url']
                image2 = form.cleaned_data['photo_second_url']
                photo_first, photo_first64 = api.get_img_and_base64(image1)
                photo_second, photo_second64 = api.get_img_and_base64(image2)
                email = form.cleaned_data['email']
            except:
                photo_err = True

            if not photo_err:
                result64 = api.match_photo(photo_first, photo_second)

                # email_sender.send_email('ig.ko4etkoff2013@gmail.com', '', result64, [form.cleaned_data['photo_first_url'], form.cleaned_data['photo_second_url']])

                mail = EmailMessage('subject', result64, 'face.comparator@gmail.com', [email])
                mail.attach(image1.name, image1.read(), image1.content_type)
                mail.attach(image2.name, image2.read(), image2.content_type)
                mail.send()

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
        form = UrlsForm()
        context = {'form': form, "load_static_examples": True, "new_imgs": False,
                   "photo_err": False, "not_valid_form": False}

        return render(request, 'url_image/index.html', context)
