freeCodeCamp: https://www.youtube.com/watch?v=F5mRW0jo-U4

###################################
####### New Project ###############
###################################

# django

cd <path_to_folder_where_you_want_to_be>

# create a project
django-admin startproject <project_name>

# create a super user
python manage.py createsuperuser

###################################
####### New App ###################
###################################

# create a new app (2 steps)
python manage.py startapp <app_name>
# add <app_name> in settings file

# add to admin.py
from .models import <app_name>
admin.site.register(<app_name>)

# run
python manage.py shell
from <app_name>.Models import <class_name>
<class_name>.objects.all()
<class_name>.objects.create(*kwargs)

###################################
####### Update the Model ##########
###################################

# change 
# changes in models.py
python manage.py makemigrations
python manage.py migrate


###################################
####### Running a Project #########
###################################

# start your project
python manage.py runserver

