from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserProfile
from projects.models import Project

User = get_user_model()


class Command(BaseCommand):
    help = 'Create demo users and projects'

    def handle(self, *args, **options):
        # Create demo users
        demo_users = [
            {
                'username': 'alice_dev',
                'email': 'alice@example.com',
                'password': 'demo123',
                'bio': 'Full-stack developer with 5 years of experience in React and Python. Passionate about clean code and user experience.',
                'skills': ['Python', 'Django', 'React', 'JavaScript', 'PostgreSQL', 'Docker'],
                'interests': ['Web Development', 'Machine Learning', 'Open Source'],
                'availability_hours': 20,
                'preferred_roles': ['Backend Developer', 'Full-stack Developer']
            },
            {
                'username': 'bob_frontend',
                'email': 'bob@example.com',
                'password': 'demo123',
                'bio': 'Frontend specialist focused on modern JavaScript frameworks. Love creating beautiful and responsive user interfaces.',
                'skills': ['React', 'Vue.js', 'TypeScript', 'CSS', 'SASS', 'Webpack'],
                'interests': ['UI/UX Design', 'Frontend Architecture', 'Performance Optimization'],
                'availability_hours': 15,
                'preferred_roles': ['Frontend Developer', 'UI Developer']
            },
            {
                'username': 'charlie_mobile',
                'email': 'charlie@example.com',
                'password': 'demo123',
                'bio': 'Mobile app developer specializing in React Native and Flutter. Experienced in both iOS and Android development.',
                'skills': ['React Native', 'Flutter', 'Swift', 'Kotlin', 'Firebase', 'Redux'],
                'interests': ['Mobile Development', 'Cross-platform Apps', 'App Store Optimization'],
                'availability_hours': 25,
                'preferred_roles': ['Mobile Developer', 'React Native Developer']
            },
            {
                'username': 'diana_designer',
                'email': 'diana@example.com',
                'password': 'demo123',
                'bio': 'UI/UX designer with a background in psychology. Focus on creating intuitive and accessible user experiences.',
                'skills': ['Figma', 'Adobe XD', 'Sketch', 'Photoshop', 'Illustrator', 'Prototyping'],
                'interests': ['User Research', 'Accessibility', 'Design Systems', 'Branding'],
                'availability_hours': 18,
                'preferred_roles': ['UI Designer', 'UX Designer', 'Product Designer']
            },
            {
                'username': 'eve_devops',
                'email': 'eve@example.com',
                'password': 'demo123',
                'bio': 'DevOps engineer with expertise in cloud infrastructure and CI/CD pipelines. Passionate about automation and scalability.',
                'skills': ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins', 'Python'],
                'interests': ['Cloud Computing', 'Infrastructure as Code', 'Monitoring', 'Security'],
                'availability_hours': 30,
                'preferred_roles': ['DevOps Engineer', 'Cloud Engineer', 'Site Reliability Engineer']
            }
        ]

        created_users = []
        for user_data in demo_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                
                # Create user profile
                profile, profile_created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': user_data['bio'],
                        'skills': user_data['skills'],
                        'interests': user_data['interests'],
                        'availability_hours': user_data['availability_hours'],
                        'preferred_roles': user_data['preferred_roles']
                    }
                )
                created_users.append(profile)
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username}')
                )
            else:
                created_users.append(user.userprofile)
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user.username}')
                )

        # Create demo projects
        demo_projects = [
            {
                'title': 'EcoTracker Mobile App',
                'description': 'A mobile application to help users track their carbon footprint and suggest eco-friendly alternatives. Features include daily activity tracking, carbon footprint calculator, and personalized recommendations for sustainable living.',
                'tech_stack': ['React Native', 'Firebase', 'Redux', 'Node.js', 'MongoDB'],
                'needed_roles': ['Mobile Developer', 'Backend Developer', 'UI Designer'],
                'created_by': created_users[0],  # alice_dev
                'members': [created_users[0], created_users[2]]  # alice_dev, charlie_mobile
            },
            {
                'title': 'DevPal Platform',
                'description': 'A web platform connecting developers with projects. Features include project discovery, team matching, skill-based recommendations, and collaboration tools. Built with modern web technologies.',
                'tech_stack': ['Django', 'React', 'PostgreSQL', 'Redis', 'Docker'],
                'needed_roles': ['Full-stack Developer', 'Frontend Developer', 'DevOps Engineer'],
                'created_by': created_users[1],  # bob_frontend
                'members': [created_users[1], created_users[0], created_users[4]]  # bob_frontend, alice_dev, eve_devops
            },
            {
                'title': 'AI Recipe Generator',
                'description': 'An intelligent recipe generator that creates personalized recipes based on available ingredients, dietary restrictions, and taste preferences. Uses machine learning to suggest optimal cooking methods.',
                'tech_stack': ['Python', 'TensorFlow', 'Django', 'React', 'PostgreSQL'],
                'needed_roles': ['Machine Learning Engineer', 'Backend Developer', 'Frontend Developer'],
                'created_by': created_users[0],  # alice_dev
                'members': [created_users[0]]
            },
            {
                'title': 'Smart Home Dashboard',
                'description': 'A comprehensive dashboard for managing smart home devices. Features include device control, energy monitoring, automation rules, and security alerts. Focus on intuitive design and accessibility.',
                'tech_stack': ['Vue.js', 'Node.js', 'WebSocket', 'MQTT', 'InfluxDB'],
                'needed_roles': ['Frontend Developer', 'Backend Developer', 'UI Designer'],
                'created_by': created_users[3],  # diana_designer
                'members': [created_users[3], created_users[1]]  # diana_designer, bob_frontend
            },
            {
                'title': 'Blockchain Voting System',
                'description': 'A secure, transparent voting system built on blockchain technology. Ensures vote integrity, prevents fraud, and provides real-time results. Includes mobile app for voters and web dashboard for administrators.',
                'tech_stack': ['Solidity', 'Web3.js', 'React Native', 'Node.js', 'IPFS'],
                'needed_roles': ['Blockchain Developer', 'Mobile Developer', 'Security Engineer'],
                'created_by': created_users[4],  # eve_devops
                'members': [created_users[4], created_users[2]]  # eve_devops, charlie_mobile
            },
            {
                'title': 'Fitness Tracker API',
                'description': 'A comprehensive API for fitness tracking applications. Provides endpoints for workout logging, progress tracking, social features, and integration with wearable devices. Scalable microservices architecture.',
                'tech_stack': ['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Kubernetes'],
                'needed_roles': ['Backend Developer', 'DevOps Engineer', 'API Designer'],
                'created_by': created_users[0],  # alice_dev
                'members': [created_users[0], created_users[4]]  # alice_dev, eve_devops
            },
            {
                'title': 'Virtual Event Platform',
                'description': 'A platform for hosting virtual events, conferences, and meetups. Features include live streaming, chat rooms, networking tools, and event management. Built for scalability and global accessibility.',
                'tech_stack': ['React', 'Node.js', 'WebRTC', 'Socket.io', 'AWS'],
                'needed_roles': ['Full-stack Developer', 'DevOps Engineer', 'UX Designer'],
                'created_by': created_users[1],  # bob_frontend
                'members': [created_users[1], created_users[3], created_users[4]]  # bob_frontend, diana_designer, eve_devops
            },
            {
                'title': 'Code Review Assistant',
                'description': 'An AI-powered code review tool that analyzes pull requests and provides intelligent suggestions for code improvements, security vulnerabilities, and best practices. Integrates with popular Git platforms.',
                'tech_stack': ['Python', 'Machine Learning', 'Django', 'React', 'Docker'],
                'needed_roles': ['Machine Learning Engineer', 'Backend Developer', 'Frontend Developer'],
                'created_by': created_users[0],  # alice_dev
                'members': [created_users[0], created_users[1]]  # alice_dev, bob_frontend
            }
        ]

        for project_data in demo_projects:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    'description': project_data['description'],
                    'tech_stack': project_data['tech_stack'],
                    'needed_roles': project_data['needed_roles'],
                    'created_by': project_data['created_by']
                }
            )
            
            if created:
                # Add members
                for member in project_data['members']:
                    project.members.add(member)
                
                self.stdout.write(
                    self.style.SUCCESS(f'Created project: {project.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Project already exists: {project.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('Demo data creation completed!')
        )
