from django.shortcuts import render
from django.http import QueryDict
from math import sqrt

def ItIsInt(**kwargs) -> dict:
    '''return 2 dict
       first - error_list
       second - given argumets if they named as "a","b" or "c" '''
    
    errors={} # dict of error strings
    args={} # int argument or raw data if not integer value given
    for key in 'abc':
        if not kwargs.get(key):
            errors['err_'+key] = "коэффициент не определен"
            args[key]='' # no data - empty arg value (prevent None)
        else:
            try:
                #print("!!!we in tray!!! ",key," : ",kwargs.get(key))
                args[key] = int(kwargs[key])
                errors['err_'+key] = "" # no error - empty string value
            except ValueError:
                errors['err_'+key] = "коэффициент не целое число"
                args[key]=kwargs.get(key) # wrong data to show
    if kwargs.get('a') == '0':
        errors['err_a'] = "коэффициент при первом слагаемом уравнения не может быть равным нулю"
    return errors, args         


def discriminant(a,b,c):
    return b*b-(4*a*c)

def roots(discriminant,a,b) -> list:
    '''Return root(s) of quadratic equation if discriminant>=0'''
    rootlist=[]
    if discriminant > 0:
        rootlist.append((-b+sqrt(discriminant))/(2*a))
        rootlist.append((-b-sqrt(discriminant))/(2*a))
    elif discriminant == 0:
        rootlist.append(-b/(2*a))
    return rootlist
      
    
      
# Create your views here.
def quadratic_results(request):
    D=x1=x2=''
#    print(request.GET.dict())
    web_params=request.GET.dict()
    errors_dict,values_dict=(ItIsInt(**web_params))
#    print("err-lst=",errors_dict,'\narg-lst=',values_dict)
    if not any(errors_dict.values()): # if no errors - calculate discriminant
        D=discriminant(*values_dict.values())
        if D >= 0: # calc roots
            try:
                x1,x2=roots(D,values_dict['a'],values_dict['b']) # > 0
            except ValueError:
                x1=roots(D,values_dict['a'],values_dict['b'])[0] # = 0
        
    context = {**errors_dict, **values_dict,'discriminant': D,'root1': str(x1),'root2': str(x2)}
    print(context)
    print(type(x1))
    return render(request, 'results.html', context)