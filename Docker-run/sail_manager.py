# Display the banner at the beginning
print("""
===================================================
            ███╗   ███╗ █████╗ ██████╗  ██████╗ 
            ████╗ ████║██╔══██╗██╔══██╗██╔══██╗
            ██╔████╔██║███████║██║  ██║██║  ██║
            ██║╚██╔╝██║██╔══██║██║  ██║██║  ██║
            ██║ ╚═╝ ██║██║  ██║██████╔╝██████╔╝
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ 
                                                  
       Automated Install Sail Creator - By Eng-Mohamed Salah
===================================================
""")

# Alias sail == ./vendor/bin/sail
import os
import subprocess
import platform
from pathlib import Path

class ProjectManager:
    def __init__(self):
        self.current_os = platform.system()
        self.project_path = None

    def list_projects(self):
        """List all directories in current path"""
        projects = [d for d in Path.cwd().iterdir() if d.is_dir()]
        if not projects:
            raise FileNotFoundError("No projects found in current directory")
        return projects

    def select_project(self, projects):
        """Handle project selection with validation"""
        print("\nAvailable Projects:")
        for idx, project in enumerate(projects, 1):
            print(f"{idx}. {project.name}")

        while True:
            try:
                choice = int(input("\nEnter project number: "))
                if 1 <= choice <= len(projects):
                    return projects[choice - 1]
                print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def execute_command(self, command):
        """Execute shell command with error handling"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                cwd=self.project_path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"\nCommand output ({command}):\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\nError executing {command}:\n{e.stderr}")
            return False

    def run_installation_flow(self):
        """Main installation workflow"""
        if not self.execute_command("composer require laravel/sail --dev"):
            return False

        if not self.execute_command("php artisan sail:install"):
            return False

        return True

    def handle_publish(self):
        """Handle sail publishing"""
        if self.ask_yes_no("\nDo you want to modify Sail configuration?"):
            return self.execute_command("php artisan sail:publish")
        return True

    def handle_deployment(self):
        """Handle deployment options with custom domain input"""
        if self.ask_yes_no("\nDo you want to share publicly?"):
            subdomain = self.get_valid_subdomain()
            return self.execute_command(f"sail share --subdomain={subdomain}")
        
        if self.ask_yes_no("\nRun locally instead?"):
            return self.execute_command("sail up -d")
        
        return True

    def get_valid_subdomain(self):
        """Get and validate subdomain input with sanitization"""
        while True:
            subdomain = input("\nEnter your desired subdomain (e.g., 'myapp'): ").strip()
            cleaned_domain = self.sanitize_subdomain(subdomain)
            
            if cleaned_domain:
                return f"{cleaned_domain}.site"
            
            print("Invalid subdomain. Please use only letters, numbers, and hyphens (4-32 chars).")

    def sanitize_subdomain(self, domain):
        """Sanitize subdomain input using whitelist approach"""
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-")
        cleaned = ''.join(c for c in domain if c in allowed_chars)
        cleaned = cleaned.strip('-').lower()
        
        if 4 <= len(cleaned) <= 32 and '.' not in cleaned:
            return cleaned
        return None

    def handle_container(self):
        """Handle container interaction"""
        if self.ask_yes_no("\nAccess container shell?"):
            self.open_new_terminal("sail shell")

    def handle_shutdown(self):
        """Handle server shutdown"""
        if self.ask_yes_no("\nStop the server?"):
            return self.execute_command("sail down")
        return True

    def open_new_terminal(self, command):
        """Open new terminal window with command"""
        full_command = f'cd "{self.project_path}" && {command}'
        
        if self.current_os == 'Windows':
            subprocess.Popen(f'start cmd /k "{full_command}"', shell=True)
        elif self.current_os == 'Linux':
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', full_command])
        else:
            print(f"\nExecute manually in new terminal:\n{full_command}")

    @staticmethod
    def ask_yes_no(question):
        """Get validated yes/no input"""
        while True:
            answer = input(f"{question} (y/n): ").lower().strip()
            if answer in ('y', 'n'):
                return answer == 'y'
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    manager = ProjectManager()
    
    try:
        projects = manager.list_projects()
        manager.project_path = manager.select_project(projects)
        os.chdir(manager.project_path)
        
        print(f"\nWorking in: {manager.project_path}")

        if not manager.run_installation_flow():
            return

        manager.handle_publish()
        manager.handle_deployment()
        manager.handle_container()
        manager.handle_shutdown()

        print("\nOperation completed successfully!")

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()