print("""
===================================================
            ███╗   ███╗ █████╗ ██████╗  ██████╗ 
            ████╗ ████║██╔══██╗██╔══██╗██╔══██╗
            ██╔████╔██║███████║██║  ██║██║  ██║
            ██║╚██╔╝██║██╔══██║██║  ██║██║  ██║
            ██║ ╚═╝ ██║██║  ██║██████╔╝██████╔╝
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ 
                                                  
       Automated Install Setting Performance & Security - By Eng-Mohamed Salah
===================================================
""")


import os
import sys

def select_project():
    """📂 Select a project from current directory"""
    projects = [d for d in os.listdir() if os.path.isdir(d) and d != ".git"]
    
    if not projects:
        print("No projects available!")
        sys.exit(1)
        
    print("\nAvailable projects:")
    for i, p in enumerate(projects, 1):
        print(f"{i}. {p}")
        
    choice = int(input("\nEnter project number: ")) - 1
    return projects[choice]

def find_target_file(project_path):
    """🔍 Locate AppServiceProvider.php file"""
    target_path = os.path.join(project_path, "app", "Providers", "AppServiceProvider.php")
    print(f"\n🔍 Scanning path: {target_path}")
    
    if not os.path.exists(target_path):
        print("\n❌ Error: AppServiceProvider.php not found!")
        sys.exit(2)
        
    return target_path

def modify_file(file_path):
    """🛠️ Update empty boot function with enhanced version"""
    # Target empty boot pattern
    target_boot = "public function boot(): void\n    {\n        //"
    
    # New boot function with all configurations
    new_boot = """public function boot(): void
    {
        $this->configureUrl();
        $this->configureVite();
        $this->configureModels();
        $this->configureCommands();

        \\Illuminate\\Pagination\\Paginator::useBootstrapFour();
    }

    /**
     * Enable HTTPS in production
     */
    private function configureUrl()
    {
        if(app()->isProduction()) {
            \\Illuminate\\Support\\Facades\\URL::forceScheme('https');
        }
    }

    /**
     * Configure model strictness
     */
    private function configureModels()
    {
        \\Illuminate\\Database\\Eloquent\\Model::shouldBeStrict();
        \\Illuminate\\Database\\Eloquent\\Model::unguard();
    }

    /**
     * Protect against destructive commands
     */
    private function configureCommands()
    {
        \\Illuminate\\Support\\Facades\\DB::prohibitDestructiveCommands(
            app()->isProduction()
        );
    }

    /**
     * Optimize Vite asset loading
     */
    private function configureVite()
    {
        \\Illuminate\\Support\\Facades\\Vite::usePreloadStrategy('aggressive');
    """

    # Read and modify file
    modified = False
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        
        if target_boot in content:
            new_content = content.replace(target_boot, new_boot)
            f.seek(0)
            f.write(new_content)
            f.truncate()
            modified = True
            
    return modified

def print_explanation():
    """📝 Detailed function explanation"""
    explanation = """
    🛠️ Enhanced AppServiceProvider Configuration:

    1️⃣ boot() Method:
    - 🧩 Core initialization point
    - ⚡ Executes critical configurations
    - 🛡️ Security & Performance Setup

    2️⃣ configureUrl():
    - 🔐 Automatic HTTPS enforcement
    - 🌐 Production environment protection
    - 🛡️ Prevents man-in-the-middle attacks

    3️⃣ configureModels():
    - 🧪 Strict model validation
    - 🔓 Flexible mass assignment
    - 📊 Enhanced data integrity

    4️⃣ configureCommands():
    - 🚫 Blocks dangerous DB operations
    - 🛡️ Production database protection
    - 💾 Prevents accidental data loss

    5️⃣ configureVite():
    - 🚀 Aggressive asset prefetching
    - ⚡ Improved loading performance
    - 📦 Optimized resource delivery

    6️⃣ Paginator():
    - 📃 Handle data for paginations
    - ⚡ Improved loading performance
    """
    print(explanation)

def main():
    try:
        print("🚀 Starting AppServiceProvider Enhancer")
        project = select_project()
        file_path = find_target_file(project)
        
        if modify_file(file_path):
            print("\n✅ Successfully upgraded boot method!")
        else:
            print("\nℹ️ No changes needed - boot method already enhanced")
        
        print_explanation()
        
    except Exception as e:
        print(f"\n❌ Critical Error: {str(e)}")
        sys.exit(3)

if __name__ == "__main__":
    main()