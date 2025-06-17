import reflex as rx
from app.states.clinic_state import (
    ClinicState,
    NotaEvolucion,
)
from app.states.auth_state import AuthState
from app.components.odontogram import interactive_odontogram
from app.components.form_helpers import (
    _form_section,
    _editable_input,
    _editable_textarea,
    _editable_select_bool,
    _editable_select_str,
)


def evolucion_note_item(
    note: NotaEvolucion, index: int
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Fecha: ",
                note["fecha_hora"],
                class_name="font-semibold text-gray-700",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: ClinicState.delete_evolucion_note(
                    index
                ),
                class_name="text-red-500 hover:text-red-700",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(
            "Procedimiento y Signos Vitales:",
            class_name="text-sm font-medium text-gray-600 mt-2",
        ),
        rx.el.p(
            note["procedimiento_signos_vitales"],
            class_name="text-sm text-gray-800 bg-gray-50 p-2 rounded-md",
        ),
        rx.el.p(
            "Observaciones:",
            class_name="text-sm font-medium text-gray-600 mt-2",
        ),
        rx.el.p(
            note["observaciones"],
            class_name="text-sm text-gray-800 bg-gray-50 p-2 rounded-md",
        ),
        class_name="border p-4 rounded-lg",
    )


def hoja_evolucion_section() -> rx.Component:
    return _form_section(
        "8. Hoja de Nota de Evolución",
        rx.el.div(
            rx.foreach(
                ClinicState.safe_seguimiento,
                evolucion_note_item,
            ),
            class_name="col-span-full space-y-4",
        ),
        rx.el.div(
            rx.el.h4(
                "Añadir Nueva Nota de Evolución",
                class_name="text-lg font-semibold text-gray-700 mb-3",
            ),
            _editable_textarea(
                "Procedimiento y Signos Vitales",
                ["nueva_nota_evolucion"],
                is_local=True,
                local_value=ClinicState.nueva_nota_evolucion,
                on_change_local=ClinicState.set_nueva_nota_evolucion,
            ),
            _editable_textarea(
                "Observaciones Adicionales",
                ["nueva_nota_observaciones"],
                is_local=True,
                local_value=ClinicState.nueva_nota_observaciones,
                on_change_local=ClinicState.set_nueva_nota_observaciones,
            ),
            rx.el.button(
                "Añadir Nota",
                on_click=ClinicState.add_evolucion_note,
                class_name="mt-2 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 text-sm font-medium",
            ),
            class_name="col-span-full mt-6 border-t pt-6",
        ),
    )


def ruta_clinica_section() -> rx.Component:
    return _form_section(
        "Odontograma Terapéutico y Ruta Clínica",
        _editable_input(
            "Periodontal",
            ["ruta_clinica", "periodontal"],
            placeholder="Ej. 18, 17, 16",
        ),
        _editable_input(
            "Endodental",
            ["ruta_clinica", "endodental"],
            placeholder="Ej. 21, 22",
        ),
        _editable_input(
            "Resinas/Incrustaciones",
            ["ruta_clinica", "resinas_incrustaciones"],
            placeholder="Ej. 36, 46",
        ),
        _editable_input(
            "Cirugía Bucal/Extracciones",
            ["ruta_clinica", "cirugia_extracciones"],
            placeholder="Ej. 18, 28, 38, 48",
        ),
        _editable_input(
            "Rehabilitación/Estético",
            ["ruta_clinica", "rehabilitacion_estetico"],
            placeholder="Ej. 11, 12, 21, 22",
        ),
        _editable_input(
            "Radiografía/Panorámica",
            ["ruta_clinica", "radiografia_panoramica"],
            placeholder="Ej. Completa",
        ),
        _editable_textarea(
            "Observaciones de Ruta Clínica",
            ["ruta_clinica", "observaciones"],
            rows=4,
        ),
    )


