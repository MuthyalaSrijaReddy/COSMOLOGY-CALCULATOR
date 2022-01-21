from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from scipy import integrate
import numpy as np

def calc(Z,Wm,Wl,Wk,Wr,Ho):
    #1.Present age of universe (in Gyears)
    #2.Age of the universe for user input redshift (in Gyears)
    #3.Look back time for user input redshift (in Gyears)
    c  = 3* 10**(8)
    # Tcmb,t0,err,T0,tz,err,Tz,del_T,r,err,rc,dl,da,ang =0

    def TIME(Z):
        return ( 1/( (1+Z)*(((Wm*((1+Z)**3)) + (Wr*((1+Z)**4)) + Wl + (Wk*((1+Z)**2)))**(1/2)) ) )
    t0,err = integrate.quad(TIME,0,np.inf)
    T0     = np.round(t0*( 3.08*(10**(19)) )/(Ho*3.15 * (10**(16))),3)            #in Giga years
    tz,err = integrate.quad(TIME,Z,100000)
    Tz     = np.round(tz*( 3.08*(10**(19)) )/(Ho*3.15 * (10**(16))),3)             #in Giga years
    del_T  = np.round((T0 - Tz),3) 
    print("1.Present age of universe : ",T0,"Gyears")
    print("2.Age of the universe for user input redshift (in Gyears):",Tz)
    print("3.Look back time for user input redshift (in Gyears):",del_T)
    
    #4.Comoving radial distance to user input redshift (in MPC)
    #5.Angular diameter distance to user input redshift (in MPC)
    #6.Angular scale at user input redshift (kpc/arcsec)
    #7.Luminosity distance to user input redshift (in MPC)

    def fun(Z,Wm,Wl,Wk,Wr):
        return (1*( 3.08*(10**(19)) )/(((Wm*((1+Z)**3)) + (Wr*((1+Z)**4)) + Wl + (Wk*((1+Z)**2)))**(1/2)))

    r,err = integrate.quad(fun,0,Z,args=(Wm,Wl,Wk,Wr))
    rc = np.round(r*c/(Ho*3.08* 10**(22)),3)               #(in MPC)
    dl = np.round((r*c*(1+Z))/(Ho*3.08* 10**(22)),3)       #(in MPC)
    da = np.round((r*c)/(Ho*(1+Z)*(3.08* 10**(22))),3)     #(in MPC)
    ang = np.round(da*(10**3)/(206265 ),3) 

    print("4.Comoving radial distance to user input redshift (in MPC)",rc)
    print("5.Angular diameter distance to user input redshift (in MPC)",da)
    print("6.Angular scale at user input redshift (kpc/arcsec)",ang)
    print("7.Luminosity distance to user input redshift (in MPC)",dl)
    
    #8. Temperature of CMB at user input redshift(K):

    Temp0 = 2.7
    Tcmb  = np.round(Temp0*(1+Z),3)  #in Kelvin
    print("8.Temperature of CMB at user input redshift(K):",Tcmb)
    return [Tcmb,t0,err,T0,tz,err,Tz,del_T,r,err,rc,dl,da,ang]


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def hai(request):
    print(request)
    Z=float(request.GET['Z'])
    Wm=float(request.GET['Wm'])
    Wl=float(request.GET['Wl'])
    Wk=float(request.GET['Wk'])
    Wr=float(request.GET['Wr'])
    Ho=float(request.GET['Ho'])
    [Tcmb,t0,err,T0,tz,err,Tz,del_T,r,err,rc,dl,da,ang]=calc(Z,Wm,Wl,Wk,Wr,Ho)
    print("-------------------------------------------------------------")
    print(Tcmb,t0,err,T0,tz,err,Tz,del_T,r,err,rc,dl,da,ang)
    return render(request,'results.html',{'Tcmb': Tcmb,'t0': t0, 'err':err,'T0':T0, 'tz' :tz, 'err' :err,'Tz':Tz ,'del_T':del_T,'r':r,'err':err,'rc':rc,'dl':dl,'da':da,'ang':ang})
def calculatorForm(request):
    return render(request,'index.html')
