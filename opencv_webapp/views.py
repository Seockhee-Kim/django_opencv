from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face


# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})


def simple_upload(request):

    if request.method == 'POST':
        # request.POST #title
        # request.FILES # image

        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():

            myfile = request.FILES['image'] #메모리에 업로되어있는 이미지

            fs = FileSystemStorage()

            filename = fs.save(myfile.name, myfile) #물리적 파일이름,객체

            uploaded_file_url = fs.url(filename) #물리적 접근가능한 url
            #fs.delete()
            context = {'form':form, 'uploaded_file_url':uploaded_file_url}

        return render(request, 'opencv_webapp/simple_upload.html', context)



    else:
        form = SimpleUploadForm()
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html', context)


def detect_face(request):

    if request.method == 'POST' :
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = ImageUploadForm(request.POST, request.FILES) # filled form

        if form.is_valid():
            post = form.save(commit=False)
	        # save() 함수는 DB에 저장될 ImageUploadModel 클래스 객체 자체를 리턴함 (== record 1건)
            # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경/추가할 수 있음 (commit=False)
            # ex) post.description = papago.translate(post.description)
            post.save() # Form 객체('form')에 채워져 있는 데이터를 DB에 실제로 저장

	    # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            imageURL = settings.MEDIA_URL + form.instance.document.name
            # == form.instance.document.url
            # == post.document.url
            # == '/media/images/2021/10/29/ses_XQAftn4.jpg'
            # print(form.instance, form.instance.document.name, form.instance.document.url)
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정

            return render(request, 'opencv_webapp/detect_face.html', {'form':form, 'post':post})

    else:
        form = ImageUploadForm()
        return render(request, 'opencv_webapp/detect_face.html',{'form':form})
