import reflex as rx
from app.states.clinic_state import ClinicState
from typing import Callable


def _form_section(title: str, *children) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            title,
            class_name="text-xl font-semibold text-gray-800 mb-4 border-b pb-2",
        ),
        rx.el.div(
            *children,
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-6",
        ),
        class_name="bg-white p-4 md:p-6 rounded-lg shadow-sm border border-gray-200 mb-8",
    )


def _editable_input(
    label: str,
    field_path: list[str],
    placeholder: str = "",
    type: str = "text",
    required: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-600",
        ),
        rx.el.input(
            default_value=ClinicState.get_history_value(
                ClinicState.selected_patient.historia_clinica,
                field_path,
            ),
            on_change=lambda value: ClinicState.update_history_field_str(
                field_path, value
            ),
            placeholder=placeholder,
            type=type,
            required=required,
            class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
        ),
        class_name="col-span-1",
    )


def _editable_textarea(
    label: str,
    field_path: list[str],
    placeholder: str = "",
    required: bool = False,
    rows: int = 3,
    is_local: bool = False,
    local_value: rx.Var[str] | None = None,
    on_change_local: rx.event.EventHandler | None = None,
) -> rx.Component:
    on_change_handler = rx.cond(
        is_local & (on_change_local != None),
        on_change_local,
        rx.call_script(
            f"new Event('{ClinicState.update_history_field_str.__name__}', {{ detail: {{ field_path: {field_path}, value: arguments[0] }} }})",
            _is_prop=True,
        ),
    )
    value_var = rx.cond(
        is_local,
        local_value,
        ClinicState.get_history_value(
            ClinicState.selected_patient.historia_clinica,
            field_path,
        ),
    )
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-600",
        ),
        rx.el.textarea(
            default_value=value_var,
            on_change=on_change_handler,
            placeholder=placeholder,
            required=required,
            class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
            rows=rows,
        ),
        class_name="col-span-1 md:col-span-2 lg:col-span-3",
    )


def _editable_select_bool(
    label: str, field_path: list[str]
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-600",
        ),
        rx.el.select(
            rx.el.option("No", value="false"),
            rx.el.option("Sí", value="true"),
            value=ClinicState.get_history_value(
                ClinicState.selected_patient.historia_clinica,
                field_path,
                False,
            ).to_string(),
            on_change=lambda value: ClinicState.update_history_field_bool(
                field_path, value
            ),
            class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white",
        ),
        class_name="col-span-1",
    )


def _editable_select_str(
    label: str,
    field_path: list[str],
    options: rx.Var[list[str]],
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-600",
        ),
        rx.el.select(
            rx.foreach(
                options,
                lambda option: rx.el.option(
                    option, value=option
                ),
            ),
            value=ClinicState.get_history_value(
                ClinicState.selected_patient.historia_clinica,
                field_path,
            ),
            on_change=lambda value: ClinicState.update_history_field_str(
                field_path, value
            ),
            class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white",
        ),
        class_name="col-span-1",
    )