def consent_section() -> rx.Component:
    return _form_section(
        "Consentimiento Informado",
        rx.el.div(
            rx.el.p(
                "Manifiesto bajo protesta decir la verdad, que los datos vertidos en esta historia clínica fueron asentados conforme a la información proporcionada por el suscrito, siendo verídicos, confidenciales y para uso interno de la Universidad.",
                class_name="text-sm text-gray-700 mb-2",
            ),
            rx.el.p(
                "Por lo tanto, acepto mi responsabilidad Médico Legal en caso de cualquier error u omisión de los mismos.",
                class_name="text-sm text-gray-700 mb-4",
            ),
            rx.el.p(
                "De acuerdo a la ley General de Salud, titulo quinto capítulo único, artículo 100 y 103, afirma: NOM 168, SSAI-1998. Numeral de la DO.A.A. 10.11.3 el código civil en su artículo 1803 y 1812, en el reglamento de la ley General de Salud, en lo referente a prestación de atención médica artículo 80, 81, 82, 83.",
                class_name="text-xs text-gray-500",
            ),
            class_name="col-span-full bg-gray-50 p-4 rounded-lg border",
        ),
        rx.el.div(
            rx.el.input(
                type="checkbox",
                on_change=lambda value: ClinicState.update_history_field_bool(
                    ["firma_consentimiento", "aceptado"],
                    value,
                ),
                checked=ClinicState.get_history_value(
                    ClinicState.selected_patient.historia_clinica,
                    ["firma_consentimiento", "aceptado"],
                    False,
                ),
                class_name="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-600",
            ),
            rx.el.label(
                "El paciente acepta los términos y condiciones.",
                class_name="ml-2 block text-sm text-gray-900",
            ),
            class_name="col-span-full flex items-center mt-4",
        ),
    )


