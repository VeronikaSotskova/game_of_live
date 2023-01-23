from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.api.serializers import WorldSerializer
from src.apps.core.exceptions import NoChangeStateException, ExistingStateException, NonAliveCellsException
from src.apps.core.models import World
from src.apps.core.service import GameOfLife


class GenerateWorldView(APIView):
    serializer_class = WorldSerializer
    queryset = World.objects.all()

    def get(self, request):
        if self.queryset.count() == 0:
            w = World.objects.create(
                width=World.DEFAULT_WIDTH,
                height=World.DEFAULT_HEIGHT
            )
            serializer = self.serializer_class(w, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        w = World.objects.first()

        gol = GameOfLife(world=w)

        try:
            with transaction.atomic():
                gol.next_generation()
        except NonAliveCellsException:
            w.delete()
            return Response(
                "На поле не осталось ни одной живой клетки.",
                status=status.HTTP_400_BAD_REQUEST
            )
        except ExistingStateException:
            w.delete()
            return Response(
                "Конфигурация на очередном шаге в точности повторяет себя же на одном из более ранних шагов.",
                status=status.HTTP_400_BAD_REQUEST
            )
        except NoChangeStateException:
            w.delete()
            return Response(
                "При очередном шаге ни одна из клеток не меняет своего состояния.",
                status=status.HTTP_400_BAD_REQUEST
            )

        else:
            serializer = self.serializer_class(w, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
