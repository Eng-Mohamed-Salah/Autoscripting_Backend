# Display the banner at the beginning
print("""
===================================================
            ███╗   ███╗ █████╗ ██████╗  ██████╗ 
            ████╗ ████║██╔══██╗██╔══██╗██╔══██╗
            ██╔████╔██║███████║██║  ██║██║  ██║
            ██║╚██╔╝██║██╔══██║██║  ██║██║  ██║
            ██║ ╚═╝ ██║██║  ██║██████╔╝██████╔╝
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ 
                                                  
       Automated Create Project Laravel Creator - By Eng-Mohamed Salah
===================================================
""")


import os
import platform
import subprocess

def detect_os():
    """Detect the operating system"""
    os_name = platform.system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Linux":
        return "linux"
    else:
        raise Exception("Unsupported operating system")

# Get Version Project Laravel
def get_laravel_version():
    """Get Laravel version from the user"""
    version = input("Enter the Laravel version you want to install (leave blank for the latest version): ").strip()
    if not version:
        print("The latest version of Laravel will be used.")
        return None
    return version

# Create Project Laravel
def create_laravel_project(version, project_name):
    """Create a Laravel project"""
    if version:
        command = f"composer create-project --prefer-dist laravel/laravel {project_name} {version}"
    else:
        command = f"composer create-project --prefer-dist laravel/laravel {project_name}"
    
    print(f"Creating Laravel project with name '{project_name}'...")
    subprocess.run(command, shell=True, check=True)

