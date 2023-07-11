from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models.administrator import Administrator
from api.serializers.administrator import AdministratorSerializer


class AdministratorView(APIView):
    """
    API endpoint for managing administrators.

    Methods:
    - GET: Retrieve all administrators or a specific administrator by their administrator ID.
    - POST: Create a new administrator.
    - PUT: Update an existing administrator by their administrator ID.
    - DELETE: Delete an existing administrator by their administrator ID.
    """

    def get(self, request, administrator_id=None):
        """
        Retrieve all administrators or a specific administrator by their administrator ID.

        Parameters:
        - request: The HTTP request object.
        - administrator_id: The ID of the administrator to retrieve (optional).

        Returns:
        - If administrator_id is provided, returns the serialized administrator data.
        - If administrator_id is None, returns serialized data for all administrators.

        HTTP Methods: GET
        """
        if administrator_id is not None:
            return self.get_single_administrator(administrator_id)
        else:
            return self.get_all_administrators()

    def get_single_administrator(self, administrator_id):
        """
        Retrieve details of an administrator by their administrator ID.

        Parameters:
        - administrator_id: The ID of the administrator to retrieve.

        Returns:
        - If the administrator exists, returns the serialized administrator data.
        - If the administrator does not exist, returns an error response.
        """
        try:
            administrator = Administrator.objects.get(pk=administrator_id)
            serializer = AdministratorSerializer(administrator)
            return Response(serializer.data)
        except Administrator.DoesNotExist:
            return Response({"error": "Administrator not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_all_administrators(self):
        """
        Retrieve all administrators.

        Returns:
        - Serialized data for all administrators.
        """
        administrators = Administrator.objects.all()
        serializer = AdministratorSerializer(administrators, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new administrator.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the administrator is created successfully, returns the generated token.
        - If the administrator data is invalid, returns an error response.

        HTTP Methods: POST
        """
        serializer = AdministratorSerializer(data=request.data)
        if serializer.is_valid():
            # Salt and hash the password
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, administrator_id):
        """
        Update an existing administrator by their administrator ID.

        Parameters:
        - request: The HTTP request object.
        - administrator_id: The ID of the administrator to update.

        Returns:
        - If the administrator exists and the data is valid, returns the updated administrator data.
        - If the administrator does not exist or the data is invalid, returns an error response.

        HTTP Methods: PUT
        """
        try:
            administrator = Administrator.objects.get(pk=administrator_id)
        except Administrator.DoesNotExist:
            return Response({"error": "Administrator not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdministratorSerializer(administrator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, administrator_id):
        """
        Delete an existing administrator by their administrator ID.

        Parameters:
        - request: The HTTP request object.
        - administrator_id: The ID of the administrator to delete.

        Returns:
        - If the administrator exists, deletes the administrator and returns a success response.
        - If the administrator does not exist, returns an error response.

        HTTP Methods: DELETE
        """
        try:
            administrator = Administrator.objects.get(pk=administrator_id)
        except Administrator.DoesNotExist:
            return Response({"error": "Administrator not found."}, status=status.HTTP_404_NOT_FOUND)

        administrator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
