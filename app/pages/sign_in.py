import reflex as rx
from app.components.sign_in_card import sign_in_card
from app.states.auth_state import AuthState


def sign_in() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.image(
                src="/logo_design_upem.png",
                class_name="h-16 w-auto mb-4",
            ),
            sign_in_card(),
            class_name="flex flex-col items-center justify-center",
        ),
        class_name="font-['Inter'] flex items-center justify-center min-h-screen bg-gray-50 p-4",
    )