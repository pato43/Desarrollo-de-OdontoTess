import reflex as rx
from app.states.auth_state import AuthState
from app.states.clinic_state import ClinicState
from app.components.clinical_history_form import (
    clinical_history_form,
)
from app.pages.dashboard import dashboard_header
from app.components.student_dashboard import status_badge


def reject_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.h2(
                "Rechazar Historia Clínica",
                class_name="text-lg font-bold text-gray-800 mb-2",
            ),
            rx.el.p(
                "Por favor, ingrese las observaciones para el rechazo.",
                class_name="text-sm text-gray-600 mb-4",
            ),
            rx.el.textarea(
                placeholder="Ej. Faltan antecedentes personales...",
                on_change=ClinicState.set_reject_observation,
                class_name="w-full px-3 py-2 mt-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancelar",
                    on_click=ClinicState.toggle_reject_dialog,
                    class_name="cursor-pointer bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 text-sm font-medium",
                ),
                rx.el.button(
                    "Confirmar Rechazo",
                    on_click=ClinicState.reject_history,
                    class_name="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm font-medium",
                ),
                class_name="flex justify-end gap-2 mt-4",
            ),
            class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
        ),
        open=ClinicState.show_reject_dialog,
        class_name="fixed inset-0 bg-black/50 w-screen h-screen backdrop-blur-sm open:flex items-center justify-center z-50",
    )


def action_buttons() -> rx.Component:
    is_student_editable = AuthState.is_student & (
        (ClinicState.safe_status == "Borrador")
        | (ClinicState.safe_status == "Rechazado")
    )
    is_professor_review = AuthState.is_professor & (
        ClinicState.safe_status == "Pendiente"
    )
    return rx.el.div(
        rx.el.button(
            "Guardar Avances",
            on_click=rx.toast.success("Avances guardados."),
            class_name="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm font-medium transition-colors",
        ),
        rx.cond(
            is_student_editable,
            rx.el.button(
                "Enviar a Revisión",
                on_click=ClinicState.submit_for_review,
                disabled=ClinicState.is_history_form_invalid,
                class_name="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.fragment(),
        ),
        rx.cond(
            is_professor_review,
            rx.el.div(
                rx.el.button(
                    "Rechazar",
                    on_click=ClinicState.toggle_reject_dialog,
                    class_name="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 text-sm font-medium transition-colors",
                ),
                rx.el.button(
                    "Aprobar y Firmar",
                    on_click=ClinicState.approve_history,
                    class_name="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 text-sm font-medium transition-colors",
                ),
                class_name="flex gap-2 md:gap-4",
            ),
            rx.fragment(),
        ),
        rx.cond(
            ClinicState.safe_status == "Aprobado",
            rx.el.button(
                rx.icon(
                    "download", class_name="mr-2 h-4 w-4"
                ),
                "Descargar PDF",
                on_click=ClinicState.generate_pdf,
                class_name="bg-green-700 text-white px-4 py-2 rounded-md hover:bg-green-800 text-sm font-medium transition-colors inline-flex items-center",
            ),
            rx.fragment(),
        ),
        class_name="flex flex-wrap gap-2 md:gap-4 justify-end items-center",
    )


def history_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                ClinicState.safe_patient_name,
                class_name="text-2xl md:text-3xl font-bold text-gray-800",
            ),
            status_badge(ClinicState.safe_status),
            class_name="flex flex-wrap items-center gap-4",
        ),
        action_buttons(),
        class_name="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4",
    )


def clinical_history() -> rx.Component:
    return rx.el.div(
        dashboard_header(),
        rx.el.main(
            rx.cond(
                ClinicState.selected_patient,
                rx.el.div(
                    history_header(),
                    reject_modal(),
                    rx.cond(
                        ClinicState.safe_status
                        == "Rechazado",
                        rx.el.div(
                            rx.el.p(
                                "Observaciones del profesor:",
                                class_name="font-semibold text-red-700",
                            ),
                            rx.el.p(
                                ClinicState.safe_observaciones_rechazo,
                                class_name="bg-red-50 border border-red-200 text-red-800 p-3 rounded-md mb-6",
                            ),
                            class_name="w-full",
                        ),
                        rx.fragment(),
                    ),
                    clinical_history_form(),
                ),
                rx.el.div(
                    rx.spinner(
                        class_name="text-blue-600 h-8 w-8"
                    ),
                    rx.el.p(
                        "Cargando historia clínica...",
                        class_name="mt-4 text-gray-600",
                    ),
                    class_name="flex flex-col items-center justify-center h-full pt-16",
                ),
            ),
            class_name="container mx-auto p-2 sm:p-4 lg:p-6",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )