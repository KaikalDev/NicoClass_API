from rest_framework import serializers



class ProfessorSerializer(serializers.Serializer):
    id = serializers.CharField()
    nome = serializers.CharField()
    disponibilidade = serializers.ListField(child= serializers.CharField())
    disciplinas = serializers.ListField(child=serializers.CharField())
    exigencias = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = "__all__"

class DisciplinaSerializer(serializers.Serializer):
    id= serializers.CharField()
    aulas_por_semana = serializers.IntegerField()
    class Meta:
        fields= "__all__"

class TurmaSerializer(serializers.Serializer):
    id = serializers.CharField()
    disciplinas = serializers.ListField(child=DisciplinaSerializer())
    dias_de_aula = serializers.ListField(child=serializers.CharField())
    periodo = serializers.CharField()
    turnos = serializers.IntegerField()
    class Meta:
        fields = "__all__"

class DisciplinasGeralSerializer(serializers.Serializer):
    id =serializers.CharField()
    nome = serializers.CharField()
    professores_possiveis = serializers.ListField(child= serializers.CharField())

    class Meta:
        fields = "__all__"

class HorarioSerializer(serializers.Serializer):
    professores = serializers.ListField(child=ProfessorSerializer())
    turmas = serializers.ListField(child=TurmaSerializer())
    disciplinas = serializers.ListField(child=DisciplinasGeralSerializer())
    horariosDisponiveis = serializers.ListField(child= serializers.CharField())
    regras = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = "__all__"

class HorarioGeralSerializer(serializers.Serializer):
    horario = HorarioSerializer()

    class Meta:
        fields = ["horario"]

