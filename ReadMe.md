# Laravel Project Setup Script
# About the Author

<div style="text-align: center;">
  <img src="https://avatars.githubusercontent.com/u/64635889?v=4" alt="Author's Picture" style="border-radius: 50%; width: 150px; height: 150px;">
</div>


## Mohamed Salah
A passionate and experienced **backend Developer PHP** with over 5 years of expertise in designing, developing, and maintaining backend systems.

---

### Specializations
- Laravel Framework  
- Clean Code and SOLID Principles  
- Scalable and maintainable web applications  

---

### Experience and Vision
Mohamed Salah is dedicated to empowering developers with tools and automation scripts to enhance productivity. His work reflects a deep understanding of best practices and efficient development techniques.

- He specializes in creating scalable, maintainable solutions while adhering to clean code principles.
- Mohamed actively contributes to the developer community by sharing knowledge and solutions for common challenges.

---

### Contact Information
- **GitHub**: [github.com/Eng-Mohamed-Salah](https://github.com/Eng-Mohamed-Salah)  
- **Email**: [mohamed.m.salah.ahmed@gmail.com](mailto:mohamed.m.salah.ahmed@gmail.com)  
- **LinkedIn**: [linkedin.com/in/mohamed-m-salah](https://www.linkedin.com/in/mohamed-m-salah)  

Feel free to reach out with feedback, suggestions, or issues related to this script!


## Features
This script automates the setup and configuration of a Laravel project with the following features:
- **Automatic OS Detection**: Automatically detects whether you’re using Windows or Linux to ensure compatibility.
- **Interactive Project Creation**: Guides you to create Laravel projects and optionally specify the Laravel version.
- **Composer Package Installation**: Installs necessary dependencies and retries if errors occur.
- **Environment Configuration**: Automatically updates the `.env` file with database credentials and essential configurations.
- **API Setup for Laravel 11**: Installs API files if you're using Laravel 11.
- **Model Creation**: Allows dynamic creation of models with operations like migrations, controllers, resources, seeders, and more.
- **Language Management**: Adds new languages to your project with middleware to handle locale prefixes.
- **Storage Link Creation**: Simplifies the creation of symbolic links for storage.

---

## Installation and Usage

### Prerequisites
Before using this script, ensure that your system meets the following requirements:

1. **Install Python 3**  
   - Visit the [Python website](https://www.python.org/) and download the Python 3 installer for your operating system.
   - During installation, ensure that you check the "Add Python to PATH" option.
   - Verify the installation by running:
     ```bash
     python --version
     ```

2. **Install Required Tools**  
   - Install **PHP 8.2** and **Composer**:
     ```bash
     php --version
     composer --version
     ```
   - Ensure **Laravel** is installed globally:
     ```bash
     laravel --version
     ```
   - Set up a database like MySQL and confirm its connectivity.

3. **Basic Command-Line Knowledge**  
   - Familiarity with terminal commands is recommended.

---

### How to Use the Script
1. **Run the Script**  
   Open a terminal in the directory containing the script, then run:
   ```bash
   python install_laravel.py
