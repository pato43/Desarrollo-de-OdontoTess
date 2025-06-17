import reflex as rx
from typing import TypedDict, Literal

Role = Literal["student", "professor"]


class User(TypedDict):
    password: str
    role: Role
    full_name: str


class AuthState(rx.State):
    users: dict[str, User] = {
        "estudiante@odontotess.com": {
            "password": "password123",
            "role": "student",
            "full_name": "Juan Pérez Estudiante",
        },
        "profesor@odontotess.com": {
            "password": "password123",
            "role": "professor",
            "full_name": "Dra. Ana García",
        },
    }
    in_session: bool = False
    current_user_email: str = ""
    current_user_role: Role | str = ""

    @rx.var
    def current_user_name(self) -> str:
        if self.current_user_email and self.users.get(
            self.current_user_email
        ):
            return self.users[self.current_user_email][
                "full_name"
            ]
        return "Usuario"

    @rx.var
    def is_student(self) -> bool:
        return self.current_user_role == "student"

    @rx.var
    def is_professor(self) -> bool:
        return self.current_user_role == "professor"

    @rx.event
    def sign_up(self, form_data: dict):
        email = form_data["email"].lower()
        if (
            not email
            or not form_data["password"]
            or (not form_data["full_name"])
        ):
            return rx.toast.error(
                "Todos los campos son obligatorios."
            )
        if email in self.users:
            return rx.toast.error(
                "El correo electrónico ya está en uso."
            )
        if not form_data.get("role"):
            return rx.toast.error(
                "Por favor, seleccione un rol."
            )
        self.users[email] = {
            "password": form_data["password"],
            "role": form_data["role"],
            "full_name": form_data["full_name"],
        }
        self.in_session = True
        self.current_user_email = email
        self.current_user_role = form_data["role"]
        return rx.redirect("/dashboard")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data["email"].lower()
        user_data = self.users.get(email)
        if (
            user_data
            and user_data["password"]
            == form_data["password"]
        ):
            self.in_session = True
            self.current_user_email = email
            self.current_user_role = user_data["role"]
            return rx.redirect("/dashboard")
        else:
            self.in_session = False
            self.current_user_email = ""
            self.current_user_role = ""
            return rx.toast.error(
                "Correo electrónico o contraseña no válidos."
            )

    @rx.event
    def sign_out(self):
        self.in_session = False
        self.current_user_email = ""
        self.current_user_role = ""
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        current_page = self.router.page.path
        if self.in_session:
            if current_page in [
                "/sign-in",
                "/sign-up",
                "/",
            ]:
                return rx.redirect("/dashboard")
        elif current_page not in ["/sign-in", "/sign-up"]:
            return rx.redirect("/sign-in")