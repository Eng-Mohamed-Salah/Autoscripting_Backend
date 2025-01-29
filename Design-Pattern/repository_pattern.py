# Display the banner at the beginning
print("""
===================================================
            ███╗   ███╗ █████╗ ██████╗  ██████╗ 
            ████╗ ████║██╔══██╗██╔══██╗██╔══██╗
            ██╔████╔██║███████║██║  ██║██║  ██║
            ██║╚██╔╝██║██╔══██║██║  ██║██║  ██║
            ██║ ╚═╝ ██║██║  ██║██████╔╝██████╔╝
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ 
                                                  
       Automated Repository Pattern Project Laravel Creator - By Eng-Mohamed Salah
===================================================
""")

import os
import sys
import re
from pathlib import Path

# ========== Configuration ==========
TEMPLATES = {
    'base_interface': '''<?php

namespace App\\Repositories\\Contracts;

interface BaseRepositoryInterface
{
    public function all();
    public function find($id);
    public function create(array $data);
    public function update($id, array $data);
    public function delete($id);
}
''',

    'model_interface': '''<?php

namespace App\\Repositories\\Contracts;

interface {model}RepositoryInterface extends BaseRepositoryInterface
{{
    // Model-specific methods
}}
''',

    'base_repository': '''<?php

namespace App\\Repositories\\Eloquent;

use App\\Repositories\\Contracts\\BaseRepositoryInterface;
use Illuminate\\Database\\Eloquent\\Model;

class BaseRepository implements BaseRepositoryInterface
{
    /** @var Model */
    protected $model;

    public function __construct(Model $model)
    {
        $this->model = $model;
    }

    public function all()
    {
        return $this->model->all();
    }

    public function find($id)
    {
        return $this->model->find($id);
    }

    public function create(array $data)
    {
        return $this->model->create($data);
    }

    public function update($id, array $data)
    {
        $record = $this->find($id);
        $record->update($data);
        return $record;
    }

    public function delete($id)
    {
        return $this->model->destroy($id);
    }
}
''',

    'model_repository': '''<?php

namespace App\\Repositories\\Eloquent;

use App\\Repositories\\Contracts\\{model}RepositoryInterface;
use App\\Models\\{model};

class {model}Repository extends BaseRepository implements {model}RepositoryInterface
{{
    public function __construct()
    {{
        parent::__construct(new {model}());
    }}

    // Implement model-specific methods here
}}
''',

    'service_provider': '''<?php

namespace App\\Providers;

use Illuminate\\Support\\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{{
    public function register()
    {{
        $repositories = [
            // Add your repositories here
            {models}
        ];
    
        foreach ($repositories as $interface => $repository) {{
            $this->app->bind(
                "App\\Repositories\\Contracts\\${{interface}}RepositoryInterface",
                "App\\Repositories\\Eloquent\\${{repository}}Repository"
            );
        }}
    }}

    public function boot()
    {{
        //
    }}
}}
'''
}

def select_project():
    """📂 Select project directory"""
    projects = [d for d in os.listdir() if os.path.isdir(d) and d != ".git"]
    
    if not projects:
        print("❌ No projects found in current directory!")
        sys.exit(1)
        
    print("\n📂 Available projects:")
    for i, p in enumerate(projects, 1):
        print(f"{i}. {p}")
        
    choice = int(input("\n➡️ Select project number: ")) - 1
    return Path(projects[choice])

def setup_paths(project_path):
    """📍 Configure paths based on selected project"""
    global BASE_DIR, REPOSITORIES_DIR, CONTRACTS_DIR, ELOQUENT_DIR, PROVIDERS_DIR, MODELS_DIR
    
    BASE_DIR = project_path / 'app'
    REPOSITORIES_DIR = BASE_DIR / 'Repositories'
    CONTRACTS_DIR = REPOSITORIES_DIR / 'Contracts'
    ELOQUENT_DIR = REPOSITORIES_DIR / 'Eloquent'
    PROVIDERS_DIR = BASE_DIR / 'Providers'
    MODELS_DIR = BASE_DIR / 'Models'
    
    create_directories(CONTRACTS_DIR, ELOQUENT_DIR, PROVIDERS_DIR)

def validate_project_structure():
    """🔍 Validate essential project directories"""
    required = [BASE_DIR, MODELS_DIR]
    for path in required:
        if not path.exists():
            print(f"❌ Required directory not found: {path}")
            sys.exit(2)

def create_directories(*paths):
    """📂 Create required directories"""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

def get_model_name():
    """🖊️ Get validated model name from user"""
    while True:
        model = input("\n✨ Enter model name (e.g. User): ").strip()
        if not model:
            print("❌ Model name cannot be empty!")
            continue
        if not model[0].isupper():
            print("❌ Model name must start with a capital letter!")
            continue
        if not model.isalnum():
            print("❌ Model name must contain only alphanumeric characters!")
            continue
        if not (MODELS_DIR / f"{model}.php").exists():
            print(f"❌ Model file not found in {MODELS_DIR.relative_to(BASE_DIR)}/")
            continue
        return model

