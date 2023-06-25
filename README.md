# VirtuMart 💻🛍️

## Short Description 💡

VirtuMart is an online store that offers a wide range of products and services.

### Detailed Description 📄

VirtuMart is a web-based platform that allows users to browse and purchase various products and services. It provides a convenient and user-friendly interface for customers to explore different categories, view product details, and make secure online transactions.

The platform is built using the Django framework, a powerful and flexible web development toolkit written in Python. It leverages Django's built-in ORM (Object-Relational Mapping) to interact with a PostgreSQL database, ensuring efficient storage and retrieval of product information. VirtuMart also utilizes various Django extensions, such as django-allauth for authentication and authorization, django-debug-toolbar for debugging and performance monitoring, django-environ for managing environment variables, and django-redis for caching and session management. 🌐🐍

To ensure secure and reliable payment processing, VirtuMart integrates with Stripe, a popular payment processing platform for the internet. Stripe handles secure online transactions, allowing customers to make payments using their preferred payment methods. 💳💰

### Technologies

| Programming Languages | Web Development | Frameworks and Libraries | Databases | Tools and Technologies | Payments |
|-----------------------|-----------------|----------------------------|--------------|--------------------------|---------|
| Python | HTML | Django + ORM | PostgreSQL | Docker | Stripe |
|| CSS | django-allauth | | Celery (Redis) | |
|| JavaScript (JS) | django-debug-toolbar | | OAuth | |
|| | django-environ | | | |
|| | django-redis | | | |

### How to Run the Project 🚀

To run the VirtuMart project, you can choose either the venv (virtual environment) method or use the provided Dockerfile.

#### Running with venv

1. Set up a virtual environment and activate it:

    ```bash
    # Create and activate the virtual environment
    python3 -m venv venv
    source venv/Scripts/activate  # For Windows
    cd .\store\  # Navigate to the project root directory
    ```

2. Install the required dependencies using the `requirements.txt` file:

    ```bash
    # Install the dependencies
    pip install -r requirements.txt
    ```

3. Set up the necessary environment variables. You can create a `.env` file in the project root directory and define the required variables. Refer to the documentation for the specific environment variables needed.

4. Apply the database migrations:

    ```bash
    # Run database migrations
    python manage.py migrate
    ```

5. Load initial data into the database (optional):

    ```bash
    # Load initial data
    python manage.py loaddata dumpdata/categories.json
    python manage.py loaddata dumpdata/products.json
    ```

6. Start the development server:

    ```bash
    # Start the development server
    python manage.py runserver
    ```

7. Access the VirtuMart application by visiting `http://127.0.0.1:8000` in your web browser.

#### Running with Docker 🐋

1. Ensure that Docker is installed and running on your system.

2. Build the Docker image using the provided Dockerfile:

   ```bash
   # Build the Docker image
   docker build -t virtumart .
   ```

3. Run a Docker container using the built image:

   ```bash
   # Run the Docker container
   docker run -p 8000:8000 virtumart
   ```

4. Access the VirtuMart application by visiting `http://127.0.0.1:8000` in your web browser.

Please note that additional configuration steps may be required based on your specific environment and deployment needs. Refer to the project documentation for more detailed instructions.
