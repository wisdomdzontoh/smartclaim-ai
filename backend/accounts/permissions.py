from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'superadmin'

class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) allowed for any authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        # write only if superadmin or same-company admin
        return (
            request.user.role == 'superadmin' or
            (request.user.role == 'company_admin' and obj.company == request.user.company)
        )

class IsClaimOwnerOrHandler(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # customers can only operate on their own claims
        if request.user.role == 'customer':
            return obj.user == request.user
        # handlers/supervisors and company_admin can operate on company claims
        return (
            request.user.role in ['claims_handler', 'supervisor', 'company_admin', 'superadmin']
            and obj.company == request.user.company
        )
