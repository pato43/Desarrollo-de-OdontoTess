import reflex as rx
from app.states.clinic_state import ClinicState, Patient
from app.states.auth_state import AuthState


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Borrador",
                "bg-gray-100 text-gray-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
            ),
            (
                "Pendiente",
                "bg-yellow-100 text-yellow-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
            ),
            (
                "Aprobado",
                "bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
            ),
            (
                "Rechazado",
                "bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
            ),
            "bg-gray-100 text-gray-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
        ),
    )


def patient_list_item(patient: Patient) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    patient["nombre"],
                    class_name="font-semibold text-gray-800",
                ),
                rx.el.p(
                    patient["edad"],
                    " años",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            patient["fecha_registro"],
            class_name="px-4 py-3 text-sm text-gray-600 hidden md:table-cell",
        ),
        rx.el.td(
            status_badge(patient["status"]),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    "Ver/Editar",
                    href=f"/history/{patient['id']}",
                    class_name="text-blue-600 hover:underline font-medium",
                ),
                class_name="flex justify-end",
            ),
            class_name="px-4 py-3 text-right",
        ),
        class_name="border-b border-gray-200 hover:bg-gray-50",
    )


def add_patient_modal() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("plus", class_name="mr-2 h-4 w-4"),
            "Agregar Nuevo Paciente",
            on_click=ClinicState.toggle_add_patient_modal,
            class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-blue-600 hover:bg-blue-700 h-9 px-4 py-2",
        ),
        rx.el.dialog(
            rx.el.div(
                rx.el.h2(
                    "Registrar Nuevo Paciente",
                    class_name="text-lg font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Complete los datos para crear un nuevo registro de paciente.",
                    class_name="text-sm text-gray-600 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Nombre Completo",
                        class_name="text-sm font-medium",
                    ),
                    rx.el.input(
                        placeholder="Ej. Juan Pérez",
                        on_change=ClinicState.set_new_patient_name,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Edad",
                        class_name="text-sm font-medium",
                    ),
                    rx.el.input(
                        placeholder="Ej. 35",
                        type="number",
                        on_change=ClinicState.set_new_patient_age,
                        class_name="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=ClinicState.toggle_add_patient_modal,
                        class_name="cursor-pointer bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 text-sm font-medium transition-colors",
                    ),
                    rx.el.button(
                        "Guardar Paciente",
                        on_click=ClinicState.add_patient,
                        class_name="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm font-medium transition-colors",
                    ),
                    class_name="flex justify-end gap-2 mt-4",
                ),
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
            ),
            class_name="fixed inset-0 bg-black/50 w-screen h-screen backdrop-blur-sm open:flex items-center justify-center z-50",
            open=ClinicState.show_add_patient_modal,
        ),
    )


def student_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Mis Pacientes",
                class_name="text-2xl font-bold text-gray-800",
            ),
            add_patient_modal(),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Paciente",
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Fecha de Registro",
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600 hidden md:table-cell",
                        ),
                        rx.el.th(
                            "Estado",
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "", class_name="px-4 py-2"
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        ClinicState.student_patients,
                        patient_list_item,
                    )
                ),
                class_name="w-full text-sm text-left rtl:text-right text-gray-500",
            ),
            rx.cond(
                ClinicState.student_patients.length() == 0,
                rx.el.div(
                    rx.el.p(
                        "No tienes pacientes registrados. Haz clic en 'Agregar Nuevo Paciente' para comenzar.",
                        class_name="text-gray-500",
                    ),
                    class_name="text-center py-10",
                ),
                rx.fragment(),
            ),
            class_name="bg-white rounded-lg shadow-md border border-gray-100 overflow-x-auto",
        ),
        class_name="p-1",
    )