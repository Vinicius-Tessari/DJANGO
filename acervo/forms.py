from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Emprestimo, Livro, Revista, MidiaDigital


User = get_user_model()

def buscar_item_por_codigo(codigo: str):
    for Model in (Livro, Revista, MidiaDigital):
        try:
            return Model.objects.get(codigo=codigo)
        except Model.DoesNotExist:
            continue
    raise forms.ValidationError('Item não encontrado para este código.')

class EmprestimoForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())
    codigo_item = forms.CharField(max_length=20, help_text='Ex.: L-001, R-101, D-900')

    class Meta:
        model = Emprestimo
        fields = ('usuario',)

    def clean(self):
        cleaned = super().clean()
        codigo = cleaned.get('codigo_item')
        if codigo:
            item = buscar_item_por_codigo(codigo)
            cleaned['item_resolvido'] = item
        return cleaned
    
    def save(self, commit=True):
        cleaned = self.cleaned_data
        item = cleaned['item_resolvido']
        usuario = cleaned['usuario']
        if item.dias_de_emprestimo() == 0:
            raise forms.ValidationError('Item de consulta local (não emprestável).')
        item.diminuir_estoque()
        emp = Emprestimo(
            item_content_type=ContentType.objects.get_for_model(item.__class__),
            item_object_id=item.pk,
            usuario=usuario,
        )
        if commit: emp.save()
        return emp
