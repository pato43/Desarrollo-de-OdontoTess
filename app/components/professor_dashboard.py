import reflex as rx
from app.states.clinic_state import (
    ClinicState,
    Patient,
    Status,
)
from .student_dashboard import status_badge


def professor_patient_list_item(
    patient: Patient,
) -> rx.Component:
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
            patient["estudiante_email"],
            class_name="px-4 py-3 text-sm text-gray-600 hidden md:table-cell",
        ),
        rx.el.td(
            status_badge(patient["status"]),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    "Revisar",
                    href=f"/history/{patient['id']}",
                    class_name="text-blue-600 hover:underline font-medium",
                ),
                class_name="flex justify-end",
            ),
            class_name="px-4 py-3 text-right",
        ),
        class_name="border-b border-gray-200 hover:bg-gray-50",
    )


def professor_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Panel de Profesor",
            class_name="text-2xl font-bold text-gray-800 mb-4",
        ),
        rx.el.p(
            "Revisa y valida las historias clínicas de los estudiantes.",
            class_name="text-gray-600 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.select(
                    rx.el.option(
                        "Filtrar por Estudiante", value=""
                    ),
                    rx.foreach(
                        ClinicState.unique_student_emails,
                        lambda email: rx.el.option(
                            email, value=email
                        ),
                    ),
                    on_change=ClinicState.set_filter_student,
                    class_name="w-full md:w-auto px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white",
                ),
                rx.el.select(
                    rx.el.option(
                        "Filtrar por Estado", value=""
                    ),
                    rx.el.option(
                        "Pendiente", value="Pendiente"
                    ),
                    rx.el.option(
                        "Aprobado", value="Aprobado"
                    ),
                    rx.el.option(
                        "Rechazado", value="Rechazado"
                    ),
                    on_change=ClinicState.set_filter_status,
                    class_name="w-full md:w-auto px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white",
                ),
                class_name="flex flex-col md:flex-row gap-4 mb-4",
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
                                "Estudiante",
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
                            ClinicState.professor_patients,
                            professor_patient_list_item,
                        )
                    ),
                    class_name="w-full text-sm text-left text-gray-500",
                ),
                rx.cond(
                    ClinicState.professor_patients.length()
                    == 0,
                    rx.el.div(
                        rx.el.p(
                            "No hay historias clínicas para revisar.",
                            class_name="text-gray-500",
                        ),
                        class_name="text-center py-10",
                    ),
                    rx.fragment(),
                ),
                class_name="bg-white rounded-lg shadow-md border border-gray-100 overflow-x-auto",
            ),
            class_name="w-full",
        ),
    )