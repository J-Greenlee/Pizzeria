from django.shortcuts import render, redirect
from .models import Pizza, Topping
from .forms import PizzaForm, ToppingForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    return render(request, 'pizzas/index.html')

@login_required
def pizzas(request):
    pizzas = Pizza.objects.filter(owner=request.user).order_by('date_added')
    context = {'pizzas':pizzas}

    return render (request, 'pizzas/pizzas.html', context)

@login_required
def pizza(request, pizza_id):
    #show one pizza and toppings
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.order_by('-date_added')

    if pizza.owner != request.user:
        raise Http404

    context = {'pizza':pizza,'toppings':toppings}
    return render(request, 'pizzas/pizza.html',context)

@login_required
def new_pizza(request):
    if request.method != 'POST':
        form = PizzaForm()
    else:
        form = PizzaForm(data=request.POST)
        if form.is_valid():
            new_pizza = form.save(commit = False)
            new_pizza.owner = request.user
            new_pizza.save()
            
            return redirect('pizzas:pizzas')
    context = {'form':form}
    return render(request, 'pizzas/new_pizza.html', context)

@login_required
def new_topping(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)

    if pizza.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = ToppingForm()
    else:
        form = ToppingForm(data=request.POST)
        if form.is_valid():
            new_topping = form.save(commit=False)
            new_topping.pizza = pizza
            new_topping.save()
            return redirect('pizzas:pizza', pizza_id=pizza_id)
    context = {'pizza':pizza, 'form':form}
    return render(request, 'pizzas/new_topping.html',context)

@login_required
def edit_topping(request, topping_id):
    topping = Topping.objects.get(id=topping_id)
    pizza = topping.pizza

    if pizza.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = ToppingForm(instance=topping)
    else:
        form = ToppingForm(instance=topping, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('pizzas:pizza',pizza_id=pizza.id)
    
    context = {'topping':topping, 'pizza':pizza, 'form':form} #context is a dictionary that has all the data that passes through the html file
    return render(request,'pizzas/edit_topping.html', context)
