import reflex as rx
from app.states.clinic_state import ClinicState
from app.components.form_helpers import _editable_textarea


def _surface_button(
    tooth_number: str, surface: str, size_class: str
) -> rx.Component:
    is_missing = ClinicState.is_tooth_missing(
        ClinicState.selected_patient.historia_clinica,
        tooth_number,
    )
    finding = ClinicState.get_tooth_surface_finding(
        ClinicState.selected_patient.historia_clinica,
        tooth_number,
        surface,
    )
    return rx.el.button(
        on_click=lambda: ClinicState.update_tooth_surface(
            tooth_number, surface
        ),
        class_name=rx.cond(
            is_missing,
            f"bg-gray-400 {size_class} border-gray-500 border transition-colors cursor-not-allowed",
            rx.cond(
                finding != "",
                rx.cond(
                    finding == "Caries",
                    f"bg-red-500 {size_class} border-gray-600 border",
                    rx.cond(
                        finding == "Sellante",
                        f"bg-blue-500 {size_class} border-gray-600 border",
                        f"bg-yellow-400 {size_class} border-gray-600 border",
                    ),
                ),
                f"bg-gray-100 hover:bg-gray-300 {size_class} border-gray-400 border transition-colors",
            ),
        ),
        disabled=is_missing,
    )


def tooth_component(tooth_number: str) -> rx.Component:
    is_missing = ClinicState.is_tooth_missing(
        ClinicState.selected_patient.historia_clinica,
        tooth_number,
    )
    return rx.el.div(
        rx.el.p(
            tooth_number,
            class_name="text-center text-xs font-semibold text-gray-700",
        ),
        rx.el.div(
            rx.el.div(),
            _surface_button(
                tooth_number,
                "vestibular",
                "h-4 w-4 md:h-5 md:w-5",
            ),
            rx.el.div(),
            _surface_button(
                tooth_number,
                "mesial",
                "h-4 w-4 md:h-5 md:w-5",
            ),
            _surface_button(
                tooth_number,
                "oclusal",
                "h-5 w-5 md:h-6 md:w-6",
            ),
            _surface_button(
                tooth_number,
                "distal",
                "h-4 w-4 md:h-5 md:w-5",
            ),
            rx.el.div(),
            _surface_button(
                tooth_number,
                "lingual",
                "h-4 w-4 md:h-5 md:w-5",
            ),
            rx.el.div(),
            class_name="grid grid-cols-3 items-center justify-items-center gap-px w-16 h-16 md:w-20 md:h-20",
        ),
        rx.el.div(
            rx.el.input(
                type="checkbox",
                checked=is_missing,
                on_change=lambda _: ClinicState.toggle_tooth_missing(
                    tooth_number
                ),
                class_name="mr-1 h-3 w-3",
            ),
            rx.el.label("Ausente", class_name="text-xs"),
            class_name="flex items-center justify-center mt-1",
        ),
        class_name=rx.cond(
            is_missing,
            "opacity-50 p-2 border rounded-lg bg-white shadow-sm transition-opacity",
            "p-2 border rounded-lg bg-white shadow-sm transition-opacity",
        ),
    )


def odontogram_arch(
    title: str, teeth: list[str]
) -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            title,
            class_name="font-semibold text-center text-gray-800 mb-3",
        ),
        rx.el.div(
            rx.foreach(teeth, tooth_component),
            class_name="flex flex-row flex-wrap justify-center gap-1 md:gap-2",
        ),
        class_name="bg-gray-50 p-2 md:p-4 rounded-lg border",
    )


def interactive_odontogram() -> rx.Component:
    upper_arch = [str(i) for i in range(18, 10, -1)] + [
        str(i) for i in range(21, 29)
    ]
    lower_arch = [str(i) for i in range(48, 40, -1)] + [
        str(i) for i in range(31, 39)
    ]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Diagnóstico/Procedimiento:",
                    class_name="font-medium mr-2",
                ),
                rx.el.select(
                    rx.foreach(
                        ClinicState.odontogram_diagnostics,
                        lambda tool: rx.el.option(
                            tool, value=tool
                        ),
                    ),
                    on_change=ClinicState.set_odontogram_tool,
                    value=ClinicState.odontogram_tool,
                    class_name="px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white",
                ),
                class_name="flex items-center flex-wrap",
            ),
            rx.el.p(
                "Herramienta seleccionada: ",
                ClinicState.odontogram_tool,
                class_name="text-sm text-gray-600 mt-2",
            ),
            class_name="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg",
        ),
        rx.el.div(
            odontogram_arch("Arcada Superior", upper_arch),
            odontogram_arch("Arcada Inferior", lower_arch),
            class_name="space-y-6",
        ),
        _editable_textarea(
            "Notas Generales del Odontograma",
            ["odontograma", "general_notes"],
        ),
        class_name="col-span-1 md:col-span-2 lg:col-span-3",
    )