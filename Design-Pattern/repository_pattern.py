import os
import sys
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

class BaseRepository implements BaseRepositoryInterface
{{
    protected $model;

    public function __construct($model)
    {{
        $this->model = $model;
    }}

    public function all()
    {{
        return $this->model::all();
    }}

    public function find($id)
    {{
        return $this->model::find($id);
    }}

    public function create(array $data)
    {{
        return $this->model::create($data);
    }}

    public function update($id, array $data)
    {{
        $record = $this->find($id);
        $record->update($data);
        return $record;
    }}

    public function delete($id)
    {{
        return $this->model::destroy($id);
    }}
}}
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
            '{model}' => '{model}',
            // Add more models as needed
        ];
    
        foreach ($repositories as $interface => $repository) {
            $this->app->bind(
                "App\\Repositories\\Contracts\\{$interface}RepositoryInterface",
                "App\\Repositories\\Eloquent\\{$repository}Repository"
            );
        }
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
    global BASE_DIR, REPOSITORIES_DIR, CONTRACTS_DIR, ELOQUENT_DIR, PROVIDERS_DIR
    
    BASE_DIR = project_path / 'app'
    REPOSITORIES_DIR = BASE_DIR / 'Repositories'
    CONTRACTS_DIR = REPOSITORIES_DIR / 'Contracts'
    ELOQUENT_DIR = REPOSITORIES_DIR / 'Eloquent'
    PROVIDERS_DIR = BASE_DIR / 'Providers'

def validate_project_structure():
    """🔍 Validate essential project directories"""
    if not BASE_DIR.exists():
        print(f"❌ 'app' directory not found in selected project!")
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
        if not model.isalpha():
            print("❌ Model name must contain only letters!")
            continue
        return model

def create_with_interface(model):
    """🔧 Create repository structure with interface"""
    try:
        # Ensure directories exist
        CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)
        ELOQUENT_DIR.mkdir(parents=True, exist_ok=True)
        PROVIDERS_DIR.mkdir(parents=True, exist_ok=True)

        # Create contract files
        base_interface_path = CONTRACTS_DIR / 'BaseRepositoryInterface.php'
        model_interface_path = CONTRACTS_DIR / f'{model}RepositoryInterface.php'
        base_repository_path = ELOQUENT_DIR / 'BaseRepository.php'
        model_repository_path = ELOQUENT_DIR / f'{model}Repository.php'
        provider_path = PROVIDERS_DIR / 'RepositoryServiceProvider.php'

        # Write files with proper error handling
        try:
            base_interface_path.write_text(TEMPLATES['base_interface'])
            model_interface_path.write_text(TEMPLATES['model_interface'].format(model=model))
            base_repository_path.write_text(TEMPLATES['base_repository'])
            model_repository_path.write_text(TEMPLATES['model_repository'].format(model=model))
        except Exception as e:
            print(f"❌ Error writing repository files: {str(e)}")
            # Clean up any partially created files
            for path in [base_interface_path, model_interface_path, base_repository_path, model_repository_path]:
                if path.exists():
                    path.unlink()
            return False

        # Update or create service provider
        try:
            if provider_path.exists():
                content = provider_path.read_text()
                new_binding = (
                    f"\n        $this->app->bind(\n"
                    f"            'App\\\\Repositories\\\\Contracts\\\\{model}RepositoryInterface',\n"
                    f"            'App\\\\Repositories\\\\Eloquent\\\\{model}Repository'\n"
                    f"        );"
                )
                
                if 'public function register()' in content:
                    content = content.replace(
                        'public function register()',
                        f'public function register()\n    {{{new_binding}\n    }}'
                    )
                    provider_path.write_text(content)
            else:
                provider_content = TEMPLATES['service_provider'].format(model=model)
                provider_path.write_text(provider_content)
        except Exception as e:
            print(f"❌ Error updating service provider: {str(e)}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error creating repository structure: {str(e)}")
        return False

def create_without_interface(model):
    """⚡ Create basic repository without interface"""
    try:
        # Ensure directory exists
        REPOSITORIES_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create repository file
        repository_path = REPOSITORIES_DIR / f'{model}Repository.php'
        repository_path.write_text(TEMPLATES['model_repository'].format(model=model))
        return True
    except Exception as e:
        print(f"❌ Error creating repository file: {str(e)}")
        return False

def main():
    try:
        print("\n🚀 Laravel Repository Pattern Generator")
        print("-------------------------------------")
        
        # Select project
        project_path = select_project()
        setup_paths(project_path)
        validate_project_structure()
        
        # Repository type selection
        print("\n🔧 Select repository type:")
        print("1. With Interface (Recommended)")
        print("2. Without Interface")
        choice = input("\n➡️ Enter choice (1/2): ").strip()

        # Get model name
        model = get_model_name()

        # Create directories based on choice
        if choice == '1':
            success = create_with_interface(model)
        else:
            success = create_without_interface(model)

        if not success:
            sys.exit(3)

        print_summary(project_path, model, choice == '1')

    except Exception as e:
        print(f"\n💥 Critical Error: {str(e)}")
        sys.exit(1)

def print_summary(project_path, model, with_interface):
    """📝 Print creation summary with emojis"""
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
        print(f"1. Add Service Provider to config/app.php:")
        print(f"   App\\Providers\\RepositoryServiceProvider::class")
    print(f"2. Use repository in controllers:")
    print(f"   use App\\Repositories\\{'Eloquent' if with_interface else ''}\\{model}Repository;")

if __name__ == "__main__":
    main()