def clinical_history_form() -> rx.Component:
    return rx.el.div(
        _form_section(
            "1. Datos Generales",
            _editable_input(
                "Nombre Completo",
                ["datos_generales", "nombre_completo"],
                required=True,
            ),
            _editable_input(
                "Edad",
                ["datos_generales", "edad"],
                type="number",
                required=True,
            ),
            _editable_select_str(
                "Sexo",
                ["datos_generales", "sexo"],
                ClinicState.opciones_sexo,
            ),
            _editable_input(
                "Fecha de Nacimiento",
                ["datos_generales", "fecha_nacimiento"],
                type="date",
            ),
            _editable_select_str(
                "Estado Civil",
                ["datos_generales", "estado_civil"],
                ClinicState.opciones_estado_civil,
            ),
            _editable_select_str(
                "Escolaridad",
                ["datos_generales", "escolaridad"],
                ClinicState.opciones_escolaridad,
            ),
            _editable_input(
                "Ocupación",
                ["datos_generales", "ocupacion"],
            ),
            _editable_input(
                "Dirección",
                ["datos_generales", "direccion"],
            ),
            _editable_input(
                "Teléfono",
                ["datos_generales", "telefono"],
                type="tel",
            ),
            _editable_input(
                "Correo Electrónico",
                ["datos_generales", "correo"],
                type="email",
            ),
            _editable_input(
                "Responsable del Paciente",
                ["datos_generales", "responsable_paciente"],
            ),
        ),
        _form_section(
            "2. Antecedentes Dentales",
            _editable_textarea(
                "¿Es la primera vez que acude a consulta dental?",
                [
                    "antecedentes_dentales",
                    "primera_vez_consulta",
                ],
            ),
            _editable_textarea(
                "¿Cuál fue el motivo de su última consulta?",
                [
                    "antecedentes_dentales",
                    "motivo_ultima_consulta",
                ],
            ),
            _editable_textarea(
                "¿Ha tenido alguna experiencia negativa en el dentista?",
                [
                    "antecedentes_dentales",
                    "experiencia_negativa",
                ],
            ),
            _editable_select_bool(
                "¿Se ha golpeado sus dientes?",
                [
                    "antecedentes_dentales",
                    "golpeado_dientes",
                ],
            ),
            _editable_select_bool(
                "¿Rechina o aprieta sus dientes?",
                [
                    "antecedentes_dentales",
                    "rechina_dientes",
                ],
            ),
            _editable_select_bool(
                "¿Ha tenido dolor o chasquido en la mandíbula?",
                [
                    "antecedentes_dentales",
                    "dolor_chasquido_atm",
                ],
            ),
            _editable_select_bool(
                "¿Usa prótesis dental?",
                [
                    "antecedentes_dentales",
                    "protesis_dental",
                ],
            ),
            _editable_input(
                "Tipo de prótesis",
                ["antecedentes_dentales", "tipo_protesis"],
            ),
        ),
        _form_section(
            "3. Resumen de la Historia Médica y/o Factores de Riesgo",
            _editable_textarea(
                "Resumen", ["resumen_historia_medica"]
            ),
        ),
        _form_section(
            "4. Exploración Física Extraoral",
            _editable_textarea(
                "Cabeza",
                ["exploracion_fisica_extraoral", "cabeza"],
            ),
            _editable_textarea(
                "Cuello",
                ["exploracion_fisica_extraoral", "cuello"],
            ),
            _editable_textarea(
                "Ganglios Linfáticos",
                [
                    "exploracion_fisica_extraoral",
                    "ganglios_linfaticos",
                ],
            ),
        ),
        _form_section(
            "5. Articulación Temporomandibular (A.T.M.)",
            _editable_select_bool(
                "¿Ha tenido dolor?",
                ["articulacion_temporomandibular", "dolor"],
            ),
            _editable_select_bool(
                "¿Escucha o siente ruidos al abrir/cerrar la boca?",
                ["articulacion_temporomandibular", "ruido"],
            ),
            _editable_select_bool(
                "¿Dificultad para abrir/cerrar la boca?",
                [
                    "articulacion_temporomandibular",
                    "dificultad_abrir_cerrar",
                ],
            ),
            _editable_select_bool(
                "¿Amanece con dolor o cansancio muscular?",
                [
                    "articulacion_temporomandibular",
                    "cansancio_muscular",
                ],
            ),
            _editable_input(
                "Límite de la apertura bucal (mm)",
                [
                    "articulacion_temporomandibular",
                    "limitacion_apertura",
                ],
            ),
        ),
        _form_section(
            "6. Exploración de Tejidos Blandos de la Cavidad Oral",
            _editable_textarea(
                "Labios",
                ["exploracion_tejidos_blandos", "labios"],
            ),
            _editable_textarea(
                "Carrillos",
                [
                    "exploracion_tejidos_blandos",
                    "carrillos",
                ],
            ),
            _editable_textarea(
                "Encía",
                ["exploracion_tejidos_blandos", "encia"],
            ),
            _editable_textarea(
                "Vestíbulo",
                [
                    "exploracion_tejidos_blandos",
                    "vestibulo",
                ],
            ),
            _editable_textarea(
                "Paladar",
                ["exploracion_tejidos_blandos", "paladar"],
            ),
            _editable_textarea(
                "Orofaringe",
                [
                    "exploracion_tejidos_blandos",
                    "orofaringe",
                ],
            ),
            _editable_textarea(
                "Región Retromolar",
                [
                    "exploracion_tejidos_blandos",
                    "region_retromolar",
                ],
            ),
            _editable_textarea(
                "Piso de Boca",
                [
                    "exploracion_tejidos_blandos",
                    "piso_boca",
                ],
            ),
            _editable_textarea(
                "Frenillos",
                [
                    "exploracion_tejidos_blandos",
                    "frenillos",
                ],
            ),
            _editable_textarea(
                "Lengua",
                ["exploracion_tejidos_blandos", "lengua"],
            ),
            _editable_textarea(
                "Glándulas Salivales",
                [
                    "exploracion_tejidos_blandos",
                    "glandulas_salivales",
                ],
            ),
            _editable_textarea(
                "Resumen del Diagnóstico de Presunción Bucal",
                [
                    "exploracion_tejidos_blandos",
                    "resumen_diagnostico_presuncion_bucal",
                ],
            ),
        ),
        _form_section(
            "7. Odontograma Interactivo",
            interactive_odontogram(),
        ),
        ruta_clinica_section(),
        hoja_evolucion_section(),
        consent_section(),
        class_name="w-full",
    )