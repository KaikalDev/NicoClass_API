from rest_framework import serializers

class ProfessorInternoSerializer(serializers.Serializer):
    nome = serializers.CharField()
    disponibilidade = serializers.ListField(child=serializers.CharField())
    exigencias = serializers.ListField(child=serializers.CharField())

class DisciplinaComProfessorSerializer(serializers.Serializer):
    nome = serializers.CharField()
    aulas_por_semana = serializers.IntegerField()
    professor = ProfessorInternoSerializer()

class TurmaEntradaSerializer(serializers.Serializer):
    nome = serializers.CharField()
    disclinas = serializers.ListField(child=DisciplinaComProfessorSerializer())
    dias_de_aula = serializers.ListField(child=serializers.CharField())
    turno = serializers.CharField()
    horarios = serializers.ListField(child=serializers.CharField())

class HorarioSerializer(serializers.Serializer):
    turmas = serializers.ListField(child=TurmaEntradaSerializer())
    regras = serializers.ListField(child=serializers.CharField())
