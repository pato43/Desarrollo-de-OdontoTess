import reflex as rx
from app.states.auth_state import AuthState
from app.states.clinic_state import ClinicState
from app.components.student_dashboard import (
    student_dashboard,
)
from app.components.professor_dashboard import (
    professor_dashboard,
)


def dashboard_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="/logo_design_upem.png",
                    class_name="h-10 w-auto",
                ),
                rx.el.h1(
                    "OdontoTess",
                    class_name="text-xl font-bold text-white hidden sm:block",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.span(
                    "Bienvenido, ",
                    AuthState.current_user_name,
                    class_name="text-white text-sm hidden md:block",
                ),
                rx.el.button(
                    rx.icon(
                        tag="log-out",
                        class_name="h-4 w-4 md:mr-2",
                    ),
                    rx.el.span(
                        "Cerrar Sesión",
                        class_name="hidden md:block",
                    ),
                    on_click=AuthState.sign_out,
                    class_name="flex items-center bg-red-500 text-white px-3 py-2 rounded-md hover:bg-red-600 text-sm font-medium transition-colors",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="container mx-auto flex justify-between items-center p-4",
        ),
        class_name="bg-blue-600 w-full shadow-md",
    )


def dashboard() -> rx.Component:
    return rx.el.div(
        dashboard_header(),
        rx.el.main(
            rx.cond(
                AuthState.in_session,
                rx.cond(
                    AuthState.is_student,
                    student_dashboard(),
                    professor_dashboard(),
                ),
                rx.el.div(
                    rx.spinner(
                        class_name="text-blue-600 h-8 w-8"
                    ),
                    rx.el.p(
                        "Cargando Panel...",
                        class_name="mt-4 text-gray-600",
                    ),
                    class_name="flex flex-col items-center justify-center h-full pt-16",
                ),
            ),
            class_name="container mx-auto p-4 sm:p-6 lg:p-8",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
        on_mount=ClinicState.load_student_patients,
    )