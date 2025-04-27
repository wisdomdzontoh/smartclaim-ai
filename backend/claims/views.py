from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Claim
from .serializers import ClaimSerializer
from accounts.permissions import IsClaimOwnerOrHandler
from ai_processing.tasks import run_ai_on_claim



class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated, IsClaimOwnerOrHandler]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'superadmin':
            return Claim.objects.all()
        # customers see only their own; staff see their company
        if user.role == 'customer':
            return Claim.objects.filter(user=user)
        return Claim.objects.filter(company=user.company)
    

    

    def perform_create(self, serializer):
        claim = serializer.save(user=self.request.user, company=self.request.user.company)
        run_ai_on_claim.delay(claim.id)

