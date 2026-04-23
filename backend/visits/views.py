from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Visit
from .serializers import (
    VisitListSerializer, VisitDetailSerializer, VisitStartSerializer,
    VisitCompleteSerializer, VisitCancelSerializer, VisitAddNotesSerializer
)
from .services import VisitService
from .filters import VisitFilter
from users.permissions import IsFieldAgent, scope_visits


class VisitViewSet(viewsets.ModelViewSet):
    filterset_class = VisitFilter
    search_fields = ['location_name', 'notes']
    ordering_fields = ['started_at', 'completed_at', 'status']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_permissions(self):
        if self.action == 'start':
            return [IsAuthenticated(), IsFieldAgent()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = Visit.objects.select_related(
            'field_agent', 'field_agent__region', 'field_agent__team', 'task'
        )
        return scope_visits(qs, self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return VisitListSerializer
        if self.action == 'start':
            return VisitStartSerializer
        if self.action == 'complete':
            return VisitCompleteSerializer
        if self.action == 'cancel':
            return VisitCancelSerializer
        if self.action == 'add_notes':
            return VisitAddNotesSerializer
        return VisitDetailSerializer

    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Use /visits/start/ to begin a visit.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _assert_ownership(self, visit, user):
        if user.is_field_agent and visit.field_agent != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only manage your own visits.')

    @action(detail=False, methods=['post'], url_path='start')
    def start(self, request):
        serializer = VisitStartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        visit = VisitService.start_visit(validated_data=serializer.validated_data, field_agent=request.user)
        return Response(VisitDetailSerializer(visit).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        visit = self.get_object()
        self._assert_ownership(visit, request.user)
        serializer = VisitCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visit = VisitService.complete_visit(
            visit=visit,
            notes=serializer.validated_data['notes'],
            outcome=serializer.validated_data['outcome'],
            actor=request.user
        )
        return Response(VisitDetailSerializer(visit).data)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        visit = self.get_object()
        self._assert_ownership(visit, request.user)
        serializer = VisitCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visit = VisitService.cancel_visit(
            visit=visit, notes=serializer.validated_data.get('notes', ''), actor=request.user
        )
        return Response(VisitDetailSerializer(visit).data)

    @action(detail=True, methods=['patch'], url_path='notes')
    def add_notes(self, request, pk=None):
        visit = self.get_object()
        self._assert_ownership(visit, request.user)
        if visit.status == Visit.Status.CANCELLED:
            return Response({'detail': 'Cannot update notes on a cancelled visit.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VisitAddNotesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visit = VisitService.add_notes(visit=visit, notes=serializer.validated_data['notes'], actor=request.user)
        return Response(VisitDetailSerializer(visit).data)

    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        qs = self.get_queryset().filter(status=Visit.Status.STARTED)
        if request.user.is_field_agent:
            qs = qs.filter(field_agent=request.user)
        return Response(VisitDetailSerializer(qs.first()).data)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            'total': qs.count(),
            'by_status': {s: qs.filter(status=s).count() for s, _ in Visit.Status.choices},
            'by_outcome': {o: qs.filter(outcome=o).count() for o, _ in Visit.Outcome.choices},
        })
