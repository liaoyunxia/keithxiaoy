from django.shortcuts import render


def add_contract(request):
    title = '制作保理合同'
    buyer_count = range(1, 6)

    return render(request, 'add_contract.html', locals())
