from django.db import transaction
from rest_framework import serializers

from .models import Socio, SocioCategoria
from categorias.models import Categoria
from categorias.serializers import CategoriaSerializer
from profesores.serializers import ProfesorSerializer


class SocioSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer(read_only=True)
    profesor_id = serializers.PrimaryKeyRelatedField(
        source="profesor",
        queryset=Socio._meta.get_field("profesor").related_model.objects.all(),
        allow_null=True,
        required=False,
    )
    categorias = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        write_only=True,
    )
    profesor_nombre = serializers.SerializerMethodField()

    def validate_dni(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("El DNI debe contener solo números")
        return str(value)

    class Meta:
        model = Socio
        fields = (
            "id",
            "nombre",
            "apellido",
            "dni",
            "email",
            "telefono",
            "fecha_inscripcion",
            "profesor_id",
            "profesor_nombre",
            "profesor",
            "categorias",
            "registra_deuda",
        )

    def get_profesor_nombre(self, obj):
        if not obj.profesor:
            return None
        return f"{obj.profesor.nombre} {obj.profesor.apellido}"

    def _sync_categorias(self, socio, categoria_ids):
        if categoria_ids is None:
            return
        categorias = list(Categoria.objects.filter(id__in=categoria_ids))
        if len(categorias) != len(set(categoria_ids)):
            raise serializers.ValidationError({"categorias": "Una o más categorías no existen"})
        SocioCategoria.objects.filter(socio=socio).delete()
        SocioCategoria.objects.bulk_create(
            [SocioCategoria(socio=socio, categoria=categoria) for categoria in categorias]
        )

    def create(self, validated_data):
        categoria_ids = validated_data.pop("categorias", [])
        with transaction.atomic():
            socio = Socio.objects.create(**validated_data)
            self._sync_categorias(socio, categoria_ids)
        return socio

    def update(self, instance, validated_data):
        categoria_ids = validated_data.pop("categorias", None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            self._sync_categorias(instance, categoria_ids)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        categorias = [
            item.categoria
            for item in instance.sociocategoria_set.select_related("categoria").all()
        ]
        data["categorias"] = CategoriaSerializer(categorias, many=True).data
        return data
