from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Allow only author to edit/delete
     Allow any authenticated user to read 
    """
    def has_object_permission(self, request, view, obj):
        # Read-only methods are allowed for anyone
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are only allowed for the author 
        return obj.author == request.user