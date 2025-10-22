import numpy as np
import math
from scipy import stats
import random

# ===================== DISTRIBUCIONES CONTINUAS =====================
parametros_por_dist = {
    "uniforme_continua": ["a", "b"],
    "exponencial": ["lambd"],        # ← cambiar λ → lambd
    "normal_box_muller": ["mu", "sigma"],  # ← cambiar μ → mu, σ → sigma
    "gamma": ["alpha", "beta"],      # ← cambiar α, β → alpha, beta
    "weibull": ["alpha", "beta", "gamma_val"],  # ← coherente con la función
    "uniforme_discreta": ["a", "b"],
    "bernoulli": ["p"],
    "binomial": ["n_trials", "p"],
    "poisson": ["lambd"],           # ← igual que exponencial
    "geometrica": ["p"]
}


def uniforme_continua(a, b, n, numeros_uniformes):
    """Distribución Uniforme Continua U(a, b)"""
    return [a + (b - a) * r for r in numeros_uniformes[:n]]

def exponencial(lambd, n, numeros_uniformes):
    """Distribución Exponencial(λ)"""
    return [-math.log(1 - r) / lambd for r in numeros_uniformes[:n]]

def normal_box_muller(mu, sigma, n, numeros_uniformes):
    """Distribución Normal N(μ, σ) usando Box-Muller"""
    normales = []
    for i in range(0, n - n % 2, 2):
        u1, u2 = numeros_uniformes[i], numeros_uniformes[i+1]
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        normales.extend([mu + sigma * z0, mu + sigma * z1])
    
    if n % 2 == 1:
        u1, u2 = numeros_uniformes[n-1], numeros_uniformes[0]
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        normales.append(mu + sigma * z0)
    
    return normales[:n]

def gamma(alpha, beta, n, numeros_uniformes):
    """Distribución Gamma(α, β)"""
    # Método de aceptación-rechazo o usando suma de exponenciales
    if alpha == int(alpha):  # Si alpha es entero (Erlang)
        resultados = []
        for _ in range(n):
            producto = 1.0
            for _ in range(int(alpha)):
                u = random.choice(numeros_uniformes)
                producto *= u
            x = -beta * math.log(producto)
            resultados.append(x)
        return resultados
    else:
        # Usar scipy para alpha no entero
        return list(stats.gamma.rvs(alpha, scale=beta, size=n))

def weibull(alpha, beta, gamma_val, n, numeros_uniformes):
    """Distribución Weibull(α, β, γ)"""
    return [gamma_val + beta * (-math.log(1 - r))**(1/alpha) 
            for r in numeros_uniformes[:n]]

# ===================== DISTRIBUCIONES DISCRETAS =====================

def uniforme_discreta(a, b, n, numeros_uniformes):
    """Distribución Uniforme Discreta U(a, b)"""
    return [a + int((b - a + 1) * r) for r in numeros_uniformes[:n]]

def bernoulli(p, n, numeros_uniformes):
    """Distribución Bernoulli(p)"""
    return [1 if r < p else 0 for r in numeros_uniformes[:n]]

def binomial(n_trials, p, n, numeros_uniformes):
    """Distribución Binomial(n, p)"""
    resultados = []
    for i in range(n):
        exitos = sum(1 for _ in range(n_trials) if random.choice(numeros_uniformes) < p)
        resultados.append(exitos)
    return resultados

def poisson(lambd, n, numeros_uniformes):
    """Distribución Poisson(λ)"""
    resultados = []
    for i in range(n):
        k = 0
        producto = 1.0
        while producto > math.exp(-lambd):
            u = random.choice(numeros_uniformes)
            producto *= u
            k += 1
        resultados.append(k - 1)
    return resultados

def geometrica(p, n, numeros_uniformes):
    """Distribución Geométrica(p)"""
    return [math.ceil(math.log(1 - r) / math.log(1 - p)) 
            for r in numeros_uniformes[:n]]