from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm
from .serializers import ProjectSerializer
from users.models import UserProfile
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@method_decorator(csrf_exempt, name='dispatch')
class ProjectCreateView(LoginRequiredMixin, CreateView):
	model = Project
	form_class = ProjectForm
	template_name = 'projects/project_create.html'

	def form_valid(self, form):
		try:
			profile = self.request.user.userprofile
		except Exception:
			profile = None
		instance = form.save(commit=False)
		if profile:
			instance.created_by = profile
		instance.save()
		return redirect('projects:project_detail', pk=instance.pk)


class ProjectListView(ListView):
	model = Project
	template_name = 'projects/project_list.html'
	context_object_name = 'projects'


class ProjectDetailView(DetailView):
	model = Project
	template_name = 'projects/project_detail.html'
	context_object_name = 'project'

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		user = self.request.user
		is_member = False
		if user.is_authenticated:
			try:
				profile = user.userprofile
				is_member = profile in self.object.members.all()
			except Exception:
				is_member = False
		ctx['is_member'] = is_member
		return ctx


class MyProjectsView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'projects/my_projects.html'
	context_object_name = 'projects'

	def get_queryset(self):
		try:
			profile = self.request.user.userprofile
		except Exception:
			return Project.objects.none()
		return Project.objects.filter(Q(created_by=profile) | Q(members=profile)).distinct()


@login_required
def join_project(request, pk):
	project = get_object_or_404(Project, pk=pk)
	try:
		profile = request.user.userprofile
	except Exception:
		return redirect('projects:project_detail', pk=pk)

	if profile in project.members.all():
		project.members.remove(profile)
	else:
		project.members.add(profile)
	return redirect('projects:project_detail', pk=pk)


# API Views
class ProjectListAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            profile = self.request.user.userprofile
            serializer.save(created_by=profile)
        except Exception:
            raise serializers.ValidationError("User profile not found")


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MyProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            profile = self.request.user.userprofile
            return Project.objects.filter(Q(created_by=profile) | Q(members=profile)).distinct()
        except Exception:
            return Project.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_project_api(request, pk):
    project = get_object_or_404(Project, pk=pk)
    try:
        profile = request.user.userprofile
    except Exception:
        return Response({"error": "User profile not found"}, status=status.HTTP_400_BAD_REQUEST)

    if profile in project.members.all():
        project.members.remove(profile)
        return Response({"message": "Left project successfully"})
    else:
        project.members.add(profile)
        return Response({"message": "Joined project successfully"})

