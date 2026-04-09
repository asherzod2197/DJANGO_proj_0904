import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # o'zingizning settings yo'lingizga o'zgartiring
django.setup()

from blog.models import Master, Mentor, Group, Student  # o'zingizning app nomiga o'zgartiring


def run():
    print("Ma'lumotlar tozalanmoqda...")
    Student.objects.all().delete()
    Group.objects.all().delete()
    Mentor.objects.all().delete()
    Master.objects.all().delete()

    print("Master (fanlar) yaratilmoqda...")
    math = Master.objects.create(subject="Matematika")
    physics = Master.objects.create(subject="Fizika")
    english = Master.objects.create(subject="Ingliz tili")
    programming = Master.objects.create(subject="Dasturlash")
    chemistry = Master.objects.create(subject="Kimyo")

    print("Mentor (o'qituvchilar) yaratilmoqda...")
    mentor1 = Mentor.objects.create(firstname="Alisher", lastname="Karimov", master=math)
    mentor3 = Mentor.objects.create(firstname="Bobur", lastname="Rahimov", master=physics)
    mentor4 = Mentor.objects.create(firstname="Malika", lastname="Toshmatova", master=english)
    mentor6 = Mentor.objects.create(firstname="Nilufar", lastname="Ergasheva", master=programming)
    mentor7 = Mentor.objects.create(firstname="Jasur", lastname="Hamidov", master=chemistry)

    print("Talabalar yaratilmoqda...")
    students_data = [
        ("Azizbek", "Tursunov", 8),
        ("Barno", "Mirzayeva", 9),
        ("Doniyor", "Xoliqov", 7),
        ("Feruza", "Abdullayeva", 10),
        ("Husan", "Qodirov", 8),
        ("Iroda", "Salimova", 9),
        ("Javlon", "Normatov", 7),
        ("Kamola", "Razzaqova", 10),
        ("Lochin", "Boymurodov", 8),
        ("Maftuna", "Sotvoldiyeva", 9),
        ("Nodir", "Usmonov", 7),
        ("Oydin", "Hamroyeva", 10),
        ("Parviz", "Botirov", 8),
        ("Rohila", "Xasanova", 9),
        ("Sanjar", "Zokirov", 7),
    ]

    students = []
    for firstname, lastname, grade in students_data:
        s = Student.objects.create(firstname=firstname, lastname=lastname, grade=grade)
        students.append(s)




    print("\n✅ Seed data muvaffaqiyatli yuklandi!")
    print(f"   Master      : {Master.objects.count()} ta")
    print(f"   Mentor      : {Mentor.objects.count()} ta")
    print(f"   Group       : {Group.objects.count()} ta")
    print(f"   Student     : {Student.objects.count()} ta")


if __name__ == '__main__':
    run()

