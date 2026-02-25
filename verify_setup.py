#!/usr/bin/env python
"""
Verification script to check if the API environment is properly configured.
Run this script to verify all dependencies and configurations are in place.

Usage: python verify_setup.py
"""

import sys
import os

# Terminal colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print(f"\n{Colors.BOLD}Checking Python Version...{Colors.END}")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"{Colors.GREEN}✓ Python {version.major}.{version.minor}.{version.micro} - OK{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}✗ Python {version.major}.{version.minor} - Requires 3.8+{Colors.END}")
        return False

def check_packages():
    """Check if required packages are installed"""
    print(f"\n{Colors.BOLD}Checking Required Packages...{Colors.END}")
    
    required_packages = {
        'django': 'Django',
        'rest_framework': 'Django REST Framework',
        'rest_framework_simplejwt': 'Django REST Framework SimpleJWT',
        'requests': 'Requests'
    }
    
    all_ok = True
    for package, display_name in required_packages.items():
        try:
            __import__(package)
            print(f"{Colors.GREEN}✓ {display_name} - Installed{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}✗ {display_name} - NOT installed{Colors.END}")
            all_ok = False
    
    return all_ok

def check_django_project():
    """Check if Django project structure is in place"""
    print(f"\n{Colors.BOLD}Checking Django Project Structure...{Colors.END}")
    
    required_files = [
        'manage.py',
        'autofare/settings.py',
        'autofare/urls.py',
        'autofare/wsgi.py',
        'users/models.py',
        'users/views.py',
        'users/serializers.py',
        'users/urls.py',
        'vehicles/models.py',
        'vehicles/views.py',
        'vehicles/serializers.py',
        'vehicles/urls.py',
        'toll/models.py',
        'toll/views.py',
        'toll/serializers.py',
        'toll/urls.py',
        'db.sqlite3'
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"{Colors.GREEN}✓ {file_path}{Colors.END}")
        else:
            print(f"{Colors.RED}✗ {file_path} - NOT FOUND{Colors.END}")
            all_ok = False
    
    return all_ok

def check_documentation():
    """Check if documentation files are present"""
    print(f"\n{Colors.BOLD}Checking Documentation Files...{Colors.END}")
    
    doc_files = [
        'API_DOCUMENTATION.md',
        'API_SETUP_GUIDE.md',
        'API_TEST_EXAMPLES.http',
        'API_IMPLEMENTATION_SUMMARY.md',
        'IMPLEMENTATION_CHECKLIST.md'
    ]
    
    all_ok = True
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            print(f"{Colors.GREEN}✓ {doc_file}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠ {doc_file} - NOT FOUND (Optional){Colors.END}")
    
    return all_ok

def check_test_files():
    """Check if test files are present"""
    print(f"\n{Colors.BOLD}Checking Test Files...{Colors.END}")
    
    test_files = [
        'test_api.py',
        'sample_data.py'
    ]
    
    all_ok = True
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"{Colors.GREEN}✓ {test_file}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠ {test_file} - NOT FOUND (Optional){Colors.END}")
    
    return all_ok

def check_django_settings():
    """Check if Django settings are configured correctly"""
    print(f"\n{Colors.BOLD}Checking Django Settings...{Colors.END}")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autofare.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Check if REST_FRAMEWORK is configured
        if 'REST_FRAMEWORK' in settings.__dict__:
            print(f"{Colors.GREEN}✓ REST_FRAMEWORK configured{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠ REST_FRAMEWORK not configured{Colors.END}")
        
        # Check if required apps are installed
        required_apps = ['rest_framework', 'users', 'vehicles', 'toll']
        missing_apps = [app for app in required_apps if app not in settings.INSTALLED_APPS]
        
        if not missing_apps:
            print(f"{Colors.GREEN}✓ All required apps installed{Colors.END}")
            for app in required_apps:
                if app in settings.INSTALLED_APPS:
                    print(f"  {Colors.GREEN}✓ {app}{Colors.END}")
        else:
            print(f"{Colors.RED}✗ Missing apps: {', '.join(missing_apps)}{Colors.END}")
        
        return not missing_apps
    except Exception as e:
        print(f"{Colors.RED}✗ Error checking settings: {str(e)}{Colors.END}")
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Automated Toll Collection System - Setup Verification    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Required Packages", check_packages()))
    results.append(("Project Structure", check_django_project()))
    results.append(("Django Settings", check_django_settings()))
    results.append(("Documentation Files", check_documentation()))
    results.append(("Test Files", check_test_files()))
    
    # Summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*60}{Colors.END}\n")
    
    for check_name, result in results:
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"{check_name:.<40} {status}")
    
    all_passed = all(result for _, result in results)
    
    # Final status
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed! System is ready to use.{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please review the errors above.{Colors.END}")
    
    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    if all_passed:
        print(f"{Colors.GREEN}1. Run migrations: python manage.py migrate{Colors.END}")
        print(f"{Colors.GREEN}2. Load sample data: python manage.py shell < sample_data.py{Colors.END}")
        print(f"{Colors.GREEN}3. Start server: python manage.py runserver{Colors.END}")
        print(f"{Colors.GREEN}4. Test API: python test_api.py{Colors.END}")
    else:
        print(f"{Colors.RED}1. Fix the errors listed above{Colors.END}")
        print(f"{Colors.RED}2. Run this script again to verify{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{Colors.RED}Verification failed with error: {str(e)}{Colors.END}")
        sys.exit(1)
