# serializers.py
from rest_framework import serializers
from .models import Master, Mentor, Group, Student


# ========================= MASTER SERIALIZER =========================
class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ['id', 'subject']
        read_only_fields = ['id']

    def validate_subject(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Fan nomi kamida 3 ta belgi bo'lishi kerak!")

        if Master.objects.filter(subject__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Bu fan nomi allaqachon mavjud!")

        return value.title()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['subject'] = instance.subject.title()
        return data


# ========================= MENTOR SERIALIZER =========================
class MentorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    master_subject = serializers.CharField(source='master.subject', read_only=True)
    group_count = serializers.SerializerMethodField()

    class Meta:
        model = Mentor
        fields = [
            'id', 'firstname', 'lastname', 'full_name',
            'master_subject', 'master', 'group_count'
        ]
        read_only_fields = ['id', 'master_subject', 'group_count']
        extra_kwargs = {
            'firstname': {'required': True, 'min_length': 2},
            'lastname': {'required': True, 'min_length': 2},
        }

    def get_full_name(self, obj):
        return f"{obj.firstname} {obj.lastname}".strip()

    def get_group_count(self, obj):
        return obj.groups.count()

    def validate(self, attrs):
        firstname = attrs.get('firstname', '').strip()
        lastname = attrs.get('lastname', '').strip()
        if firstname.lower() == lastname.lower():
            raise serializers.ValidationError({"lastname": "Familiya ism bilan bir xil bo'lishi mumkin emas!"})
        return attrs

    def create(self, validated_data):
        validated_data['firstname'] = validated_data['firstname'].strip().title()
        validated_data['lastname'] = validated_data['lastname'].strip().title()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'firstname' in validated_data:
            validated_data['firstname'] = validated_data['firstname'].strip().title()
        if 'lastname' in validated_data:
            validated_data['lastname'] = validated_data['lastname'].strip().title()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['meta'] = {"groups_count": instance.groups.count()}
        return data


# ========================= GROUP SERIALIZER =========================
class GroupSerializer(serializers.ModelSerializer):
    mentor_fullname = serializers.StringRelatedField(source='mentor', read_only=True)
    mentor_firstname = serializers.CharField(source='mentor.firstname', read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'id', 'title', 'mentor_fullname', 'mentor_firstname',
            'mentor', 'student_count'
        ]
        read_only_fields = ['id', 'mentor_fullname', 'mentor_firstname', 'student_count']
        extra_kwargs = {'title': {'required': True, 'min_length': 3}}

    def get_student_count(self, obj):
        return 0   # Kelajakda Student bilan bog'lash uchun

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Guruh nomi kamida 3 ta belgi bo'lishi kerak!")

        if Group.objects.filter(title__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Bu nomdagi guruh allaqachon mavjud!")

        return value.title()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['title'] = instance.title.title()
        return data


# ========================= STUDENT SERIALIZER =========================
class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'firstname', 'lastname', 'full_name', 'grade']
        read_only_fields = ['id']
        extra_kwargs = {
            'firstname': {'required': True, 'min_length': 2},
            'grade': {'min_value': 1, 'max_value': 11},
        }

    def get_full_name(self, obj):
        lastname = obj.lastname or ''
        return f"{obj.firstname} {lastname}".strip()

    def validate_grade(self, value):
        if not (1 <= value <= 11):
            raise serializers.ValidationError("Sinf (grade) 1 dan 11 gacha bo'lishi kerak!")
        return value

    def validate(self, attrs):
        firstname = attrs.get('firstname', '').strip()
        lastname = attrs.get('lastname', '').strip()
        if firstname and lastname and firstname.lower() == lastname.lower():
            raise serializers.ValidationError({"lastname": "Familiya ism bilan bir xil bo'lishi mumkin emas!"})
        return attrs

    def create(self, validated_data):
        validated_data['firstname'] = validated_data['firstname'].strip().title()
        if validated_data.get('lastname'):
            validated_data['lastname'] = validated_data['lastname'].strip().title()
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['full_name'] = self.get_full_name(instance)
        return data