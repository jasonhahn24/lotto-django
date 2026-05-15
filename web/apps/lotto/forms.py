from django import forms

class TicketPurchaseForm(forms.Form):
    PURCHASE_TYPES = [('manual', '수동 선택'), ('auto', '자동 선택')]
    purchase_type = forms.ChoiceField(choices=PURCHASE_TYPES, widget=forms.RadioSelect)
    num1 = forms.IntegerField(min_value=1, max_value=45, required=False)
    num2 = forms.IntegerField(min_value=1, max_value=45, required=False)
    num3 = forms.IntegerField(min_value=1, max_value=45, required=False)
    num4 = forms.IntegerField(min_value=1, max_value=45, required=False)
    num5 = forms.IntegerField(min_value=1, max_value=45, required=False)
    num6 = forms.IntegerField(min_value=1, max_value=45, required=False)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('purchase_type') == 'manual':
            nums = [cleaned.get(f'num{i}') for i in range(1, 7)]
            if any(n is None for n in nums):
                raise forms.ValidationError('수동 선택 시 6개 번호를 모두 입력하세요.')
            if len(set(nums)) != 6:
                raise forms.ValidationError('중복된 번호가 있습니다.')
        return cleaned