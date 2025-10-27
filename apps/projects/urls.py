from django.urls import path
from .views import (
	ProjectCreateView,
	ProjectListView,
	ProjectDetailView,
	MyProjectsView,
	join_project,
	ProjectListAPIView,
	ProjectDetailAPIView,
	MyProjectsAPIView,
	join_project_api,
)

app_name = 'projects'

urlpatterns = [
	path('', ProjectListView.as_view(), name='project_list'),
	path('create/', ProjectCreateView.as_view(), name='project_create'),
	path('my/', MyProjectsView.as_view(), name='my_projects'),
	path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
	path('<int:pk>/join/', join_project, name='project_join'),
	# API endpoints
	path('api/', ProjectListAPIView.as_view(), name='project_list_api'),
	path('api/my/', MyProjectsAPIView.as_view(), name='my_projects_api'),
	path('api/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_api'),
	path('api/<int:pk>/join/', join_project_api, name='project_join_api'),
]

# GET /api/projects/api/ - List all projects 
# POST /api/projects/api/ - Create new project 
# GET /api/projects/api/{id}/ - Get project details 
# PUT /api/projects/api/{id}/ - Update project 
# GET /api/projects/api/my/ - Get user's projects 
# POST /api/projects/api/{id}/join/ - Join/leave project 