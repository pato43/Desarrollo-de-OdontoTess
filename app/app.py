import reflex as rx
from app.pages.sign_in import sign_in
from app.pages.sign_up import sign_up
from app.pages.dashboard import dashboard
from app.pages.clinical_history import clinical_history
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.spinner(class_name="text-blue-600 h-8 w-8"),
        class_name="flex items-center justify-center min-h-screen bg-gray-50",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
    stylesheets=["/pdf_styles.css"],
)
app.add_page(
    index, route="/", on_load=AuthState.check_session
)
app.add_page(
    dashboard,
    route="/dashboard",
    on_load=AuthState.check_session,
)
app.add_page(
    sign_in,
    route="/sign-in",
    on_load=AuthState.check_session,
)
app.add_page(
    sign_up,
    route="/sign-up",
    on_load=AuthState.check_session,
)
app.add_page(
    clinical_history,
    route="/history/[patient_id]",
    on_load=AuthState.check_session,
)