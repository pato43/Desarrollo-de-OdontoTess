import reflex as rx
import datetime
from typing import TypedDict, Literal, Optional, cast, Union
import copy
from app.states.auth_state import AuthState

Status = Literal[
    "Borrador", "Pendiente", "Aprobado", "Rechazado"
]
FieldValue = Union[str, int, bool, dict, list]


class ToothSurfaces(TypedDict, total=False):
    vestibular: str
    lingual: str
    distal: str
    mesial: str
    oclusal: str


class ToothState(TypedDict, total=False):
    surfaces: ToothSurfaces
    missing: bool


class Odontograma(TypedDict, total=False):
    teeth: dict[str, ToothState]
    general_notes: str


class AntecedentesDentales(TypedDict, total=False):
    primera_vez_consulta: str
    motivo_ultima_consulta: str
    experiencia_negativa: str
    golpeado_dientes: bool
    rechina_dientes: bool
    dolor_chasquido_atm: bool
    protesis_dental: bool
    tipo_protesis: str


class ExploracionFisicaExtraoral(TypedDict, total=False):
    cabeza: str
    cuello: str
    ganglios_linfaticos: str


class ArticulacionTemporomandibular(TypedDict, total=False):
    dolor: bool
    ruido: bool
    dificultad_abrir_cerrar: bool
    cansancio_muscular: bool
    limitacion_apertura: str


class ExploracionTejidosBlandos(TypedDict, total=False):
    labios: str
    carrillos: str
    encia: str
    vestibulo: str
    paladar: str
    orofaringe: str
    region_retromolar: str
    piso_boca: str
    frenillos: str
    lengua: str
    glandulas_salivales: str
    resumen_diagnostico_presuncion_bucal: str


class FirmaConsentimiento(TypedDict, total=False):
    aceptado: bool
    firma_data_url: str


class DatosGenerales(TypedDict, total=False):
    nombre_completo: str
    edad: str
    sexo: str
    fecha_nacimiento: str
    estado_civil: str
    escolaridad: str
    ocupacion: str
    direccion: str
    telefono: str
    correo: str
    fecha_ingreso: str
    responsable_paciente: str


class DatosAdministrativos(TypedDict, total=False):
    matricula_estudiante: str
    nombre_estudiante: str
    profesor_responsable: str


class AntecedentesHeredoFamiliares(TypedDict, total=False):
    diabetes: bool
    hipertension: bool
    cancer: bool
    tuberculosis: bool
    enfermedades_mentales: bool
    otros: str


class AntecedentesPersonalesPatologicos(
    TypedDict, total=False
):
    hospitalizaciones: str
    cirugias: str
    alergias: str
    medicamentos_actuales: str
    enfermedades_actuales: str
    vacunas_recientes: str


class AntecedentesPersonalesNoPatologicos(
    TypedDict, total=False
):
    higiene_bucal: str
    frecuencia_cepillado: str
    uso_hilo_enjuague: str
    consumo_tabaco: str
    consumo_alcohol: str
    consumo_drogas: str
    dieta: str


class PadecimientoActual(TypedDict, total=False):
    motivo_consulta: str
    descripcion_problema: str
    evolucion: str
    factores_asociados: str


class ExploracionClinicaGeneral(TypedDict, total=False):
    frecuencia_cardiaca: str
    presion_arterial: str
    temperatura: str
    saturacion: str
    peso: str
    talla: str
    estado_general: str


class Diagnostico(TypedDict, total=False):
    clinico: str
    cie_10: str
    diferencial: str
    pronostico: str


class PlanTratamiento(TypedDict, total=False):
    fases: str
    procedimientos: str
    frecuencia_citas: str
    materiales: str


class NotaEvolucion(TypedDict, total=False):
    fecha_hora: str
    procedimiento_signos_vitales: str
    observaciones: str


class RutaClinica(TypedDict, total=False):
    periodontal: str
    endodental: str
    resinas_incrustaciones: str
    cirugia_extracciones: str
    rehabilitacion_estetico: str
    radiografia_panoramica: str
    observaciones: str


