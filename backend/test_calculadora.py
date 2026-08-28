#!/usr/bin/env python3

"""
test_calculadora.py - Suite de pruebas automatizadas para Calculadora Confusa
Objetivo: Validar todas las HUs (HU1-HU5) funcionan correctamente

Uso:
    python backend/test_calculadora.py
  
Requisitos:
  pip install requests
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def test_connection():
    """Verificar conexión con backend"""
    print_header("HU0: Verificar Conexión")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        print_success(f"Servidor respondiendo en {BASE_URL}")
        print(f"  Status Code: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print_error(f"No se puede conectar a {BASE_URL}")
        print("  Asegúrate de que la aplicación está corriendo: python backend/calculadora.py")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False

def test_hu1_suma():
    """HU1: Servicio de Suma"""
    print_header("HU1: Servicio de Suma")
    
    test_cases = [
        {"num1": "1/2", "num2": "3/4", "desc": "Fracciones"},
        {"num1": "0.5", "num2": "0.75", "desc": "Decimales"},
        {"num1": "5", "num2": "3", "desc": "Enteros"},
        {"num1": "1/2", "num2": "0.5", "desc": "Mixto (fracción + decimal)"},
    ]
    
    passed = 0
    for test in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/suma",
                json={"num1": test["num1"], "num2": test["num2"]},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"{test['desc']}: {test['num1']} + {test['num2']} = {data.get('resultado_formateado')}")
                passed += 1
            else:
                print_error(f"{test['desc']}: HTTP {response.status_code}")
                
        except Exception as e:
            print_error(f"{test['desc']}: {e}")
    
    print(f"\nResultado HU1: {passed}/{len(test_cases)} pruebas pasadas")
    return passed == len(test_cases)

def test_hu2_resta_multiplicacion():
    """HU2: Resta y Multiplicación"""
    print_header("HU2: Resta y Multiplicación")
    
    test_cases = [
        {"endpoint": "resta", "num1": "1.5", "num2": "0.75", "desc": "Resta decimales"},
        {"endpoint": "resta", "num1": "3/2", "num2": "1/4", "desc": "Resta fracciones"},
        {"endpoint": "multiplica", "num1": "2/3", "num2": "3/4", "desc": "Multiplica fracciones"},
        {"endpoint": "multiplica", "num1": "2.5", "num2": "4", "desc": "Multiplica mixto"},
    ]
    
    passed = 0
    for test in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/{test['endpoint']}",
                json={"num1": test['num1'], "num2": test['num2']},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"{test['desc']}: {data.get('resultado_formateado')}")
                passed += 1
            else:
                print_error(f"{test['desc']}: HTTP {response.status_code}")
                
        except Exception as e:
            print_error(f"{test['desc']}: {e}")
    
    print(f"\nResultado HU2: {passed}/{len(test_cases)} pruebas pasadas")
    return passed == len(test_cases)

def test_hu3_historial():
    """HU3: Sistema de Registro (Historial)"""
    print_header("HU3: Historial de Operaciones")
    
    try:
        # Obtener historial
        response = requests.get(f"{BASE_URL}/historial", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            historial = data.get("historial", [])
            total = data.get("total", 0)
            
            print_success(f"Historial cargado: {total} operaciones")
            
            if historial:
                print("\nÚltimas operaciones:")
                for i, item in enumerate(historial[:3], 1):
                    print(f"  {i}. {item['num1']} {item['operacion']} {item['num2']} = {item['resultado']}")
                    print(f"     Timestamp: {item['timestamp']}")
            else:
                print_warning("Historial vacío (expected si es primera ejecución)")
            
            return True
        else:
            print_error(f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_hu4_division():
    """HU4: División con Validación"""
    print_header("HU4: División con Validación")
    
    print(f"{Colors.BOLD}Prueba 1: División normal{Colors.ENDC}")
    try:
        response = requests.post(
            f"{BASE_URL}/divide",
            json={"num1": "1", "num2": "2"},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"División exitosa: {data.get('resultado_formateado')}")
            test1_passed = True
        else:
            print_error(f"HTTP {response.status_code}")
            test1_passed = False
    except Exception as e:
        print_error(f"Error: {e}")
        test1_passed = False
    
    print(f"\n{Colors.BOLD}Prueba 2: División por cero (error esperado){Colors.ENDC}")
    try:
        response = requests.post(
            f"{BASE_URL}/divide",
            json={"num1": "5", "num2": "0"},
            timeout=TIMEOUT
        )
        
        if response.status_code == 400:
            data = response.json()
            print_success(f"Error capturado correctamente: {data.get('error')}")
            test2_passed = True
        elif response.status_code == 200:
            print_error("División por cero NO fue rechazada")
            test2_passed = False
        else:
            print_error(f"HTTP {response.status_code}")
            test2_passed = False
    except Exception as e:
        print_error(f"Error: {e}")
        test2_passed = False
    
    passed = sum([test1_passed, test2_passed])
    print(f"\nResultado HU4: {passed}/2 pruebas pasadas")
    return passed == 2

def test_hu5_health_status():
    """HU5: Telemetría y Health Check"""
    print_header("HU5: Health Check y Status")
    
    print(f"{Colors.BOLD}Prueba 1: /health endpoint{Colors.ENDC}")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health Status: {data.get('status')}")
            print(f"  Service: {data.get('service')}")
            print(f"  Uptime: {data.get('uptime')}")
            print(f"  Persistence: {data.get('persistence')}")
            test1_passed = True
        else:
            print_error(f"HTTP {response.status_code}")
            test1_passed = False
    except Exception as e:
        print_error(f"Error: {e}")
        test1_passed = False
    
    print(f"\n{Colors.BOLD}Prueba 2: /status endpoint{Colors.ENDC}")
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Application Status: {data.get('status')}")
            print(f"  Service: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
            print(f"  Uptime (segundos): {data.get('uptime_seconds')}")
            print(f"  Operations Logged: {data.get('operations_logged')}")
            print(f"  Persistence Writable: {data.get('persistence_writable')}")
            test2_passed = True
        else:
            print_error(f"HTTP {response.status_code}")
            test2_passed = False
    except Exception as e:
        print_error(f"Error: {e}")
        test2_passed = False
    
    passed = sum([test1_passed, test2_passed])
    print(f"\nResultado HU5: {passed}/2 pruebas pasadas")
    return passed == 2

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════╗")
    print("║   CALCULADORA CONFUSA - Test Suite HU1-HU5     ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backend URL: {BASE_URL}\n")
    
    # Verificar conexión
    if not test_connection():
        print(f"\n{Colors.RED}No se puede continuar sin conexión al backend{Colors.ENDC}")
        sys.exit(1)
    
    # Ejecutar pruebas
    results = {
        "HU1 (Suma)": test_hu1_suma(),
        "HU2 (Resta/Mult)": test_hu2_resta_multiplicacion(),
        "HU3 (Historial)": test_hu3_historial(),
        "HU4 (División)": test_hu4_division(),
        "HU5 (Health/Status)": test_hu5_health_status(),
    }
    
    # Resumen
    print_header("RESUMEN FINAL")
    total_passed = sum(results.values())
    total_tests = len(results)
    
    for name, result in results.items():
        status = f"{Colors.GREEN}✓ PASÓ{Colors.ENDC}" if result else f"{Colors.RED}✗ FALLÓ{Colors.ENDC}"
        print(f"{name:20} {status}")
    
    print(f"\n{Colors.BOLD}Total: {total_passed}/{total_tests} conjuntos de pruebas pasaron{Colors.ENDC}")
    
    if total_passed == total_tests:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODAS LAS HUs FUNCIONAN CORRECTAMENTE{Colors.ENDC}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  Algunas HUs requieren atención{Colors.ENDC}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
