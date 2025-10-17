from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta

class ItemBase(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=200)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(1400)])
    estoque = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def dias_de_emprestimo(self) -> int:
        raise NotImplementedError

    def multa_por_dia(self) -> float:
        raise NotImplementedError

    @property
    def disponivel(self) -> bool:
        return self.estoque > 0

    def diminuir_estoque(self):
        if self.estoque <= 0:
            raise ValueError("Sem unidades disponíveis.")
        self.estoque -= 1
        self.save(update_fields=["estoque"])

    def aumentar_estoque(self):
        self.estoque += 1
        self.save(update_fields=["estoque"])

    def __str__(self) -> str:
        return f"{self.__class__.__name__}('{self.titulo}', {self.ano})"


class Livro(ItemBase):
    autor = models.CharField(max_length=120)
    isbn = models.CharField(max_length=20)

    def dias_de_emprestimo(self) -> int:
        return 14

    def multa_por_dia(self) -> float:
        return 1.5


class Revista(ItemBase):
    edicao = models.PositiveIntegerField()

    def dias_de_emprestimo(self) -> int:
        return 7

    def multa_por_dia(self) -> float:
        return 0.5


class MidiaDigital(ItemBase):
    estoque = models.PositiveIntegerField(default=0)

    def dias_de_emprestimo(self) -> int:
        return 30

    def multa_por_dia(self) -> float:
        return 0.0

    def diminuir_estoque(self): pass
    def aumentar_estoque(self): pass


class Emprestimo(models.Model):
    item_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    item_object_id = models.PositiveIntegerField()
    item = GenericForeignKey("item_content_type", "item_object_id")

    usuario = models.ForeignKey("auth.User", on_delete=models.PROTECT)
    criado_em = models.DateField(default=timezone.now)
    devolvido_em = models.DateField(null=True, blank=True)

    @property
    def em_aberto(self) -> bool:
        return self.devolvido_em is None

    @property
    def prazo(self):
        return self.criado_em + timedelta(days=self.item.dias_de_emprestimo())

    @property
    def dias_em_atraso(self) -> int:
        data_ref = self.devolvido_em or timezone.now().date()
        return max(0, (data_ref - self.prazo).days)

    def calcular_multa(self) -> float:
        return self.dias_em_atraso * float(self.item.multa_por_dia())

    def __str__(self):
        status = "aberto" if self.em_aberto else f"devolvido em {self.devolvido_em}"
        return f"[{status}] {self.item} -> {self.usuario} (prazo {self.prazo})"
