from rest_framework.decorators import api_view
from .geradorPrompt import gerar_prompt
from .geminiService import enviar_prompt
from rest_framework.response import Response
from rest_framework import status
from .serializers import HorarioGeralSerializer
import json
@api_view(["POST"])
def enviarHorario(request):
    if request.method == "POST":
        dadosJsonMock = HorarioGeralSerializer(data=request.data)
        if dadosJsonMock.is_valid():

            dados = dadosJsonMock.validated_data.get("horario")

            prompt = gerar_prompt(dados)

            

            res = enviar_prompt(prompt)

            if isinstance(res, Exception):
                return Response({"error": f"Erro ao enviar mensagem para o Gemini: {str(res)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            texto = res.get("resposta")

            if texto.startswith("```json"):
                texto = texto.replace("```json", "", 1).strip()
            if texto.endswith("```"):
                texto = texto[:-3].strip()

            try:
                resJson = json.loads(texto)
                print(resJson)

            except json.JSONDecodeError:
                return Response({"respostaJson": "Deu erro boy"})

            return Response({"respostaJson": resJson}, status=status.HTTP_200_OK)
        else:
            print("deu errado")
            return Response(dadosJsonMock.errors, status=status.HTTP_400_BAD_REQUEST)
