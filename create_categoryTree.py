# Display the banner at the beginning
print("""
===================================================
            ███╗   ███╗ █████╗ ██████╗  ██████╗ 
            ████╗ ████║██╔══██╗██╔══██╗██╔══██╗
            ██╔████╔██║███████║██║  ██║██║  ██║
            ██║╚██╔╝██║██╔══██║██║  ██║██║  ██║
            ██║ ╚═╝ ██║██║  ██║██████╔╝██████╔╝
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ 
                                                  
       Automated Create Category Tree Creator - By Eng-Mohamed Salah
===================================================
""")



import os
import subprocess

# Function to list files and folders in the current directory
def list_files_and_folders():
    print("Files and folders in the current directory:")
    items = os.listdir()  # Get all items in the current directory
    for i, item in enumerate(items):
        item_path = os.path.join(os.getcwd(), item)
        if os.path.isfile(item_path):
            print(f"{i + 1}. 📄 {item} (File)")
        elif os.path.isdir(item_path):
            print(f"{i + 1}. 📁 {item} (Folder)")
    return items

# Function to get the project path from the user
def get_project_path():
    print("\nOptions:")
    print("1. Use the current directory")
    print("2. Enter a custom project path")
    print("3. Choose a folder from the list above")
    choice = input("Choose an option (1, 2, or 3): ")

    if choice == "1":
        return os.getcwd()  # Use the current directory
    elif choice == "2":
        custom_path = input("Enter the full path to your Laravel project: ")
        if os.path.exists(custom_path):
            return custom_path
        else:
            print("❌ The provided path does not exist.")
            return None
    elif choice == "3":
        items = list_files_and_folders()
        folder_index = int(input("Enter the number of the folder you want to use: ")) - 1
        if 0 <= folder_index < len(items):
            selected_item = items[folder_index]
            selected_path = os.path.join(os.getcwd(), selected_item)
            if os.path.isdir(selected_path):
                return selected_path
            else:
                print("❌ The selected item is not a folder.")
                return None
        else:
            print("❌ Invalid folder number.")
            return None
    else:
        print("❌ Invalid choice.")
        return None

# Function to find the artisan file in the project path
def find_artisan_path(project_path):
    for root, dirs, files in os.walk(project_path):
        if "artisan" in files:
            return root  # Return the directory containing artisan
    return None  # Return None if artisan is not found

# Function to define paths based on the project path
def define_paths(project_path):
    models_path = os.path.join(project_path, "app", "Models")  # Updated path
    services_path = os.path.join(project_path, "app", "Http", "Services")
    category_model_path = os.path.join(models_path, "Category.php")
    category_service_path = os.path.join(services_path, "Category", "CategoryService.php")
    return models_path, services_path, category_model_path, category_service_path

# Function to create directories if they don't exist
def create_directories_if_not_exist(*paths):
    for path in paths:
        if not os.path.exists(path):
            print(f"Creating directory: {path}")
            os.makedirs(path)

# Step 1: Check if Category.php exists, and create it if it doesn't
def step_1(category_model_path, models_path, artisan_path):
    try:
        create_directories_if_not_exist(models_path)  # Ensure the directory exists
        if not os.path.exists(category_model_path):
            print("Step 1: Category.php not found. Creating...")
            subprocess.run(["php", "artisan", "make:model", "Category", "-mr"], check=True, cwd=artisan_path)
            print(f"✅ Step 1: File created at {category_model_path}")
        else:
            print(f"✅ Step 1: File already exists at {category_model_path}")
        return True
    except Exception as e:
        print(f"❌ Step 1 failed: {category_model_path} - {e}")
        return False

# Step 2: Add the `children()` method to the Category.php file
def step_2(category_model_path):
    try:
        # Open the Category.php file in read-write mode
        with open(category_model_path, "r+") as file:
            # Read the entire content of the file
            content = file.read()

            # Check if the `children()` method already exists in the file
            if "public function children()" not in content:
                # Find the position of the last closing brace "}" in the file
                last_brace_index = content.rfind("}")
                if last_brace_index == -1:
                    # If no closing brace is found, raise an exception
                    raise Exception("No closing brace '}' found in the file.")

                # Insert the new code (children() method) just before the last closing brace
                updated_content = (
                    content[:last_brace_index] +  # Content before the last "}"
                    "\n    public function children()\n    {\n        return $this->hasMany(Category::class, 'parent_id');\n    }\n" +  # New code to insert
                    content[last_brace_index:]  # Content after the last "}"
                )

                # Move the file pointer to the beginning of the file
                file.seek(0)
                # Write the updated content back to the file
                file.write(updated_content)
                # Truncate the file to remove any leftover content (if the new content is shorter than the old content)
                file.truncate()

                # Print success message
                print(f"✅ Step 2: Updated file {category_model_path}")
            else:
                # If the `children()` method already exists, print a message
                print(f"✅ Step 2: Code already exists in {category_model_path}")
        return True
    except Exception as e:
        # If an error occurs, print the error message
        print(f"❌ Step 2 failed: {category_model_path} - {e}")
        return False

# Step 3: Check if the Services directory exists, and create it if it doesn't
def step_3(services_path):
    try:
        create_directories_if_not_exist(services_path)  # Ensure the directory exists
        print(f"✅ Step 3: Directory exists at {services_path}")
        return True
    except Exception as e:
        print(f"❌ Step 3 failed: {services_path} - {e}")
        return False

# Step 4: Create the Category directory and CategoryService.php file
def step_4(category_service_path):
    try:
        category_folder_path = os.path.dirname(category_service_path)
        create_directories_if_not_exist(category_folder_path)  # Ensure the directory exists
        if not os.path.exists(category_service_path):
            print("Step 4: CategoryService.php not found. Creating...")
            with open(category_service_path, "w") as file:
                file.write('''<?php

namespace App\\Services\\Category;

use App\\Models\\Category;
use Illuminate\\Support\\Facades\\Cache;

class CategoryService
{
    public function buildTree()
    {
        return Cache::remember('categories_tree', 60, function () {
            return Category::with('children')->whereNull('parent_id')->get();
        });
    }
}
''')
            print(f"✅ Step 4: File created at {category_service_path}")
        else:
            print(f"✅ Step 4: File already exists at {category_service_path}")
        return True
    except Exception as e:
        print(f"❌ Step 4 failed: {category_service_path} - {e}")
        return False

# Main execution
if __name__ == "__main__":
    # List files and folders in the current directory
    items = list_files_and_folders()

    # Get the project path from the user
    project_path = get_project_path()
    if not project_path:
        print("❌ No valid project path provided. Exiting...")
        exit()

    # Find the artisan file
    artisan_path = find_artisan_path(project_path)
    if not artisan_path:
        print("❌ Could not find the artisan file. Are you sure this is a Laravel project?")
        exit()

    # Define paths based on the project path
    models_path, services_path, category_model_path, category_service_path = define_paths(project_path)

    # Execute steps
    steps = [
        lambda: step_1(category_model_path, models_path, artisan_path),
        lambda: step_2(category_model_path),
        lambda: step_3(services_path),
        lambda: step_4(category_service_path),
    ]

    for step in steps:
        if not step():
            break