class ClinicalHistory(TypedDict, total=False):
    datos_generales: DatosGenerales
    datos_administrativos: DatosAdministrativos
    antecedentes_heredo_familiares: (
        AntecedentesHeredoFamiliares
    )
    antecedentes_personales_patologicos: (
        AntecedentesPersonalesPatologicos
    )
    antecedentes_personales_no_patologicos: (
        AntecedentesPersonalesNoPatologicos
    )
    padecimiento_actual: PadecimientoActual
    exploracion_clinica_general: ExploracionClinicaGeneral
    exploracion_fisica_extraoral: ExploracionFisicaExtraoral
    articulacion_temporomandibular: (
        ArticulacionTemporomandibular
    )
    exploracion_tejidos_blandos: ExploracionTejidosBlandos
    odontograma: Odontograma
    diagnostico: Diagnostico
    plan_tratamiento: PlanTratamiento
    seguimiento: list[NotaEvolucion]
    firma_consentimiento: FirmaConsentimiento
    antecedentes_dentales: AntecedentesDentales
    resumen_historia_medica: str
    ruta_clinica: RutaClinica


class Patient(TypedDict):
    id: str
    nombre: str
    edad: int
    fecha_registro: str
    status: Status
    estudiante_email: str
    historia_clinica: ClinicalHistory
    firma_paciente_url: Optional[str]
    firma_profesor_url: Optional[str]
    fecha_firma_profesor: Optional[str]
    observaciones_rechazo: Optional[str]


def create_empty_history() -> ClinicalHistory:
    return {
        "datos_generales": {},
        "datos_administrativos": {},
        "antecedentes_heredo_familiares": {
            "diabetes": False,
            "hipertension": False,
            "cancer": False,
            "tuberculosis": False,
            "enfermedades_mentales": False,
        },
        "antecedentes_personales_patologicos": {},
        "antecedentes_personales_no_patologicos": {},
        "padecimiento_actual": {},
        "exploracion_clinica_general": {},
        "exploracion_fisica_extraoral": {},
        "articulacion_temporomandibular": {
            "dolor": False,
            "ruido": False,
            "dificultad_abrir_cerrar": False,
            "cansancio_muscular": False,
            "limitacion_apertura": "",
        },
        "exploracion_tejidos_blandos": {},
        "odontograma": {"teeth": {}, "general_notes": ""},
        "diagnostico": {},
        "plan_tratamiento": {},
        "seguimiento": [],
        "firma_consentimiento": {
            "aceptado": False,
            "firma_data_url": "",
        },
        "antecedentes_dentales": {
            "golpeado_dientes": False,
            "rechina_dientes": False,
            "dolor_chasquido_atm": False,
            "protesis_dental": False,
        },
        "resumen_historia_medica": "",
        "ruta_clinica": {},
    }


def create_initial_patients() -> list[Patient]:
    today = datetime.date.today().isoformat()
    history1 = create_empty_history()
    history1["datos_generales"].update(
        {"nombre_completo": "Ana Torres", "edad": "34"}
    )
    history1["datos_administrativos"].update(
        {
            "matricula_estudiante": "estudiante@odontotess.com",
            "nombre_estudiante": "Juan Pérez Estudiante",
        }
    )
    history1["padecimiento_actual"][
        "motivo_consulta"
    ] = "Revisión general y limpieza."
    history1["odontograma"]["teeth"] = {
        "16": {"surfaces": {"oclusal": "Caries"}},
        "36": {"missing": True},
    }
    history2 = create_empty_history()
    history2["datos_generales"].update(
        {"nombre_completo": "Carlos Ruiz", "edad": "52"}
    )
    history2["datos_administrativos"].update(
        {
            "matricula_estudiante": "estudiante@odontotess.com",
            "nombre_estudiante": "Juan Pérez Estudiante",
        }
    )
    history2["padecimiento_actual"][
        "motivo_consulta"
    ] = "Dolor en molar superior derecho."
    return [
        {
            "id": "p1",
            "nombre": "Ana Torres",
            "edad": 34,
            "fecha_registro": today,
            "status": "Borrador",
            "estudiante_email": "estudiante@odontotess.com",
            "historia_clinica": history1,
            "firma_paciente_url": None,
            "firma_profesor_url": None,
            "fecha_firma_profesor": None,
            "observaciones_rechazo": None,
        },
        {
            "id": "p2",
            "nombre": "Carlos Ruiz",
            "edad": 52,
            "fecha_registro": today,
            "status": "Pendiente",
            "estudiante_email": "estudiante@odontotess.com",
            "historia_clinica": history2,
            "firma_paciente_url": None,
            "firma_profesor_url": None,
            "fecha_firma_profesor": None,
            "observaciones_rechazo": None,
        },
    ]


