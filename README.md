# Sistema de Gestión para Local Gastronómico

Este proyecto consiste en una aplicación fullstack orientada a la administración de un local gastronómico, permitiendo gestionar de forma simple y organizada las principales entidades del negocio: categorías, productos e ingredientes.

El sistema fue desarrollado con una arquitectura separada entre frontend y backend:

* **Frontend:** desarrollado con React + TypeScript + Vite + TailwindCSS, utilizando TanStack Query para el manejo de estado asíncrono y consumo de la API.
* **Backend:** desarrollado con FastAPI + SQLModel + PostgreSQL, aplicando una arquitectura basada en capas con Service, Repository y Unit of Work para mantener una mejor organización y escalabilidad del proyecto.

## Funcionalidades principales

* CRUD completo de Categorías
* CRUD completo de Productos
* CRUD completo de Ingredientes
* Asignación de categorías a productos
* Asignación de ingredientes a productos
* Visualización en formato tabla
* Modales para detalle, creación, edición y eliminación
* Validaciones de datos tanto en frontend como backend
* Manejo de excepciones con HTTPException
* Paginación mediante Query Parameters (`offset` y `limit`)

## Objetivo del proyecto

El objetivo principal fue aplicar buenas prácticas de desarrollo fullstack, integrando frontend y backend de forma profesional, utilizando patrones de diseño, validaciones, manejo de errores y una estructura escalable que permita continuar expandiendo el sistema a futuro.

## Video de presentación

Link al video explicativo del proyecto:

https://drive.google.com/file/d/1Sz6D6OHlMbqje2gP7T3dfI8HktfiI5xL/view?usp=drive_link