# Install Vendor Project
def install_composer_packages(project_name):
    """Install Composer packages"""
    skip = input("Do you want to skip installing Composer packages? (y/n): ").strip().lower()
    if skip == 'y':
        print("Skipping package installation.")
        return
    
    os.chdir(project_name)
    print("Installing Composer packages...")
    try:
        subprocess.run("composer install", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while installing packages. Trying with ignored requirements...")
        subprocess.run("composer install --ignore-platform-req=ext-grpc", shell=True, check=True)

# Function Configurations Project 
def configure_env_file():
    """Configure the .env file"""
    print("Configuring the .env file...")
    
    # Read the .env file
    with open(".env", "r") as file:
        lines = file.readlines()
    
    # Modify database settings
    new_lines = []
    for line in lines:
        if line.startswith("DB_CONNECTION=") and "mysql" not in line:
            line = "DB_CONNECTION=mysql\n"
        if line.strip().startswith("#DB_") or line.strip().startswith("# DB_"):
            line = line.replace("#", "", 1).strip()  
            line = line + "\n"  
        new_lines.append(line)
    
    # Write modifications to the .env file
    with open(".env", "w") as file:
        file.writelines(new_lines)
    
    # Prompt user for database credentials
    db_name = input("Enter the database name (DB_DATABASE): ").strip()
    db_user = input("Enter the database username (DB_USERNAME): ").strip()
    db_password = input("Enter the database password (DB_PASSWORD): ").strip()
    
    # Update the .env file with new values
    with open(".env", "r") as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith("DB_DATABASE="):
            lines[i] = f"DB_DATABASE={db_name}\n"
        elif line.startswith("DB_USERNAME="):
            lines[i] = f"DB_USERNAME={db_user}\n"
        elif line.startswith("DB_PASSWORD="):
            lines[i] = f"DB_PASSWORD={db_password}\n"
    
    with open(".env", "w") as file:
        file.writelines(lines)
    
    print(".env file updated successfully.")

# Create Rest API (only Laravel 11 )
def install_api_files():
    """Install API files if Laravel version is 11"""
    skip = input("Do you want to skip installing API files? (y/n): ").strip().lower()
    if skip == 'y':
        print("Skipping API installation.")
        return
    
    # Get Laravel version using 'php artisan -v'
    try:
        result = subprocess.run("php artisan -v", shell=True, capture_output=True, text=True, check=True)
        output = result.stdout
        if "Laravel Framework 11." in output:
            print("Installing API files for Laravel 11...")
            subprocess.run("php artisan install:api", shell=True, check=True)
        else:
            print("Skipping API installation (not Laravel 11).")
    except subprocess.CalledProcessError as e:
        print(f"Failed to check Laravel version: {e}")

# Create Link For Storage Project 
def create_storage_link():
    """Create storage link"""
    skip = input("Do you want to skip creating the storage link? (y/n): ").strip().lower()
    if skip == 'y':
        print("Skipping storage link creation.")
        return
    
    print("Creating storage link...")
    subprocess.run("php artisan storage:link", shell=True, check=True)

# Create Model With Arguments
def create_models():
    """Create models based on user input"""
    skip = input("Do you want to skip creating models? (y/n): ").strip().lower()
    if skip == 'y':
        print("Skipping model creation.")
        return
    
    try:
        num_models = int(input("How many models do you want to create? ").strip())
        if num_models <= 0:
            print("No models will be created.")
            return
        
        models = []
        for i in range(num_models):
            model_name = input(f"Enter the name of model {i + 1}: ").strip()
            if model_name:
                # Convert the first letter to uppercase (PascalCase)
                model_name = model_name[0].upper() + model_name[1:]
                models.append(model_name)
        
        if not models:
            print("No valid model names provided.")
            return
        
        # Ask if the user wants to apply all operations to all models
        apply_all = input("Do you want to apply all operations (controller, migration, resource, seed) to all models? (y/n): ").strip().lower()
        if apply_all == 'y':
            # Apply all operations to all models
            for model in models:
                print(f"Creating model with all operations: {model}...")
                subprocess.run(f"php artisan make:model {model} -mcrs", shell=True, check=True)
            print("All models created with full operations successfully!")
            return
        
        # If not applying all operations, ask for each model
        for model in models:
            print(f"\nConfiguring operations for model: {model}")
            print("Choose the operations you want to apply:")
            print("1. Controller")
            print("2. Migration")
            print("3. Resource")
            print("4. Seed")
            print("5. API")
            print("6. Requests")
            print("7. Controller with Migration")
            print("8. Controller with Migration and Resource")
            print("9. Controller with Migration, Resource, and Seed")
            
            choice = input("Enter your choice (1-9): ").strip()
            
            # Map choices to arguments
            options = {
                "1": "-c",
                "2": "-m",
                "3": "-r",
                "4": "-s",
                "5": "--api",
                "6": "-R",
                "7": "-mc",
                "8": "-mcr",
                "9": "-mcrs"
            }
            
            if choice in options:
                argument = options[choice]
                print(f"Creating model with selected operations: {model}...")
                subprocess.run(f"php artisan make:model {model} {argument}", shell=True, check=True)
            else:
                print("Invalid choice. Creating model without additional operations.")
                subprocess.run(f"php artisan make:model {model}", shell=True, check=True)
        
        print("Models created successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Generate Configurations Languages
def add_languages(os_type):
    """Add languages to the project"""
    add_lang = input("Do you want to add languages to your project? (y/n): ").strip().lower()
    if add_lang != 'y':
        print("Skipping language addition.")
        return
    
    # Publish language files
    print("Publishing language files...")
    subprocess.run("php artisan lang:publish", shell=True, check=True)
    
    # Ask for the number of languages
    try:
        num_languages = int(input("How many languages do you want to add? ").strip())
        if num_languages <= 0:
            print("No languages will be added.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    
    # Get language names
    languages = []
    for i in range(num_languages):
        lang_name = input(f"Enter the name of language {i + 1}: ").strip().lower()
        if lang_name:
            languages.append(lang_name)
    
    if not languages:
        print("No valid language names provided.")
        return
    
    # Copy and rename the 'en' folder for each language
    for lang in languages:
        src_folder = os.path.join("lang", "en")
        dest_folder = os.path.join("lang", lang)
        
        if os.path.exists(dest_folder):
            print(f"Language folder '{lang}' already exists. Skipping...")
            continue
        
        print(f"Creating language folder for '{lang}'...")
        if os_type == "windows":
            subprocess.run(f"xcopy {src_folder} {dest_folder} /E /I", shell=True, check=True)
        else:
            subprocess.run(f"cp -r {src_folder} {dest_folder}", shell=True, check=True)
    
    # Add available_locales to /config/app.php
    try:
        app_config_path = os.path.join("config", "app.php")
        with open(app_config_path, "r") as file:
            lines = file.readlines()
        
        # Find the line containing 'locale' => env('APP_LOCALE', 'en'),
        locale_line_index = -1
        for i, line in enumerate(lines):
            if "'locale' => env('APP_LOCALE', 'en')," in line:
                locale_line_index = i
                break
        
        if locale_line_index == -1:
            print("Could not find 'locale' line in /config/app.php. Skipping available_locales addition.")
        else:
            # Prepare the available_locales line
            available_locales = ["'en'"]  # English is always included
            available_locales.extend([f"'{lang}'" for lang in languages])
            available_locales_line = f"    'available_locales' => [{', '.join(available_locales)}],\n"
            
            # Insert the available_locales line after the locale line
            lines.insert(locale_line_index + 1, available_locales_line)
            
            # Write the updated content back to the file
            with open(app_config_path, "w") as file:
                file.writelines(lines)
            
            print("Added available_locales to /config/app.php successfully!")
    
    except Exception as e:
        print(f"Failed to update /config/app.php: {e}")
        return
    
    # Create SetAppLang middleware
    try:
        print("Creating SetAppLang middleware...")
        subprocess.run("php artisan make:middleware SetAppLang", shell=True, check=True)
        
        # Update the SetAppLang middleware file
        middleware_path = os.path.join("app", "Http", "Middleware", "SetAppLang.php")
        with open(middleware_path, "r") as file:
            lines = file.readlines()
        
        # Find the handle method
        handle_method_start = -1
        handle_method_end = -1
        for i, line in enumerate(lines):
            if "public function handle(Request $request, Closure $next): Response" in line:
                handle_method_start = i
            if handle_method_start != -1 and "return $next($request);" in line:
                handle_method_end = i
                break
        
        if handle_method_start == -1 or handle_method_end == -1:
            print("Could not find the handle method in SetAppLang.php. Skipping middleware update.")
        else:
            # Prepare the new handle method content
            new_handle_content = [
                "{\n"
                "        // Set the application locale based on the URL segment\n",
                "        if (!in_array($request->segment(2), config('app.available_locales'))) {\n",
                "            abort(400);\n",
                "        }\n",
                "\n",
                "        App::setLocale($request->segment(2));\n",
                "\n",
           
            ]
            
            # Replace the handle method content
            lines[handle_method_start + 1:handle_method_end] = new_handle_content
            
            # Write the updated content back to the file
            with open(middleware_path, "w") as file:
                file.writelines(lines)
            
            print("Updated SetAppLang middleware successfully!")
    
    except Exception as e:
        print(f"Failed to create or update SetAppLang middleware: {e}")
        return
    
    # Update /bootstrap/app.php to add SetAppLang middleware alias
    try:
        app_bootstrap_path = os.path.join("bootstrap", "app.php")
        with open(app_bootstrap_path, "r") as file:
            lines = file.readlines()
        
        # Find the line containing '->withMiddleware(function (Middleware $middleware) {'
        middleware_line_index = -1
        for i, line in enumerate(lines):
            if "->withMiddleware(function (Middleware $middleware) {" in line:
                middleware_line_index = i
                break
        
        if middleware_line_index == -1:
            print("Could not find middleware configuration in /bootstrap/app.php. Skipping middleware addition.")
        else:
            # Prepare the middleware alias addition
            middleware_alias_addition = [
                "        $middleware->alias([\n",
                "            'setapplang' => \\App\\Http\\Middleware\\SetAppLang::class,\n",
                "        ]);\n"
            ]
            
            # Insert the middleware alias addition after the middleware line
            lines.insert(middleware_line_index + 1, "".join(middleware_alias_addition))
            
            # Write the updated content back to the file
            with open(app_bootstrap_path, "w") as file:
                file.writelines(lines)
            
            print("Added SetAppLang middleware alias to /bootstrap/app.php successfully!")
    
    except Exception as e:
        print(f"Failed to update /bootstrap/app.php: {e}")
        return
    
    # Update /routes/web.php and /routes/api.php
    try:
        # Update web.php
        web_routes_path = os.path.join("routes", "web.php")
        if os.path.exists(web_routes_path):
            with open(web_routes_path, "r") as file:
                lines = file.readlines()
            
            # Find the line containing 'use Illuminate\Support\Facades\Route;'
            route_import_index = -1
            for i, line in enumerate(lines):
                if "use Illuminate\Support\Facades\Route;" in line:
                    route_import_index = i
                    break
            
            if route_import_index == -1:
                print("Could not find Route import in /routes/web.php. Skipping route group addition.")
            else:
                # Prepare the route group addition
                route_group_addition = [
                    "\n",
                    "Route::middleware('setapplang')->prefix('{locale}')->group(function()\n",
                    "{\n",
                    "    // Add Route Here\n",
                    "});\n"
                ]
                
                # Insert the route group addition after the Route import
                lines.insert(route_import_index + 1, "".join(route_group_addition))
                
                # Write the updated content back to the file
                with open(web_routes_path, "w") as file:
                    file.writelines(lines)
                
                print("Added route group to /routes/web.php successfully!")
        
        # Update api.php
        api_routes_path = os.path.join("routes", "api.php")
        if os.path.exists(api_routes_path):
            with open(api_routes_path, "r") as file:
                lines = file.readlines()
            
            # Find the line containing 'use Illuminate\Support\Facades\Route;'
            route_import_index = -1
            for i, line in enumerate(lines):
                if "use Illuminate\Support\Facades\Route;" in line:
                    route_import_index = i
                    break
            
            if route_import_index == -1:
                print("Could not find Route import in /routes/api.php. Skipping route group addition.")
            else:
                # Prepare the route group addition
                route_group_addition = [
                    "\n",
                    "Route::middleware('setapplang')->prefix('{locale}')->group(function()\n",
                    "{\n",
                    "    // Add Route Here\n",
                    "});\n"
                ]
                
                # Insert the route group addition after the Route import
                lines.insert(route_import_index + 1, "".join(route_group_addition))
                
                # Write the updated content back to the file
                with open(api_routes_path, "w") as file:
                    file.writelines(lines)
                
                print("Added route group to /routes/api.php successfully!")
    
    except Exception as e:
        print(f"Failed to update route files: {e}")
        return
    
    print("Languages added successfully!")


# Run Script 
def main():
    try:
        # Detect the operating system
        os_type = detect_os()
        print(f"Current operating system: {os_type.capitalize()}")
        
        # Get Laravel version
        laravel_version = get_laravel_version()
        
        # Project name
        project_name = input("Enter the project name: ").strip()
        if not project_name:
            raise Exception("A project name must be provided.")
        
        # Create Laravel project
        create_laravel_project(laravel_version, project_name)
        
        # Install Composer packages
        install_composer_packages(project_name)
        
        # Configure the .env file
        configure_env_file()
        
        # Install API files (only for Laravel 11)
        install_api_files()
        
        # Create storage link
        create_storage_link()
        
        # Create models
        create_models()
        
        # Add languages
        add_languages(os_type)
        
        # Return Successful
        print("Laravel project setup completed successfully!")

    # Handel Errors 
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()