class ClinicState(rx.State):
    patients: list[Patient] = create_initial_patients()
    student_patients: list[Patient] = []
    filter_student: str = ""
    filter_status: str = ""
    new_patient_name: str = ""
    new_patient_age: int = 0
    show_add_patient_modal: bool = False
    show_reject_dialog: bool = False
    reject_observation: str = ""
    odontogram_tool: str = "Ninguno"
    odontogram_diagnostics: list[str] = [
        "Ninguno",
        "Caries",
        "Sellante",
        "Restauración",
    ]
    opciones_sexo: list[str] = [
        "Masculino",
        "Femenino",
        "No especificado",
    ]
    opciones_estado_civil: list[str] = [
        "Soltero(a)",
        "Casado(a)",
        "Divorciado(a)",
        "Viudo(a)",
        "Unión Libre",
    ]
    opciones_escolaridad: list[str] = [
        "Sin estudios",
        "Primaria",
        "Secundaria",
        "Bachillerato",
        "Licenciatura",
        "Posgrado",
    ]
    nueva_nota_evolucion: str = ""
    nueva_nota_observaciones: str = ""

    @rx.var
    def selected_patient(self) -> Patient | None:
        patient_id = self.router.page.params.get(
            "patient_id", None
        )
        if not patient_id:
            return None
        return next(
            (
                p
                for p in self.patients
                if p["id"] == patient_id
            ),
            None,
        )

    @rx.var
    def safe_patient_name(self) -> str:
        return (
            self.selected_patient["nombre"]
            if self.selected_patient
            else "Cargando..."
        )

    @rx.var
    def safe_status(self) -> str:
        return (
            self.selected_patient["status"]
            if self.selected_patient
            else "Borrador"
        )

    @rx.var
    def safe_observaciones_rechazo(self) -> str:
        return (
            self.selected_patient["observaciones_rechazo"]
            if self.selected_patient
            else ""
        )

    @rx.var
    def safe_seguimiento(self) -> list[NotaEvolucion]:
        if self.selected_patient:
            return self.selected_patient.get(
                "historia_clinica", {}
            ).get("seguimiento", [])
        return []

    @staticmethod
    def get_history_value(
        history: rx.Var[ClinicalHistory],
        field_path: list[str],
        default: FieldValue = "",
    ) -> rx.Var:
        current_level = history
        for key in field_path:
            current_level = current_level.get(key, {})
        return rx.cond(
            current_level == {},
            rx.cond(
                isinstance(default, (str, int, float)),
                default.to_string(),
                "",
            ),
            current_level.to_string(),
        )

    @staticmethod
    def is_tooth_missing(
        history: rx.Var[ClinicalHistory], tooth_number: str
    ) -> rx.Var[bool]:
        return (
            history.get("odontograma", {})
            .get("teeth", {})
            .get(tooth_number, {})
            .get("missing", False)
        )

    @staticmethod
    def get_tooth_surface_finding(
        history: rx.Var[ClinicalHistory],
        tooth_number: str,
        surface: str,
    ) -> rx.Var[str]:
        return (
            history.get("odontograma", {})
            .get("teeth", {})
            .get(tooth_number, {})
            .get("surfaces", {})
            .get(surface, "")
        )

    @rx.var
    def is_history_form_invalid(self) -> bool:
        if not self.selected_patient:
            return True
        history = self.selected_patient["historia_clinica"]
        required_fields = [
            history.get("datos_generales", {}).get(
                "nombre_completo"
            ),
            history.get("datos_generales", {}).get("edad"),
            history.get("padecimiento_actual", {}).get(
                "motivo_consulta"
            ),
        ]
        return not all(required_fields)

    @rx.var
    def professor_patients(self) -> list[Patient]:
        filtered_patients = [p for p in self.patients]
        if self.filter_student:
            filtered_patients = [
                p
                for p in filtered_patients
                if self.filter_student
                in p["estudiante_email"]
            ]
        if self.filter_status:
            filtered_patients = [
                p
                for p in filtered_patients
                if p["status"] == self.filter_status
            ]
        return filtered_patients

    @rx.var
    def unique_student_emails(self) -> list[str]:
        return sorted(
            list(
                {
                    p["estudiante_email"]
                    for p in self.patients
                }
            )
        )

    @rx.event
    async def load_student_patients(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user_email:
            self.student_patients = [
                p
                for p in self.patients
                if p["estudiante_email"]
                == auth_state.current_user_email
            ]

    def _get_patient_index(
        self, patient_id: str | None
    ) -> int | None:
        if not patient_id:
            return None
        for i, p in enumerate(self.patients):
            if p["id"] == patient_id:
                return i
        return None

    def _generate_pdf_content(self) -> str:
        if not self.selected_patient:
            return ""
        patient = self.selected_patient
        history = patient["historia_clinica"]

        def field_html(label, value):
            val = value if value else "N/A"
            return f'<div class="pdf-field">\n                        <span class="pdf-field-label">{label}</span>\n                        <span class="pdf-field-value">{val}</span>\n                    </div>'

        def section_html(title, content):
            return f'<div class="pdf-section">\n                        <h2>{title}</h2>\n                        <div class="pdf-grid">{content}</div>\n                    </div>'

        sections = []
        dg = history.get("datos_generales", {})
        dg_content = (
            field_html(
                "Nombre Completo", dg.get("nombre_completo")
            )
            + field_html("Edad", dg.get("edad"))
            + field_html("Sexo", dg.get("sexo"))
            + field_html(
                "Fecha de Nacimiento",
                dg.get("fecha_nacimiento"),
            )
            + field_html(
                "Estado Civil", dg.get("estado_civil")
            )
            + field_html("Ocupación", dg.get("ocupacion"))
            + field_html("Dirección", dg.get("direccion"))
            + field_html("Teléfono", dg.get("telefono"))
        )
        sections.append(
            section_html("Datos Generales", dg_content)
        )
        odonto_html = "<table class='odontogram-table'><tr><th>Diente</th><th>Estado</th></tr>"
        teeth = history.get("odontograma", {}).get(
            "teeth", {}
        )
        for tooth_num, tooth_data in sorted(teeth.items()):
            status = []
            if tooth_data.get("missing"):
                status.append("Ausente")
            surfaces = tooth_data.get("surfaces", {})
            for surface, finding in surfaces.items():
                if finding:
                    status.append(
                        f"{surface.capitalize()}: {finding}"
                    )
            status_str = (
                ", ".join(status) if status else "Sano"
            )
            odonto_html += f"<tr><td>{tooth_num}</td><td>{status_str}</td></tr>"
        odonto_html += "</table>"
        sections.append(
            f"<div class='pdf-section'><h2>Odontograma</h2>{odonto_html}</div>"
        )
        evolucion_html = ""
        for note in history.get("seguimiento", []):
            evolucion_html += f"""\n                <div class="pdf-field" style="grid-column: span 2;">\n                    <span class="pdf-field-label">Fecha: {note.get('fecha_hora')}</span>\n                    <p class="pdf-field-value"><b>Procedimiento:</b> {note.get('procedimiento_signos_vitales')}<br><b>Observaciones:</b> {note.get('observaciones')}</p>\n                </div>"""
        sections.append(
            section_html(
                "Notas de Evolución", evolucion_html
            )
        )
        firma_profesor = f"<p>Firma Profesor: {('Sí' if patient.get('firma_profesor_url') else 'No')}</p>"
        firma_paciente = f"<p>Consentimiento Paciente: {('Aceptado' if history.get('firma_consentimiento', {}).get('aceptado') else 'No Aceptado')}</p>"
        sections.append(
            f"<div class='pdf-section'><h2>Firmas y Consentimiento</h2>{firma_paciente}{firma_profesor}</div>"
        )
        full_html = f"""\n        <html>\n            <head>\n                <link rel="stylesheet" href="/pdf_styles.css">\n            </head>\n            <body>\n                <div class="pdf-container">\n                    <div class="pdf-header">\n                        <img src="/logo_design_upem.png" alt="Logo UPEM">\n                        <h1>Historia Clínica Odontológica</h1>\n                    </div>\n                    {''.join(sections)}\n                </div>\n            </body>\n        </html>\n        """
        return full_html

    @rx.event
    def toggle_add_patient_modal(self):
        self.show_add_patient_modal = (
            not self.show_add_patient_modal
        )

    @rx.event
    def toggle_reject_dialog(self):
        self.show_reject_dialog = (
            not self.show_reject_dialog
        )
        if not self.show_reject_dialog:
            self.reject_observation = ""

    @rx.event
    def set_new_patient_name(self, name: str):
        self.new_patient_name = name

    @rx.event
    def set_new_patient_age(self, age: str):
        try:
            self.new_patient_age = int(age)
        except (ValueError, TypeError):
            self.new_patient_age = 0

    @rx.event
    def set_nueva_nota_evolucion(self, value: str):
        self.nueva_nota_evolucion = value

    @rx.event
    def set_nueva_nota_observaciones(self, value: str):
        self.nueva_nota_observaciones = value

    def _update_history_field(
        self, field_path: list[str], value: FieldValue
    ):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        idx = self._get_patient_index(patient_id)
        if idx is not None:
            patients_copy = copy.deepcopy(self.patients)
            current_level = patients_copy[idx][
                "historia_clinica"
            ]
            for key in field_path[:-1]:
                if key not in current_level:
                    current_level[cast(str, key)] = {}
                current_level = current_level[
                    cast(str, key)
                ]
            current_level[cast(str, field_path[-1])] = value
            self.patients = patients_copy

    @rx.event
    def update_history_field_str(
        self, field_path: list[str], value: str
    ):
        self._update_history_field(field_path, value)

    @rx.event
    def update_history_field_bool(
        self, field_path: list[str], value: str
    ):
        self._update_history_field(
            field_path, value == "true"
        )

    @rx.event
    def update_tooth_surface(
        self, tooth_id: str, surface: str
    ):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        idx = self._get_patient_index(patient_id)
        if (
            idx is not None
            and self.odontogram_tool
            and (self.odontogram_tool != "Ninguno")
        ):
            patients_copy = copy.deepcopy(self.patients)
            tooth_data = patients_copy[idx][
                "historia_clinica"
            ]["odontograma"]["teeth"].setdefault(
                tooth_id, {}
            )
            tooth_surfaces = tooth_data.setdefault(
                "surfaces", {}
            )
            current_finding = tooth_surfaces.get(
                surface, ""
            )
            if current_finding == self.odontogram_tool:
                tooth_surfaces[surface] = ""
            else:
                tooth_surfaces[surface] = (
                    self.odontogram_tool
                )
            self.patients = patients_copy

    @rx.event
    def toggle_tooth_missing(self, tooth_id: str):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        idx = self._get_patient_index(patient_id)
        if idx is not None:
            patients_copy = copy.deepcopy(self.patients)
            tooth_data = patients_copy[idx][
                "historia_clinica"
            ]["odontograma"]["teeth"].setdefault(
                tooth_id, {}
            )
            tooth_data["missing"] = not tooth_data.get(
                "missing", False
            )
            self.patients = patients_copy

    @rx.event
    async def add_patient(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user_email:
            yield rx.toast.error(
                "No se pudo identificar al estudiante."
            )
            return
        if (
            not self.new_patient_name
            or self.new_patient_age <= 0
        ):
            yield rx.toast.error(
                "Nombre y edad del paciente son requeridos."
            )
            return
        new_id = f"p{len(self.patients) + 1}"
        today = datetime.date.today().isoformat()
        empty_history = create_empty_history()
        empty_history["datos_generales"][
            "nombre_completo"
        ] = self.new_patient_name
        empty_history["datos_generales"]["edad"] = str(
            self.new_patient_age
        )
        empty_history["datos_generales"][
            "fecha_ingreso"
        ] = today
        empty_history["datos_administrativos"][
            "nombre_estudiante"
        ] = auth_state.current_user_name
        empty_history["datos_administrativos"][
            "matricula_estudiante"
        ] = auth_state.current_user_email
        new_patient: Patient = {
            "id": new_id,
            "nombre": self.new_patient_name,
            "edad": self.new_patient_age,
            "fecha_registro": today,
            "status": "Borrador",
            "estudiante_email": auth_state.current_user_email,
            "historia_clinica": empty_history,
            "firma_paciente_url": None,
            "firma_profesor_url": None,
            "fecha_firma_profesor": None,
            "observaciones_rechazo": None,
        }
        self.patients.append(new_patient)
        self.new_patient_name = ""
        self.new_patient_age = 0
        self.show_add_patient_modal = False
        yield ClinicState.load_student_patients
        yield rx.toast.success(
            f"Paciente '{new_patient['nombre']}' agregado."
        )

    @rx.event
    def submit_for_review(self):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        idx = self._get_patient_index(patient_id)
        if idx is not None:
            self.patients[idx]["status"] = "Pendiente"
            self.patients[idx][
                "observaciones_rechazo"
            ] = None
            return rx.toast.info(
                "Historia clínica enviada para revisión."
            )

    @rx.event
    def approve_history(self):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        idx = self._get_patient_index(patient_id)
        if idx is not None:
            self.patients[idx]["status"] = "Aprobado"
            self.patients[idx][
                "firma_profesor_url"
            ] = "/placeholder.svg"
            self.patients[idx][
                "fecha_firma_profesor"
            ] = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            return rx.toast.success(
                "Historia clínica aprobada y firmada."
            )

    @rx.event
    def reject_history(self):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        if not self.reject_observation:
            return rx.toast.error(
                "Las observaciones son requeridas para rechazar."
            )
        idx = self._get_patient_index(patient_id)
        if idx is not None:
            self.patients[idx]["status"] = "Rechazado"
            self.patients[idx][
                "observaciones_rechazo"
            ] = self.reject_observation
            self.reject_observation = ""
            self.show_reject_dialog = False
            return rx.toast.warning(
                "Historia clínica rechazada con observaciones."
            )

    @rx.event
    def set_reject_observation(self, observation: str):
        self.reject_observation = observation

    @rx.event
    def generate_pdf(self):
        if not self.selected_patient:
            return rx.toast.error(
                "No hay un paciente seleccionado."
            )
        pdf_content = self._generate_pdf_content()
        filename = f"historia_clinica_{self.selected_patient['nombre'].replace(' ', '_')}.html"
        return rx.download(
            data=pdf_content, filename=filename
        )

    @rx.event
    def set_odontogram_tool(self, tool: str):
        self.odontogram_tool = tool

    @rx.event
    def add_evolucion_note(self):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        idx = self._get_patient_index(patient_id)
        if idx is not None:
            if not self.nueva_nota_evolucion and (
                not self.nueva_nota_observaciones
            ):
                return rx.toast.error(
                    "Debe completar al menos un campo de la nota."
                )
            new_note = {
                "fecha_hora": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "procedimiento_signos_vitales": self.nueva_nota_evolucion,
                "observaciones": self.nueva_nota_observaciones,
            }
            self.patients[idx]["historia_clinica"][
                "seguimiento"
            ].append(new_note)
            self.nueva_nota_evolucion = ""
            self.nueva_nota_observaciones = ""

    @rx.event
    def delete_evolucion_note(self, index: int):
        patient_id = self.router.page.params.get(
            "patient_id"
        )
        idx = self._get_patient_index(patient_id)
        if idx is not None:
            del self.patients[idx]["historia_clinica"][
                "seguimiento"
            ][index]