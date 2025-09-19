from rest_framework.serializers import ModelSerializer

from user.models import Pay, User


class PaySerializer(ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializers(ModelSerializer):
    payment = PaySerializer(many=True, source="pay_set", read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_fields = ["payment"]

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)
        return expanded_fields + self.Meta.extra_fields


class UserPublicSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "first_name", "country", "avatar"]
        read_only_fields = fields


class UserDetailSerializer(ModelSerializer):
    payment = PaySerializer(many=True, source="user", read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "payment",
        ]
