from django.urls import path,re_path
from .views import dashboard,Cv,Candidatures,Messages,save_Cv_pdf,save_Other_Docs_pdf,save_photo,rec_dashboard,save_skills,delete_skill,save_education,delete_education,downloadCV,downloadOtherDoc,Tests
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('Dashboard/',dashboard,name='dashboard'),
   path('Cv/',Cv,name='Cv'),
   path('Candidatures/',Candidatures,name='Candidatures'),
   path('Messages/',Messages,name='Messages'),
   path('save_Cv_pdf/', save_Cv_pdf, name='save_Cv_pdf'),
   path('save_Other_Docs_pdf/', save_Other_Docs_pdf, name='save_Other_Docs_pdf'),
   path('save_photo/', save_photo, name='save_photo'),
   path('save_skills/', save_skills, name='save_skills'),
   path('save_education/', save_education, name='save_education'),
   path('delete_skill/<int:skill_id>/', delete_skill, name='delete_skill'),
   path('delete_education/<int:education_id>/', delete_education, name='delete_education'),
   path('Download_Cv_pdf/', downloadCV, name='downloadCV'),
   path('Download_Other_Docs_pdf/', downloadOtherDoc, name='downloadOtherDoc'),
   path('Tests/', Tests, name='Tests'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)