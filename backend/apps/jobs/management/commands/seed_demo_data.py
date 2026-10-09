from getpass import getpass

from django.core.management.base import BaseCommand, CommandError

from apps.jobs.models import Job
from apps.users.models import EmployerProfile, User


class Command(BaseCommand):
    help = "Seed the database with a demo employer and sample job listings."

    def handle(self, *args, **options):
        employer_email = "employer@skillbase.local"
        employer_password = getpass("Demo employer password: ")
        password_confirmation = getpass("Demo employer password (again): ")

        if not employer_password:
            raise CommandError("Password cannot be empty.")
        if employer_password != password_confirmation:
            raise CommandError("The two passwords did not match.")

        employer, created = User.objects.get_or_create(
            email=employer_email,
            defaults={
                "role": "employer",
                "is_staff": False,
                "is_superuser": False,
            },
        )

        if not created:
            employer.role = "employer"
            employer.is_staff = False
            employer.is_superuser = False

        employer.set_password(employer_password)
        employer.save()

        EmployerProfile.objects.get_or_create(
            user=employer,
            defaults={
                "company_name": "SkillBase Labs",
                "industry": "Software",
                "company_size": "11-50",
            },
        )

        sample_jobs = [
            {
                "title": "Senior Frontend Engineer",
                "description": "Build accessible, responsive interfaces for a skill-based hiring platform and partner with design and backend teams to ship new product experiences.",
                "required_skills": ["React", "Next.js", "TypeScript", "Tailwind CSS", "UI Architecture"],
                "salary": "$120k - $150k",
                "location": "Remote",
                "experience_level": "SENIOR",
                "positions": 2,
            },
            {
                "title": "Python Backend Developer",
                "description": "Develop and maintain API services, optimize database access, and support AI-powered recommendation features for candidate and job matching.",
                "required_skills": ["Python", "Django", "REST API", "PostgreSQL", "Celery"],
                "salary": "$110k - $135k",
                "location": "Hybrid",
                "experience_level": "MID",
                "positions": 3,
            },
            {
                "title": "Data Analyst",
                "description": "Analyze hiring funnel metrics, interpret skill trends, and support teams with dashboard reporting and insight generation.",
                "required_skills": ["SQL", "Python", "Excel", "Power BI", "Analytics"],
                "salary": "$90k - $120k",
                "location": "Remote",
                "experience_level": "MID",
                "positions": 1,
            },
            {
                "title": "Product Designer",
                "description": "Design user flows, create mobile-friendly experiences, and collaborate closely with engineering to deliver polished product experiences.",
                "required_skills": ["Figma", "UX Research", "Design Systems", "User Flows", "Product Design"],
                "salary": "$100k - $130k",
                "location": "Remote",
                "experience_level": "MID",
                "positions": 2,
            },
        ]

        for job_data in sample_jobs:
            Job.objects.get_or_create(
                title=job_data["title"],
                created_by=employer,
                defaults={
                    "description": job_data["description"],
                    "required_skills": job_data["required_skills"],
                    "salary": job_data["salary"],
                    "location": job_data["location"],
                    "experience_level": job_data["experience_level"],
                    "positions": job_data["positions"],
                    "status": "open",
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo employer and sample jobs created."))
