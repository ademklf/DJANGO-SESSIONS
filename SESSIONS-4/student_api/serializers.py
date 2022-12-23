from rest_framework import serializers
from .models import Student

# class StudentSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=50)
#     number = serializers.IntegerField()
#     age = serializers.IntegerField()
    
    
#     def create(self, validated_data):
#         return Student.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.number = validated_data.get('number', instance.number)
#         instance.age = validated_data.get('age', instance.age)
#         instance.save()
#         return instance



class StudentSerializer(serializers.ModelSerializer):

    born_year = serializers.SerializerMethodField() #read_only

    class Meta:
        model = Student
        fields = ["first_name","last_name", "number","age","born_year", "path"]
        # fields = "__all__" # tüm field kısımlarını alıyor
        # fields = ["first_name","last_name"] # sadece istediğimiz filed ksımları alınıyor
        # exclude = ["number"]  # belirtilen field hariç geri kalanlar

    def get_born_year(self, obj):
        import datetime
        current_time = datetime.datetime.now()
        return current_time.year - obj.age