import reflex as rx
from app.states.auth_state import AuthState


def sign_up_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Crea tu Cuenta en OdontoTess",
                class_name="text-2xl font-bold text-gray-800",
            ),
            rx.el.p(
                "Completa los detalles a continuación para registrarte.",
                class_name="text-sm text-gray-500",
            ),
            class_name="text-center mb-6",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Nombre Completo",
                    class_name="text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="text",
                    placeholder="Juan Pérez",
                    name="full_name",
                    required=True,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Correo Electrónico",
                    class_name="text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="email",
                    placeholder="usuario@ejemplo.com",
                    name="email",
                    required=True,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Contraseña",
                    class_name="text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="password",
                    name="password",
                    required=True,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Rol",
                    class_name="text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.el.option(
                        "Selecciona un rol",
                        value="",
                        disabled=True,
                    ),
                    rx.el.option(
                        "Estudiante", value="student"
                    ),
                    rx.el.option(
                        "Profesor", value="professor"
                    ),
                    name="role",
                    required=True,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white",
                    default_value="",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Crear Cuenta",
                type="submit",
                class_name="w-full bg-blue-600 text-white py-2 px-4 rounded-md font-semibold hover:bg-blue-700 transition-colors",
            ),
            rx.el.div(
                rx.el.span(
                    "¿Ya tienes una cuenta?",
                    class_name="text-sm text-gray-600",
                ),
                rx.el.a(
                    "Iniciar Sesión",
                    href="/sign-in",
                    class_name="text-sm text-blue-600 hover:underline font-medium",
                ),
                class_name="text-center mt-4 flex justify-center gap-2",
            ),
            on_submit=AuthState.sign_up,
            class_name="w-full",
        ),
        class_name="w-full max-w-md p-8 bg-white rounded-xl shadow-lg border border-gray-200",
    )