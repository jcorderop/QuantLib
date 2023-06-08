# Pricing Rest-API

___
## Project Scope
  * Gather knowledge and document the steps needed to create a Python **Pricing Rest-API** using **Quantlib** as engine calculation.
  * Configure **FastAPI** with **Swagger** to simplify the testing of the Rest End-Points and to create the Rest Document.
  * How to use **Azure** as a service infrastructure.
    * Deploy locally into **Docker** and pushing images into **Azure Container Registry**.
    * Integrate with **Azure Active Directory** and register application for Authentication. e.g:
      * Back-End API.
      * FastAPI to authenticate.
      * Client that authenticate and can request via rest to the Back-End.
    * Deployment into **Azure App Service**.
  * CI/CD autonomization using **GitHub Actions**.

___
## Project Links:

* Project Set-up: </main/help/ENV_SETUP_README.md>
* Home Page: <http://localhost:8000/>
* API Swagger: <http://localhost:8000/docs>
* API Specification: <http://localhost:8000/redoc>

___
## [Quantlib](https://www.quantlib.org/)

QuantLib is an open-source software library which provides tools for software developers and practitioners interested in financial instrument valuation and related subjects. 
It is written in C++. It is a free/open-source library for modeling, trading, and risk management in real-life and it offers tools that are useful both for practical implementation and for advanced modeling.

* Other Example: 
  * <https://github.com/lballabio/QuantLib-SWIG/tree/master/Python/examples>
  * <http://gouthamanbalaraman.com/blog/quantlib-python-tutorials-with-examples.html>

---
## [FastAPI](https://fastapi.tiangolo.com/)

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

FastAPI simplifies the use of Swagger, it is a powerful easy-to-use suite of API developer tools for teams and individuals, enabling development across the entire API lifecycle, from design and documentation.

Below you can find the references and steps to register an application in Azure.
How to use fastapi-azure-s and configure a Python application with security.

* How-to set-up FastApi with security: <https://intility.github.io/fastapi-azure-auth/>
* How-to configure a client: <https://intility.github.io/fastapi-azure-auth/usage-and-faq/calling_your_apis_from_python>
* How-to personalize rest-api document: <https://fastapi.tiangolo.com/tutorial/metadata/>