def update_service_provider(model):
    """🔄 Update RepositoryServiceProvider with new binding"""
    provider_path = PROVIDERS_DIR / 'RepositoryServiceProvider.php'
    try:
        if not provider_path.exists():
            # Create new service provider
            models_entry = f"'{model}' => '{model}',"
            content = TEMPLATES['service_provider'].format(models=models_entry)
            provider_path.write_text(content)
            return True

        # Update existing service provider
        content = provider_path.read_text()
        pattern = r'\$repositories\s*=\s*\[(.*?)\]'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            existing = match.group(1).strip()
            new_entry = f"'{model}' => '{model}',"
            
            if new_entry in existing:
                return True  # Already exists
            
            # Add new entry with proper formatting
            updated_entries = f"{existing}\n            {new_entry}" if existing else new_entry
            new_content = content.replace(
                match.group(0),
                f'$repositories = [\n            {updated_entries}\n        ];'
            )
            provider_path.write_text(new_content)
            return True
        
        # Fallback if pattern not found
        replacement = (
            "$repositories = [\n            "
            f"'{model}' => '{model}',\n        "
            "];\n\n        foreach ($repositories"
        )
        new_content = content.replace('foreach ($repositories', replacement)
        provider_path.write_text(new_content)
        return True

    except Exception as e:
        print(f"❌ Error updating service provider: {str(e)}")
        return False

def create_with_interface(model):
    """🔧 Create repository structure with interface"""
    created_files = []
    try:
        # Create contract files
        files = [
            (CONTRACTS_DIR / 'BaseRepositoryInterface.php', TEMPLATES['base_interface']),
            (CONTRACTS_DIR / f'{model}RepositoryInterface.php', 
             TEMPLATES['model_interface'].format(model=model)),
            (ELOQUENT_DIR / 'BaseRepository.php', TEMPLATES['base_repository']),
            (ELOQUENT_DIR / f'{model}Repository.php', 
             TEMPLATES['model_repository'].format(model=model))
        ]

        for path, content in files:
            try:
                path.write_text(content)
                created_files.append(path)
            except Exception as e:
                print(f"❌ Error writing {path.name}: {str(e)}")
                for f in created_files:
                    f.unlink(missing_ok=True)
                return False

        # Update service provider
        if not update_service_provider(model):
            for f in created_files:
                f.unlink(missing_ok=True)
            return False

        return True

    except Exception as e:
        print(f"❌ Error creating repository structure: {str(e)}")
        for f in created_files:
            f.unlink(missing_ok=True)
        return False

def print_summary(project_path, model, with_interface):
    """📝 Print creation summary"""
    print(f"\n✅ Successfully created in project: {project_path.name}/")
    print(f"📦 Model: {model}")
    print("📁 Created Structure:")
    
    if with_interface:
        print(f"├── 📂 {REPOSITORIES_DIR.relative_to(project_path)}")
        print(f"│   ├── 📂 Contracts")
        print(f"│   │   ├── 📄 BaseRepositoryInterface.php")
        print(f"│   │   └── 📄 {model}RepositoryInterface.php")
        print(f"│   └── 📂 Eloquent")
        print(f"│       ├── 📄 BaseRepository.php")
        print(f"│       └── 📄 {model}Repository.php")
        print(f"└── 📂 {PROVIDERS_DIR.relative_to(project_path)}")
        print(f"    └── 📄 RepositoryServiceProvider.php")
    else:
        print(f"└── 📂 {REPOSITORIES_DIR.relative_to(project_path)}")
        print(f"    └── 📄 {model}Repository.php")

    print("\n🔧 Next Steps:")
    if with_interface:
        print("1. Add to config/app.php providers:")
        print("   App\\Providers\\RepositoryServiceProvider::class")
    print("2. Use in controllers:")
    print(f"   use App\\Repositories\\{'Eloquent' if with_interface else ''}\\{model}Repository;")
    print("3. Run: composer dump-autoload\n")

def main():
    try:
        print("\n🚀 Laravel Repository Pattern Generator")
        print("-------------------------------------")
        
        project_path = select_project()
        setup_paths(project_path)
        validate_project_structure()
        
        print("\n🔧 Select repository type:")
        print("1. With Interface (Recommended)")
        print("2. Without Interface")
        choice = input("\n➡️ Enter choice (1/2): ").strip()

        model = get_model_name()

        if choice == '1':
            success = create_with_interface(model)
        else:
            print("❌ Basic repository without interface is not supported in this version")
            success = False

        if success:
            print_summary(project_path, model, choice == '1')
        else:
            print("\n❌ Failed to create repository structure")
            sys.exit(1)

    except Exception as e:
        print(f"\n💥 Critical Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()